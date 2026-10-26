"""Constants for the Alice <-> Sonos Sync integration."""

DOMAIN = "alice_sonos_sync"

CONF_ALICE_ENTITY = "alice_entity"
CONF_SONOS_ENTITIES = "sonos_entities"  # one or more outputs (multi-room)

# Entry type: this integration handles two kinds of config entry. A "pair"
# (default) is the Alice -> Sonos handoff. A "group" is a standalone
# speaker-group toggle: one switch that joins 2+ Music Assistant Sonos players
# into one synchronised group (leader + members) on demand — no Alice involved.
CONF_ENTRY_TYPE = "entry_type"
ENTRY_TYPE_PAIR = "pair"
ENTRY_TYPE_GROUP = "group"

# Group-entry data keys.
CONF_GROUP_LEADER = "group_leader"  # the Music Assistant player others join
CONF_GROUP_MEMBERS = "group_members"  # one or more players joined to the leader

# Options (all tunable from the UI). Defaults mirror the blueprint defaults.
OPT_SYNC_OFFSET = "sync_offset"
OPT_HANDOFF_DELAY = "handoff_delay"
OPT_STEPS = "steps"
OPT_HEADSTART_MS = "sonos_headstart_ms"
OPT_ALICE_GAP_MS = "alice_gap_ms"
OPT_SONOS_FLOOR = "sonos_floor"
OPT_SONOS_TARGET = "sonos_target"
OPT_ALICE_END_VOLUME = "alice_end_volume"
OPT_TRACK_URI_PREFIX = "track_uri_prefix"
OPT_MEDIA_TYPE = "media_type"
OPT_PLAY_WAIT_TIMEOUT = "play_wait_timeout"
OPT_BUFFER_WAIT_TIMEOUT = "buffer_wait_timeout"
OPT_STOP_FADE_FLOOR = "stop_fade_floor"
OPT_ALICE_RESTORE_VOLUME = "alice_restore_volume"
OPT_STOP_STEPS = "stop_steps"
OPT_STOP_STEP_DELAY_MS = "stop_step_delay_ms"
OPT_STOP_CONFIRM_DELAY = "stop_confirm_delay"  # debounce real stops vs voice-command blips
# Multi-room robustness levers.
OPT_REGROUP_EACH_TRACK = "regroup_each_track"  # force re-join on every handoff
OPT_SEEK_EACH_OUTPUT = "seek_each_output"  # seek every output, not just the leader
OPT_REDIRECT_VOLUME = "redirect_volume"  # Alice "louder/quieter" -> outputs when handed off
# Escape hatch for players whose stream breaks on a Music Assistant seek: the
# track then plays from 0:00 and Sync offset is the only alignment lever.
OPT_SKIP_SEEK = "skip_seek"
# Sonos-specific behaviour.
# After a smooth stop, put every Sonos back to the volume it was playing at, so
# the next play from the Sonos app / buttons does not start near-silent at the
# fade floor.
OPT_RESTORE_SONOS_VOLUME = "restore_sonos_volume"
# Pause/resume pressed on the Sonos itself (app, touch controls) is mirrored to
# Alice, so the silent Station does not run on alone.
OPT_FOLLOW_SONOS_PAUSE = "follow_sonos_pause"

DEFAULTS: dict[str, float | int | str | bool] = {
    OPT_SYNC_OFFSET: 5.0,
    OPT_HANDOFF_DELAY: 0.0,
    OPT_STEPS: 12,
    OPT_HEADSTART_MS: 350,
    OPT_ALICE_GAP_MS: 180,
    OPT_SONOS_FLOOR: 0.05,
    # Sonos Amp / Five / Arc are loud — start the ramp lower than a small
    # LinkPlay speaker would need; raise it in Configure to taste.
    OPT_SONOS_TARGET: 0.25,
    OPT_ALICE_END_VOLUME: 0.0,
    OPT_TRACK_URI_PREFIX: "yandex_music://track/",
    OPT_MEDIA_TYPE: "track",
    OPT_PLAY_WAIT_TIMEOUT: 12,
    OPT_BUFFER_WAIT_TIMEOUT: 6,
    OPT_STOP_FADE_FLOOR: 0.01,
    OPT_ALICE_RESTORE_VOLUME: 0.5,
    OPT_STOP_STEPS: 10,
    OPT_STOP_STEP_DELAY_MS: 200,
    OPT_STOP_CONFIRM_DELAY: 1.0,
    OPT_REGROUP_EACH_TRACK: False,
    OPT_SEEK_EACH_OUTPUT: False,
    OPT_REDIRECT_VOLUME: True,
    OPT_SKIP_SEEK: False,
    OPT_RESTORE_SONOS_VOLUME: True,
    OPT_FOLLOW_SONOS_PAUSE: True,
}

INVALID_CONTENT_IDS = (None, "", "unknown", "unavailable")
STOP_STATES = ("idle", "paused", "standby", "off")
