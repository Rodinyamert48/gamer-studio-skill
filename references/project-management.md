# Project Management — tasks, status, decisions, versioning

## Task lifecycle

```
BACKLOG → TODO → IN PROGRESS → REVIEW → TESTING → DONE
                     ↘ BLOCKED (with reason + unblock condition) ↗
```
- **BACKLOG**: known, not yet scheduled. **TODO**: scheduled, dependencies met or near.
- **IN PROGRESS**: a specialist is working on it (one owner).
- **REVIEW**: output delivered; Coordinator / lead reviews diff & spec compliance.
- **TESTING**: QA verifying against acceptance criteria.
- **DONE**: acceptance criteria verified with evidence. No evidence → not DONE.
- **BLOCKED**: cannot proceed; record the blocker and who/what unblocks it.

## Task ID convention
`<AREA>-<NNN>` — areas: `PRE` pre-production, `DES` design, `LVL` level, `NAR` narrative,
`ECO` economy, `UX`, `UI`, `ART`, `ANM` animation, `VFX`, `GPL` gameplay, `AI`, `PHY`
physics/combat, `NET` multiplayer/backend, `BLD` tools/build, `SFX`, `MUS`, `QA`, `BUG`, `PUB`.

## Task card (in `studio/TASKS.md`)

```markdown
### GPL-003 — Player double jump
- **Status:** TESTING
- **Owner:** gameplay-programmer
- **Description:** Add a second jump in mid-air; resets on landing.
- **Depends on:** GPL-001 (player controller), DES-002 (jump metrics)
- **Acceptance criteria:**
  - [x] Second jump only while airborne, once per airtime
  - [x] Height = 80% of first jump (DES-002)
  - [ ] Jump SFX plays on both jumps (SFX-004)
- **Files:** `scripts/player/player.gd` (mod), `tests/test_player_jump.gd` (new)
- **Test status:** unit test passing (`godot --headless -s addons/gut/gut_cmdln.gd` → 12/12); manual: NOT RUN
```

A compact table view at the top of TASKS.md helps for M+:

```markdown
| ID | Title | Owner | Status | Depends | Test |
|---|---|---|---|---|---|
| GPL-001 | Player controller | gameplay-programmer | DONE | PRE-004 | ✅ auto |
| GPL-003 | Double jump | gameplay-programmer | TESTING | GPL-001, DES-002 | ⏳ |
```

## Dependency planning
1. List tasks per discipline from the GDD/TDD.
2. Mark hard dependencies (needs output of) vs soft (better after).
3. Build batches: tasks whose hard dependencies are all DONE form the next parallel batch.
4. Inside a batch, assign **disjoint file ownership**; anything touching a shared file
   (scene root, project settings, input map, autoload list, package.json) is owned by one
   task, others hand off their needs to that owner.
5. Critical path = longest dependency chain; protect it (start it first, don't overload it).

## `studio/PROJECT_STATUS.md`
Template in `templates/PROJECT_STATUS.md`. Update at every phase gate and at the end of
every session of work. It must answer in < 30 seconds: phase, % of MVP done, what runs,
what's broken, what's next, risks, how to run the game.

## `studio/DECISIONS.md` (decision log)
```markdown
## D-007 — Use Godot 4.3 instead of Unity  (2026-03-02)
- **Context:** 2D pixel platformer, desktop + web, no Unity license here.
- **Options:** Godot 4.3 | Unity 6 | Phaser 3
- **Decision:** Godot 4.3 — free, headless CLI export, good 2D.
- **Decided by:** technical-director, approved by coordinator
- **Consequences:** GDScript standards apply; web export needs SharedArrayBuffer headers.
```

## Risk register (in PROJECT_STATUS or TECHNICAL_DESIGN)
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|

## Scope control (MoSCoW)
Executive Producer keeps the MVP list as **Must / Should / Could / Won't (this version)**.
New requests are slotted there; anything that pushes Must items past the deadline is
flagged to the user with options.

## Versioning
- Semver `MAJOR.MINOR.PATCH`: prototype `0.1.0`, alpha `0.5.x`, beta `0.9.x`, release `1.0.0`.
- Patch = fixes only; minor = features/content; major = breaking save/protocol or big relaunch.
- Version lives in one place (engine project settings / package.json) and is read elsewhere.
- Git: commit at each integrated batch with a clear message; tag releases `v1.0.0`.

## Handoff notes
When a specialist's output affects others, the Coordinator writes the relevant facts into
the next task cards (and, for M+, appends a line to `studio/DECISIONS.md` or the task's
notes). Example: "LVL-004 moved the boss arena door to x=1820; AI-002 patrol points and
GPL-010 trigger must be updated."
