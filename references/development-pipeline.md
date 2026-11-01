# Development Pipeline — phase checklists & gates

Use with SKILL.md §6. Every phase has: **who**, **inputs**, **work**, **deliverables**, and a
**gate** (exit criteria). Scale to the tier: S-tier projects compress phases 1–2 into one
short pass; XL projects repeat phases 2–6 per milestone / vertical slice.

## Milestones (M+ tiers)

| Milestone | Meaning | Must be true |
|---|---|---|
| Concept | idea validated on paper | pillars, core loop, engine, scope agreed |
| Prototype | core loop playable | runs; placeholder art; one test level |
| Vertical slice | one representative chunk at near-final quality | all key systems in one level, final-ish art/audio for it |
| Alpha | feature complete | all features in, content placeholder allowed, no S1 bugs known unaddressed |
| Beta | content complete | all content in, only polish/bugfix left, no open S1, S2 tracked |
| Release Candidate | shippable candidate | no open S1/S2, smoke+regression pass on the built artifact |
| Gold / Release | shipped | versioned build delivered, release notes, store materials |

## Phase 1 — Pre-production
**Who:** 01 Executive Producer, 02 Project Manager, 03 Game Director, 04 Creative Director,
05 Technical Director, 06 Lead Game Designer (+ 07–10 as needed for M+).

**Inputs:** user request, existing project scan, available tooling list.

**Work (parallel where marked ∥):**
1. ∥ 03 – vision: 3 design pillars, target experience, reference *feelings* (never copy).
2. ∥ 04 – creative identity: tone, mood, audiovisual direction, naming/branding.
3. ∥ 05 – tech assessment: engine recommendation/confirmation, platforms, architecture
   sketch, tech risks, what can be built/tested in this environment.
4. 01 – scope & goals: tier, MVP feature list (must/should/could/won't), success criteria.
5. 06 – GDD (`templates/GDD.md`): core loop, mechanics, controls, progression, content list.
6. 05 – `TECHNICAL_DESIGN.md` (`templates/TECHNICAL_DESIGN.md`) for M+.
7. 02 – `TASKS.md` with dependencies + `PROJECT_STATUS.md`.

**Gate:** pillars + core loop + engine + MVP scope written; assumptions logged; task list
exists with owners and dependencies; risks listed with mitigations.

## Phase 2 — Prototyping
**Who:** 06, 08, 22, 13, 19 (+24 for physics-heavy, +23 for AI-centric, +25 for multiplayer core).

**Work:**
1. 05/26 – project skeleton: engine project, folder layout, run/build/test commands working.
2. 22 – player controller + core mechanic, input map, minimal game state.
3. 08 – greybox test level (primitives/tiles), metrics documented (jump height, speeds).
4. 13 – minimal HUD + start/restart flow.
5. 19 – placeholder asset convention + import settings so art can drop in later.
6. 29 – smoke test: launches, core loop playable start→fail/win→restart.
7. 03 – "is it fun / does the loop work?" review → keep / iterate / pivot.

**Gate:** builds and runs here (or verified by the available runtime), loop playable
end-to-end, Game Director approval or a documented iteration list.

## Phase 3 — Production
**Who:** whatever the GDD needs. Typical parallel batches (disjoint ownership):
- Batch A design: 07 balance tables, 08 levels, 09 narrative, 10 economy.
- Batch B art: 14 art bible first → 15 concepts → 16/17/18 assets ∥ → 19 import → 20 anims, 21 VFX.
- Batch C code: 22 systems, 23 AI, 24 combat/physics, 25 network, 13 UI — each owns its modules.
- Batch D audio: 27 SFX + audio manager, 28 music + music system.
Integrate (Phase 4 mini-pass) after each batch rather than once at the end.

**Gate:** every MVP feature implemented and wired; content per GDD present (placeholder
allowed where art not ready); task board up to date.

## Phase 4 — Integration
**Who:** Coordinator, 05, 26.
1. Diff review per module; enforce coding standards and single-source-of-truth systems.
2. Resolve conflicts (file, naming, API, input bindings, layer/collision matrices).
3. Fix every asset reference / path / import error.
4. Clean build from scratch (delete caches if needed) + launch.
5. Update `TECHNICAL_DESIGN.md` if architecture drifted.

**Gate:** clean build + launch with no errors; warnings triaged; no orphan/duplicate systems.

## Phase 5 — QA & Testing
**Who:** 29 lead; owners fix.
Test types: functional, gameplay/progression, UI/navigation, input (keyboard/mouse/gamepad/
touch as targeted), performance (frame time, memory, load times), compatibility (target OS/
browser), resolution & aspect ratio (at least 16:9, 16:10, 21:9, 4:3 or mobile portrait as
relevant), save/load, audio, regression. See `qa-standards.md`.

**Gate:** QA report exists; no open S1; S2s fixed or explicitly accepted by 01 + user informed.

## Phase 6 — Polish & Optimization
**Who:** 19, 20, 21, 27, 28, 11, 12, 13, 22, 24 as relevant; 29 regression.
- Profile first, then optimise the measured hotspots (draw calls, overdraw, physics steps,
  GC/allocations, texture memory, audio voices).
- Remove unused assets/code; compress textures/audio.
- Game feel: hit-stop, screen shake (with accessibility toggle), easing, anticipation.
- Audio mix pass (levels, ducking, loudness targets in `audio-pipeline.md`).
- UX pass: readability, feedback, onboarding, settings (volume, key rebinding where feasible).
- Final full playthrough by 29 (+03 sign-off on feel).

**Gate:** performance budget met on target, regression pass, no new S1/S2.

## Phase 7 — Release
**Who:** 26 build, 29 final smoke, 30 publishing, 01 go/no-go.
1. Version bump (semver `MAJOR.MINOR.PATCH`), changelog.
2. Release build per platform (export presets / build scripts) — debug symbols off, release flags on.
3. Smoke test **the built artifact**, not the editor.
4. `RELEASE_NOTES.md`, store page copy, screenshots (captured from the real build), press kit outline.
5. Checksums + artifact list; license/attribution file shipped if external assets used.
6. 01 go/no-go; deliver artifact path(s) + run instructions to the user.

**Gate:** artifact exists and was smoke-tested (or is explicitly marked "build command
provided, not built here" with the reason).

## Iteration rules
- A failed gate → back to the phase that owns the problem, not a full restart.
- Change requests mid-production: 01 evaluates scope impact, 02 re-plans, owners update docs.
- Keep each loop small: build → test → fix in short cycles.
