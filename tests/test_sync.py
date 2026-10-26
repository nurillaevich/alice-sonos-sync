"""The sync engine end to end against fake players: handoff, stop, the Sonos
volume restore and the Sonos pause/resume mirror."""

from __future__ import annotations

import asyncio
from unittest.mock import patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir
from homeassistant.util import dt as dt_util

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.alice_sonos_sync import controller as controller_mod
from custom_components.alice_sonos_sync.const import (
    CONF_ALICE_ENTITY,
    CONF_ENTRY_TYPE,
    CONF_SONOS_ENTITIES,
    DOMAIN,
    ENTRY_TYPE_PAIR,
    OPT_ALICE_GAP_MS,
    OPT_FOLLOW_SONOS_PAUSE,
    OPT_HEADSTART_MS,
    OPT_RESTORE_SONOS_VOLUME,
    OPT_STEPS,
    OPT_STOP_CONFIRM_DELAY,
    OPT_STOP_STEP_DELAY_MS,
    OPT_STOP_STEPS,
)

from .conftest import ALICE, SONOS, SONOS_2, FakePlayers, wait_until_idle

TRACK = "12345"
TRACK_URI = f"yandex_music://track/{TRACK}"

# Fast but otherwise default timings, so each test takes a second or two.
FAST = {
    OPT_STEPS: 2,
    OPT_HEADSTART_MS: 0,
    OPT_ALICE_GAP_MS: 0,
    OPT_STOP_STEPS: 2,
    OPT_STOP_STEP_DELAY_MS: 0,
    OPT_STOP_CONFIRM_DELAY: 0,
}


@pytest.fixture(autouse=True)
def fast_follow_confirm():
    with patch.object(controller_mod, "FOLLOW_CONFIRM_DELAY", 0.1):
        yield


async def _setup(hass: HomeAssistant, outputs: list[str], **options):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_ALICE_ENTITY: ALICE,
            CONF_SONOS_ENTITIES: outputs,
            CONF_ENTRY_TYPE: ENTRY_TYPE_PAIR,
        },
        options={**FAST, **options},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry, entry.runtime_data


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


async def test_handoff_plays_seeks_and_crossfades(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])

    await _alice_starts(hass, players, controller)

    (play,) = players.called("music_assistant", "play_media")
    assert play["media_id"] == TRACK_URI
    assert play["entity_id"] == SONOS
    (seek,) = players.called("media_player", "media_seek")
    assert 35 <= seek["seek_position"] <= 37  # Alice's 30 s + 5 s offset (+ elapsed)
    assert players.attr(SONOS, "volume_level") == 0.25
    assert players.attr(ALICE, "volume_level") == 0
    assert controller.last_run == "handoff"


async def test_multiroom_groups_the_sonos_players(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS, SONOS_2])

    await _alice_starts(hass, players, controller)

    (join,) = players.called("media_player", "join")
    assert join["entity_id"] == SONOS
    assert join["group_members"] == [SONOS_2]
    assert players.state(SONOS_2) == "playing"
    assert players.attr(SONOS_2, "volume_level") == 0.25


async def test_voice_command_blip_does_not_rerun_handoff(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)

    # "Alisa, gromche": the Station drops out of playing and back, same track.
    players.set(ALICE, "idle")
    players.set(ALICE, "playing")
    await hass.async_block_till_done()
    await asyncio.sleep(0.2)
    await wait_until_idle(controller)

    assert len(players.called("music_assistant", "play_media")) == 1
    assert players.state(SONOS) == "playing"


async def test_stop_fades_pauses_and_restores_sonos_volume(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)
    players.set(SONOS, volume_level=0.3)  # user turned the Sonos up a bit

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.state(SONOS) == "paused"
    fade = [c["volume_level"] for c in players.called("media_player", "volume_set") if c["entity_id"] == SONOS]
    assert 0.01 in fade  # it did fade down before pausing
    assert players.attr(SONOS, "volume_level") == 0.3  # ...and got its volume back
    assert players.attr(ALICE, "volume_level") == 0.5
    assert controller.last_run == "smooth_stop"


