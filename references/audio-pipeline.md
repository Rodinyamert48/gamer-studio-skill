# Audio Pipeline — SFX, music, implementation, mixing

Audio is produced **reproducibly**: procedural synthesis scripts (Python `numpy`/`wave`,
`sox`, `ffmpeg` filters, WebAudio, jsfxr-style parameter sets), tracker/MIDI-style
note data rendered by script, or verified-licence external sound/music (CC0/CC-BY, logged
in `studio/ASSET_LICENSES.md`). Keep generator scripts in `tools/audio/`. Never use
music or sounds ripped from existing games, films or songs.

## 1. Audio direction (Sound Designer + Composer, approved by Creative Director)
- Sonic identity: 3 adjectives (e.g. "crunchy, warm, retro"), reference *qualities* not tracks.
- Palette: synthesis types/instruments, tempo range, key/mode per mood.
- Feedback priorities: which events must always be heard (player damage, pickup, UI confirm).

## 2. Event list (`studio/AUDIO_EVENTS.md` or in GDD)
| Event | Trigger | Asset(s) | Variations | Priority | Bus |
|---|---|---|---|---|---|
| `player_jump` | jump start | `sfx_player_jump_01..03.ogg` | 3 + pitch ±5% | high | SFX |
| `ui_confirm` | button press | `sfx_ui_confirm.ogg` | 1 | high | UI |
| `mus_level_1` | level start | `mus_level1_loop.ogg` | loop | — | Music |

## 3. Naming & formats
- `sfx_<category>_<name>[_<variant>]`, `amb_<place>`, `mus_<context>[_<layer>]`, `vo_<char>_<line_id>`.
- Source: 48 kHz (or 44.1) 16/24-bit WAV in `assets/audio/_source/`.
- Runtime: OGG Vorbis (music/ambience, long SFX), WAV for very short latency-critical SFX
  where the engine prefers it; MP3/OGG/WebM for web (check browser support; OGG not on older Safari → provide fallback if targeting Safari).
- Mono for positional SFX; stereo for music/ambience/UI.

## 4. Implementation rules
- One **audio manager/service** (or engine buses) — no ad-hoc players scattered across scripts.
- Buses: `Master → Music, SFX, UI, Ambience, Voice`; user volume settings per bus, persisted.
- Random variation (2–4 variants, pitch ±3–8%) for frequent sounds to avoid fatigue.
- Voice limiting / cooldowns for spammy events; priority stealing for important cues.
- Ducking: music ducks under dialogue/stingers.
- Web: unlock AudioContext on first user gesture; pause/resume on visibility change.
- Sync: trigger SFX from animation events/hit frames, not timers guessed in code.

## 5. Adaptive music (Composer)
- Techniques: horizontal re-sequencing (switch segments on bar boundaries), vertical layering
  (add/remove stems by intensity), stingers for events (win, level up, boss).
- Loop points must be seamless (zero-crossing / crossfade); document BPM and bar length.
- Transition table: `explore → combat` (crossfade 1 bar), `combat → victory` (stinger + fade), …

## 6. Loudness & mix targets
- Integrated loudness: about **−16 LUFS** for web/mobile, **−14 to −18 LUFS** desktop/console; peaks ≤ **−1 dBTP**.
- Music sits under SFX by ~3–6 dB in gameplay; UI sounds short and consistent.
- Check with `ffmpeg -i file -af ebur128 -f null -` (where ffmpeg is available).

## 7. Review checklist
- [ ] Every event in the list has an asset and triggers in-game (QA verifies)
- [ ] No clipping; loudness within target; loops seamless
- [ ] Volume settings work and persist
- [ ] Licence recorded for any non-original audio
