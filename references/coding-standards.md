# Coding Standards — all studio programmers

## 1. Principles
1. **Read before writing.** Search for an existing system (`Grep` for class names, signals,
   managers) before adding one. Extend, don't duplicate.
2. **Follow the project's existing style** over this document when they differ.
3. **Small, cohesive modules** with one responsibility; explicit dependencies.
4. **Data-driven tuning.** Gameplay numbers live in data (exported vars, ScriptableObjects,
   JSON/CSV/Resource files), not magic numbers scattered in code — designers own the values.
5. **Deterministic, testable core.** Keep pure logic (damage formulas, inventory, economy,
   save serialization, state machines) separate from engine glue so it can be unit tested.
6. **Fail loudly in dev, gracefully in release.** Assertions/logs for invalid state; no silent `catch {}`.
7. **No dead code, no commented-out blocks, no TODO without a task ID** (`# TODO(GPL-012): ...`).

## 2. Architecture patterns (pick what fits; don't over-engineer S-tier)
- **Scene/entity composition**: components over deep inheritance.
- **State machines** for player, enemies, game flow (`Boot → Menu → Playing → Paused → GameOver`).
- **Event bus / signals** for cross-system communication (UI listens to gameplay events; gameplay never reaches into UI).
- **Single sources of truth (one each):** input map, game state/session, save system, audio
  manager, scene loader, settings, localisation table, event bus.
- **Object pooling** for bullets/particles/enemies spawned frequently.
- **Fixed timestep** for physics/gameplay simulation; render interpolation if needed.
- **Service/autoload singletons** only for truly global services; pass dependencies otherwise.

## 3. Naming
| Thing | Convention |
|---|---|
| Files (Godot/web/Python/Lua) | `snake_case` (`player_controller.gd`, `enemy_spawner.js`) |
| Files (Unity C#/UE C++) | `PascalCase` matching class (`PlayerController.cs`) |
| Classes/types | `PascalCase` |
| Functions/variables | engine idiom: GDScript/Python/Lua `snake_case`; C#/JS/TS `camelCase` methods/vars (C# public members `PascalCase`) |
| Constants | `UPPER_SNAKE_CASE` |
| Signals/events | past tense: `died`, `health_changed`, `onLevelCompleted` |
| Booleans | `is_`, `has_`, `can_` prefixes |

## 4. Engine idioms
- **GDScript (Godot 4):** static typing everywhere; `@export` tunables; `@onready` node refs;
  signals for decoupling; `_physics_process` for movement; avoid `get_node` with long
  absolute paths; groups for categories; `class_name` for reusable types.
- **C# (Unity):** `[SerializeField] private` over public fields; cache components in
  `Awake`; no `GameObject.Find`/`GetComponent` in `Update`; asmdefs; ScriptableObjects for
  data; new Input System; `async`/coroutines consistently, not mixed randomly.
- **C++ (Unreal):** UE naming prefixes (`A`, `U`, `F`, `E`, `I`, `b` for bools); `UPROPERTY`/
  `UFUNCTION` for exposure; Gameplay Ability System only when justified; avoid ticking actors unnecessarily.
- **Luau (Roblox):** `--!strict`; ModuleScripts; server-authoritative; validate every RemoteEvent argument; no yielding in hot loops.
- **JS/TS (web):** ES modules; no globals except a deliberate debug hook (`window.__game` in dev);
  `requestAnimationFrame` + fixed-step accumulator; clean up listeners; prefer TS for M+ projects.
- **Lua (Defold/LÖVE), GML, Python:** follow the same separation of logic and engine glue.

## 5. Input
- Map **actions**, not keys (`jump`, `attack`, `pause`). One input map. Support keyboard +
  gamepad for desktop when reasonable; touch for mobile. Allow rebinding at M+ if feasible.
- Input buffering & coyote time for platformers; dead zones for sticks.

## 6. Save / persistence
- Versioned save format (`{ "version": 2, ... }`) + migration for old versions.
- Write atomically (temp file → rename) where the platform allows; handle missing/corrupt saves.
- Never store secrets in client saves; online data is server-authoritative.

## 7. Performance rules
- Measure before optimising; record before/after numbers.
- No allocations in per-frame hot paths where avoidable (pool, reuse arrays/vectors).
- Avoid per-frame searches (`find`, `get_nodes_in_group` every frame) — cache.
- Throttle AI/pathfinding updates; use spatial partitioning for many entities.
- Budgets (default, adjust per target): 60 FPS (16.6 ms) desktop/web, 30–60 mobile; load < 5 s for small games.

## 8. Error handling & logging
- Central logger with levels; tag by system (`[AI]`, `[NET]`). Strip verbose logs in release.
- Validate external data (level files, saves, network messages) at the boundary.

## 9. Testing (programmer responsibility before handing to QA)
- Unit tests for pure logic (formulas, inventory, economy, save serialization, state transitions).
- A smoke run: project loads/builds, main scene starts, no errors in the log.
- Test frameworks: Godot GUT/GdUnit4, Unity Test Framework, UE Automation, TestEZ/Jest-Lua,
  `node --test`/Vitest + Playwright for web, pytest for Python.
- Report exact commands and results in the Studio Protocol report.

## 10. Version control
- Commit integrated, working increments; messages `area: change` (e.g. `gameplay: add double jump (GPL-003)`).
- `.gitignore` per engine (Godot `.godot/`, Unity `Library/ Temp/ Logs/ obj/`, UE `Binaries/ Intermediate/ Saved/ DerivedDataCache/`, web `node_modules/ dist/`).
- Large binary assets → Git LFS when the project uses it.

## 11. Code review checklist (Technical Director / Coordinator)
- [ ] Builds/loads without errors or new warnings
- [ ] No duplicate system; uses existing managers/APIs
- [ ] Tunables exposed as data; no unexplained magic numbers
- [ ] No per-frame allocations/searches in hot paths
- [ ] Errors handled at boundaries; no swallowed exceptions
- [ ] Tests added/updated for pure logic; results reported
- [ ] File ownership respected; shared files changed minimally and reported
