# <Game Title> — Technical Design
> Owner: technical-director · Version 0.1

## 1. Engine & platforms
- Engine + exact version, language(s), target platforms, min specs.
- Decision rationale (link to DECISIONS.md).
- Tooling available in the dev environment / missing tooling.

## 2. Project structure
```
(folder tree with ownership notes)
```

## 3. Architecture
- Scene/entity structure, main systems and their responsibilities.
- Single sources of truth: input map, game state, save, audio, scene loader, settings, event bus.
- System interaction diagram / event list.

## 4. Data
- Data formats (resources/JSON/CSV/ScriptableObjects), who owns which tables.
- Save format (versioned) and migration plan.

## 5. Networking (if any)
Topology, authority model, tick rate, replication, lobby/matchmaking, backend services, security.

## 6. Build, test & release
- Run command, build/export commands per platform, test commands, CI.
- Versioning location.

## 7. Performance budgets
Frame time, memory, draw calls, load time per platform.

## 8. Technical risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|

## 9. Engine notes
Version-specific gotchas discovered during development.