async def test_stop_without_volume_restore_stays_at_floor(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS], **{OPT_RESTORE_SONOS_VOLUME: False})
    await _alice_starts(hass, players, controller)

    players.set(ALICE, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.state(SONOS) == "paused"
    assert players.attr(SONOS, "volume_level") == 0.01


async def test_pause_on_sonos_pauses_alice_and_resume_follows(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)

    # Pause pressed on the Sonos itself (app / touch controls).
    players.set(SONOS, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.called("media_player", "media_pause")[-1]["entity_id"] == ALICE
    assert players.state(ALICE) == "paused"
    assert players.attr(ALICE, "volume_level") == 0.5  # voice back while paused
    assert controller.last_run == "follow_pause"

    # Play pressed on the Sonos again: Alice resumes muted, no new handoff.
    players.set(SONOS, "playing")
    await hass.async_block_till_done()
    await wait_until_idle(controller)
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert players.called("media_player", "media_play")[-1]["entity_id"] == ALICE
    assert players.state(ALICE) == "playing"
    assert players.attr(ALICE, "volume_level") == 0
    assert len(players.called("music_assistant", "play_media")) == 1
    assert controller.last_run == "follow_resume"


async def test_short_pause_blip_on_sonos_is_ignored(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)

    players.set(SONOS, "paused")
    players.set(SONOS, "playing")
    await hass.async_block_till_done()
    await wait_until_idle(controller)

    assert not players.called("media_player", "media_pause")
    assert players.state(ALICE) == "playing"


async def test_natural_track_end_on_sonos_does_not_pause_alice(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)

    # Music Assistant ran out of the single handed-off track: idle, not paused.
    players.set(SONOS, "idle")
    await hass.async_block_till_done()
    await asyncio.sleep(0.3)
    await wait_until_idle(controller)

    assert not players.called("media_player", "media_pause")
    assert players.state(ALICE) == "playing"


async def test_follow_pause_can_be_turned_off(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS], **{OPT_FOLLOW_SONOS_PAUSE: False})
    await _alice_starts(hass, players, controller)

    players.set(SONOS, "paused")
    await hass.async_block_till_done()
    await asyncio.sleep(0.3)
    await wait_until_idle(controller)

    assert not players.called("media_player", "media_pause")
    assert players.state(ALICE) == "playing"


async def test_new_track_from_sonos_app_does_not_resume_alice(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    await _alice_starts(hass, players, controller)
    players.set(SONOS, "paused")
    await hass.async_block_till_done()
    await wait_until_idle(controller)
    assert players.state(ALICE) == "paused"

    # The user starts something else from the Sonos app.
    players.set(SONOS, "playing", media_content_id="spotify://track/other")
    await hass.async_block_till_done()
    await asyncio.sleep(0.3)
    await wait_until_idle(controller)

    assert not players.called("media_player", "media_play")
    assert players.state(ALICE) == "paused"


async def test_play_media_failure_keeps_music_on_alice(hass: HomeAssistant, players) -> None:
    _, controller = await _setup(hass, [SONOS])
    players.fail_play_media = RuntimeError("The provider is currently unavailable")

    await _alice_starts(hass, players, controller)

    assert players.attr(SONOS, "volume_level") == 0.3  # put back, not left at floor
    assert players.attr(ALICE, "volume_level") == 0.6  # Alice untouched
    assert controller.last_run == "handoff_failed"
    issues = ir.async_get(hass).issues
    assert any(domain == DOMAIN for domain, _ in issues)


async def test_sync_switch_off_stops_reacting(hass: HomeAssistant, players) -> None:
    entry, controller = await _setup(hass, [SONOS])
    switch_id = next(
        s.entity_id for s in hass.states.async_all("switch") if s.attributes.get("alice_entity") == ALICE
    )
    await hass.services.async_call("switch", "turn_off", {"entity_id": switch_id}, blocking=True)

    await _alice_starts(hass, players, controller)

    assert not players.called("music_assistant", "play_media")
    assert entry.runtime_data.enabled is False
