"""Native Sonos outputs (HA's own Sonos integration): no Music Assistant, the
track's stream URL comes from the YandexStation integration's session."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er, issue_registry as ir
from homeassistant.util import dt as dt_util

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.alice_sonos_sync import controller as controller_mod
from custom_components.alice_sonos_sync.const import (
    CONF_ALICE_ENTITY,
    CONF_ENTRY_TYPE,
    CONF_SONOS_ENTITIES,
    DOMAIN,
    ENTRY_TYPE_PAIR,
)

from .conftest import ALICE, SONOS, SONOS_2, FakePlayers, wait_until_idle
from .test_sync import FAST

TRACK = "12345"
STREAM_URL = "http://192.168.90.135/api/yandex_station/token.mp3"
AZAN_URL = "http://192.168.90.135/media/local/azan.mp3"


@pytest.fixture(autouse=True)
def native_sonos(hass: HomeAssistant):
    """Register the speakers as entities of HA's own Sonos integration. Runs
    before the `players` fixture sets their states, so the ids stay free."""
    registry = er.async_get(hass)
    for entity_id in (SONOS, SONOS_2):
        entry = registry.async_get_or_create(
            "media_player", "sonos", f"RINCON_{entity_id}", suggested_object_id=entity_id.split(".")[1]
        )
        assert entry.entity_id == entity_id
    with patch.object(controller_mod, "FOLLOW_CONFIRM_DELAY", 0.1):
        yield


@pytest.fixture
def stream_url():
    with patch.object(
        controller_mod.SyncController,
        "_resolve_stream_url",
        AsyncMock(return_value=STREAM_URL),
    ) as mock:
        yield mock


async def _setup(hass: HomeAssistant, outputs: list[str]):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: outputs, CONF_ENTRY_TYPE: ENTRY_TYPE_PAIR},
        options=FAST,
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry.runtime_data


async def _alice_starts(hass: HomeAssistant, players: FakePlayers, controller) -> None:
    players.set(
        ALICE,
        "playing",
        media_content_id=TRACK,
        media_content_type="music",
        media_position=30,
        media_position_updated_at=dt_util.utcnow(),
    )
    await hass.async_block_till_done()
    await wait_until_idle(controller)


async def test_flow_offers_native_sonos_without_music_assistant(hass: HomeAssistant, players) -> None:
    """The live case: Music Assistant removed — the picker must still work."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"next_step_id": "pair"})
    (sonos_field,) = [k for k in result["data_schema"].schema if k.schema == CONF_SONOS_ENTITIES]
    integrations = {f["integration"] for f in result["data_schema"].schema[sonos_field].config["filter"]}
    assert integrations == {"sonos", "music_assistant"}

    hass.services.async_remove("music_assistant", "play_media")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: [SONOS]}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_handoff_streams_alice_track_to_native_sonos(
    hass: HomeAssistant, players, stream_url
) -> None:
    controller = await _setup(hass, [SONOS])

    await _alice_starts(hass, players, controller)

    stream_url.assert_awaited_once_with(TRACK)
    (play,) = players.called("media_player", "play_media")
    assert play == {"entity_id": SONOS, "media_content_id": STREAM_URL, "media_content_type": "music"}
    assert not players.called("music_assistant", "play_media")
    (seek,) = players.called("media_player", "media_seek")
    assert 35 <= seek["seek_position"] <= 37
    assert players.attr(SONOS, "volume_level") == 0.25
    assert players.attr(ALICE, "volume_level") == 0
    assert controller.last_run == "handoff"


async def test_native_multiroom_joins_and_streams_once(hass: HomeAssistant, players, stream_url) -> None:
    controller = await _setup(hass, [SONOS, SONOS_2])

    await _alice_starts(hass, players, controller)

    (join,) = players.called("media_player", "join")
    assert join["group_members"] == [SONOS_2]
    assert len(players.called("media_player", "play_media")) == 1
    assert players.state(SONOS_2) == "playing"


async def test_stream_url_failure_keeps_music_on_alice(hass: HomeAssistant, players) -> None:
    controller = await _setup(hass, [SONOS])

    with patch.object(
        controller_mod.SyncController,
        "_resolve_stream_url",
        AsyncMock(side_effect=RuntimeError("not logged in")),
    ):
        await _alice_starts(hass, players, controller)

    assert not players.called("media_player", "play_media")
    assert players.attr(SONOS, "volume_level") == 0.3
    assert players.attr(ALICE, "volume_level") == 0.6
    assert controller.last_run == "handoff_failed"
    assert any(domain == DOMAIN for domain, _ in ir.async_get(hass).issues)


async def test_stop_fades_and_pauses_our_stream(hass: HomeAssistant, players, stream_url) -> None:
    controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.state(SONOS) == "paused"
    assert players.attr(SONOS, "volume_level") == 0.25  # volume given back
    assert players.attr(ALICE, "volume_level") == 0.5


async def test_azan_over_our_stream_is_left_alone(hass: HomeAssistant, players, stream_url) -> None:
    controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)
    # The azan automation takes the Sonos over.
    players.set(SONOS, "playing", media_content_id=AZAN_URL, volume_level=0.6)

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)
    players.set(SONOS, "paused")  # the azan ends / is paused by its automation
    await hass.async_block_till_done()
    await asyncio.sleep(0.3)
    await wait_until_idle(controller)

    sonos_pauses = [c for c in players.called("media_player", "media_pause") if c["entity_id"] == SONOS]
    assert not sonos_pauses
    assert players.attr(SONOS, "volume_level") == 0.6
    assert players.attr(ALICE, "volume_level") == 0.5


async def test_sonos_airplay_content_uri_is_not_ours(hass: HomeAssistant, players, stream_url) -> None:
    controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)
    players.set(SONOS, "playing", media_content_id="x-sonos-vli:RINCON_X:1,airplay:abc")

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.state(SONOS) == "playing"


async def test_unavailable_sonos_skips_without_touching_alice_later(
    hass: HomeAssistant, players, stream_url
) -> None:
    """The live «Главная Гостиная» case: the speaker was offline, the handoff
    was skipped, and the later stop still set Alice's volume to 0.5."""
    controller = await _setup(hass, [SONOS])
    players.set(SONOS, "unavailable")
    await _alice_starts(hass, players, controller)

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await asyncio.sleep(0.2)
    await wait_until_idle(controller)

    assert not players.called("media_player", "play_media")
    assert not players.called("media_player", "volume_set")
    assert players.attr(ALICE, "volume_level") == 0.6
