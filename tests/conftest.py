"""Shared fixtures: fake Alice/Sonos players driven by fake services.

The fakes behave like the real players closely enough for the sync engine:
volume_set updates volume_level, play_media starts the leader (and its group),
seek moves the position, pause/play flip the state. Every call is recorded.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

import pytest

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.util import dt as dt_util

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ALICE = "media_player.yandex_station_mini"
SONOS = "media_player.sonos_amp_zal"
SONOS_2 = "media_player.sonos_five_oshxona"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Load custom_components/ in every test."""
    yield


def _ids(call: ServiceCall) -> list[str]:
    entity_ids = call.data.get("entity_id", [])
    return [entity_ids] if isinstance(entity_ids, str) else list(entity_ids)


class FakePlayers:
    """Fake media_player / music_assistant services with call recording."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.fail_play_media: Exception | None = None

    def set(self, entity_id: str, state: str | None = None, **attrs: Any) -> None:
        current = self.hass.states.get(entity_id)
        new_state = state if state is not None else (current.state if current else "idle")
        merged = {**(current.attributes if current else {}), **attrs}
        self.hass.states.async_set(entity_id, new_state, merged)

    def attr(self, entity_id: str, name: str) -> Any:
        return self.hass.states.get(entity_id).attributes.get(name)

    def state(self, entity_id: str) -> str:
        return self.hass.states.get(entity_id).state

    def called(self, domain: str, service: str) -> list[dict[str, Any]]:
        return [data for d, s, data in self.calls if (d, s) == (domain, service)]

    def register(self) -> None:
        handlers = {
            ("media_player", "volume_set"): self._volume_set,
            ("media_player", "media_pause"): self._pause,
            ("media_player", "media_play"): self._play,
            ("media_player", "media_seek"): self._seek,
            ("media_player", "join"): self._join,
            ("media_player", "unjoin"): self._unjoin,
            ("music_assistant", "play_media"): self._play_media,
        }
        for (domain, service), handler in handlers.items():
            self.hass.services.async_register(domain, service, self._recorder(domain, service, handler))

    def _recorder(self, domain: str, service: str, handler):
        async def _handle(call: ServiceCall) -> None:
            self.calls.append((domain, service, dict(call.data)))
            await handler(call)

        return _handle

    async def _volume_set(self, call: ServiceCall) -> None:
        for entity_id in _ids(call):
            self.set(entity_id, volume_level=call.data["volume_level"])

    async def _pause(self, call: ServiceCall) -> None:
        for entity_id in _ids(call):
            self.set(entity_id, "paused")

    async def _play(self, call: ServiceCall) -> None:
        for entity_id in _ids(call):
            self.set(entity_id, "playing")

    async def _seek(self, call: ServiceCall) -> None:
        for entity_id in _ids(call):
            self.set(
                entity_id,
                media_position=call.data["seek_position"],
                media_position_updated_at=dt_util.utcnow(),
            )

    async def _join(self, call: ServiceCall) -> None:
        for entity_id in _ids(call):
            self.set(entity_id, group_members=[entity_id, *call.data["group_members"]])

    async def _unjoin(self, call: ServiceCall) -> None:
        return

    async def _play_media(self, call: ServiceCall) -> None:
        if self.fail_play_media is not None:
            raise self.fail_play_media
        for leader in _ids(call):
            group = self.attr(leader, "group_members") or [leader]
            for entity_id in {leader, *group}:
                self.set(
                    entity_id,
                    "playing",
                    media_content_id=call.data["media_id"],
                    media_position=0,
                    media_position_updated_at=dt_util.utcnow(),
                )


@pytest.fixture
def players(hass: HomeAssistant) -> FakePlayers:
    fake = FakePlayers(hass)
    fake.register()
    fake.set(ALICE, "idle", volume_level=0.6, media_content_type="music")
    for sonos in (SONOS, SONOS_2):
        fake.set(sonos, "idle", volume_level=0.3, media_content_id=None, supported_features=524288)
    return fake


async def wait_until_idle(controller, timeout: float = 15.0) -> None:
    """Wait for the controller's handoff/stop/mirror run to finish."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        tasks = [t for t in (controller._task, controller._vol_task) if t is not None]
        if all(t.done() for t in tasks):
            return
        await asyncio.sleep(0.05)
    raise AssertionError("controller run did not finish in time")
