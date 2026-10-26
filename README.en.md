# 🎶 Alice ↔ Sonos — Smooth Sync

> A Home Assistant integration (+ blueprints) that hands music off from a
> Yandex Station (**Alice**) to **Sonos** speakers/amps (Sonos Amp, Port, Era,
> Five, Arc, Beam…) through **Music Assistant** — starting at the *exact same
> second*, with a smooth crossfade — and gracefully brings it back when
> playback stops.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
![ha](https://img.shields.io/badge/Home%20Assistant-2024.12%2B-41BDF5)
![license](https://img.shields.io/badge/license-MIT-green)

🇺🇿 O'zbekcha: [`README.md`](README.md)

This is the **Sonos** edition of
[alice-arylic-sync](https://github.com/nurillaevich/alice-arylic-sync): the same
sync engine, with Sonos naming, Sonos defaults and two Sonos-specific features.
The UI is in Uzbek.

---

## What it does

| Situation | What happens |
|---|---|
| **A track starts on Alice** | The same track starts on the Sonos at the same second, then a **step-by-step** crossfade: Sonos up → Alice down → … Ends with Alice **muted** and the Sonos at full volume. |
| **Music stops on Alice** | The Sonos fades down and pauses, then gets its **volume back**; Alice is restored to a set level (e.g. **50%**). |
| **Pause pressed on the Sonos** (app or buttons) | Alice pauses too and gets her voice back. Press **Play** on the Sonos and Alice resumes, muted. |
| **"Alice, louder / quieter"** | After a handoff the change goes to the **Sonos**, not the muted Station. |

## Sonos-specific features

| Feature | Default | Why |
|---|---|---|
| **Mirror a Sonos pause to Alice** | on | Pausing from the Sonos app or touch controls no longer leaves the muted Station playing on alone (whose next track would restart the Sonos by itself). A natural track end (`idle`) is not treated as a pause. |
| **Restore the Sonos volume after a stop** | on | The stop fades the Sonos to 1 %; without this the next play from the Sonos app would start at 1 %. |
| **Sonos target volume 25 %** | `0.25` | Sonos Amp / Five / Arc are loud. Tune it in **Configure**. |

Everything else is as in the original: multi-room, a **Sonos group** toggle,
voice-volume redirect, voice-command blip detection, a **Repairs** issue when
Music Assistant cannot play the track.

## Requirements

1. Home Assistant **2024.12+** (blueprints: 2024.10+).
2. **[Music Assistant](https://music-assistant.io/)** integration.
3. Sonos added to Music Assistant: **Settings → Providers → Add provider → Sonos**
   (or **Sonos S1** for legacy S1 systems).
4. Yandex Station in HA (e.g. [AlexxIT/YandexStation](https://github.com/AlexxIT/YandexStation)).
5. The **Yandex Music** provider in Music Assistant (or change **Track URI prefix**).

Pick the Sonos' **Music Assistant** `media_player` as the output — not the entity
from HA's own Sonos integration (`music_assistant.play_media` only accepts MA
players; the picker only lists them).

## Install

**HACS:** HACS → ⋮ → **Custom repositories** →
`https://github.com/nurillaevich/alice-sonos-sync`, type **Integration** →
Download → restart HA → **Settings → Devices & Services → Add Integration →
Alice ↔ Sonos Sync** → **Alice → Sonos pair**.

**Manual:** copy `custom_components/alice_sonos_sync/` into
`config/custom_components/` and restart.

**Blueprints:** import
`blueprints/automation/alice_sonos/alice_sonos_handoff_start.yaml` and
`alice_sonos_smooth_stop.yaml` (no pause mirror, no multi-room — those are
integration-only). Don't run the blueprints and the integration for the same
pair, and don't run alice-arylic-sync and alice-sonos-sync on the same Alice.

## Status

v1.0.0 is covered by automated tests (pytest + Home Assistant). Sync offset and
head-start depend on your network — tune them on first use with
[`docs/TUNING.md`](docs/TUNING.md). Troubleshooting:
[`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

## License

MIT — [`LICENSE`](LICENSE).
