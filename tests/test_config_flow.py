"""Config and options flow."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.alice_sonos_sync.const import (
    CONF_ALICE_ENTITY,
    CONF_ENTRY_TYPE,
    CONF_GROUP_LEADER,
    CONF_GROUP_MEMBERS,
    CONF_SONOS_ENTITIES,
    DEFAULTS,
    DOMAIN,
    ENTRY_TYPE_GROUP,
    ENTRY_TYPE_PAIR,
    OPT_FOLLOW_SONOS_PAUSE,
    OPT_RESTORE_SONOS_VOLUME,
    OPT_SONOS_TARGET,
)

from .conftest import ALICE, SONOS, SONOS_2


async def _start_menu(hass: HomeAssistant, step: str):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.MENU
    return await hass.config_entries.flow.async_configure(
        result["flow_id"], {"next_step_id": step}
    )


async def test_pair_flow_creates_entry(hass: HomeAssistant, players) -> None:
    result = await _start_menu(hass, "pair")
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: [SONOS, SONOS_2]},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_ALICE_ENTITY: ALICE,
        CONF_SONOS_ENTITIES: [SONOS, SONOS_2],
        CONF_ENTRY_TYPE: ENTRY_TYPE_PAIR,
    }
    await hass.async_block_till_done()
    (entry,) = hass.config_entries.async_entries(DOMAIN)
    assert entry.state is ConfigEntryState.LOADED


async def test_pair_flow_rejects_alice_as_output(hass: HomeAssistant, players) -> None:
    result = await _start_menu(hass, "pair")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: [ALICE]}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "same_entity"}


async def test_pair_flow_needs_music_assistant(hass: HomeAssistant) -> None:
    result = await _start_menu(hass, "pair")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: [SONOS]}
    )
    assert result["errors"] == {"base": "music_assistant_missing"}


async def test_group_flow_creates_entry(hass: HomeAssistant, players) -> None:
    result = await _start_menu(hass, "group")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_GROUP_LEADER: SONOS, CONF_GROUP_MEMBERS: [SONOS_2]}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_ENTRY_TYPE] == ENTRY_TYPE_GROUP


async def test_group_flow_rejects_leader_as_member(hass: HomeAssistant, players) -> None:
    result = await _start_menu(hass, "group")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_GROUP_LEADER: SONOS, CONF_GROUP_MEMBERS: [SONOS]}
    )
    assert result["errors"] == {"base": "leader_in_members"}


async def test_options_flow_defaults_and_save(hass: HomeAssistant, players) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ALICE_ENTITY: ALICE, CONF_SONOS_ENTITIES: [SONOS], CONF_ENTRY_TYPE: ENTRY_TYPE_PAIR},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    defaults = {
        key.schema: key.default() for key in result["data_schema"].schema
    }
    assert defaults[OPT_SONOS_TARGET] == 0.25
    assert defaults[OPT_FOLLOW_SONOS_PAUSE] is True
    assert defaults[OPT_RESTORE_SONOS_VOLUME] is True

    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {**DEFAULTS, OPT_SONOS_TARGET: 0.4}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert entry.options[OPT_SONOS_TARGET] == 0.4


async def test_group_entry_has_no_options(hass: HomeAssistant, players) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_ENTRY_TYPE: ENTRY_TYPE_GROUP,
            CONF_GROUP_LEADER: SONOS,
            CONF_GROUP_MEMBERS: [SONOS_2],
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "group_no_options"
