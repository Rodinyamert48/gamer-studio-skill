# Engine Guidelines — detection, choice, build, run, test, export

Always verify commands against the installed version (`--version`, `--help`) before
relying on them; flags change between releases. If an engine binary is not installed in
this environment, still create a correct project, test what other runtimes allow, and mark
engine-dependent checks **NOT VERIFIED HERE** with exact commands for the user.

## 1. Detection markers

| Engine | Markers |
|---|---|
| Godot 4 / 3 | `project.godot` (`config_version=5` → Godot 4), `*.tscn`, `*.gd`, `export_presets.cfg` |
| Unity | `Assets/`, `ProjectSettings/ProjectVersion.txt`, `Packages/manifest.json`, `*.unity`, `*.cs` |
| Unreal | `*.uproject`, `Config/DefaultEngine.ini`, `Source/`, `Content/*.uasset` |
| Roblox | `default.project.json` (Rojo), `*.rbxl`/`*.rbxlx`, `*.luau`/`*.lua` under `src/`, `wally.toml` |
| GameMaker | `*.yyp`, `objects/`, `rooms/`, `scripts/*.gml` |
| Defold | `game.project`, `*.collection`, `*.script`, `*.gui_script` |
| HTML5 / web | `index.html` + canvas/WebGL, `package.json` with phaser/pixi/three/babylon/kaboom/excalibur, `vite.config.*` |
| Custom / framework | `CMakeLists.txt` + SDL/raylib/SFML, `Cargo.toml` + bevy/macroquad, `main.lua`+`conf.lua` (LÖVE), pygame imports, MonoGame `.csproj` |

## 2. Choosing an engine (when the user didn't)

| Need | Good default | Why |
|---|---|---|
| Small 2D, browser-playable, fastest to verify | HTML5 (vanilla Canvas or Phaser 3) | no install, runs & tests headless with Playwright |
| Simple 3D in browser | Three.js (or Babylon.js) | same verification path |
| Desktop indie 2D/3D, free, scriptable CLI | Godot 4 | headless import/export, small, open source |
| Mobile/console reach, big asset store, C# | Unity | ecosystem; needs editor licence + install |
| High-end 3D, AAA visuals | Unreal 5 | best rendering; heavy toolchain, C++/Blueprints |
| Roblox platform / UGC audience | Roblox Studio (+ Rojo for files) | platform requirement |
| 2D with designer-friendly IDE | GameMaker | user preference/existing project |
| Lightweight cross-platform 2D, Lua | Defold | small builds, good HTML5/mobile |
| Learning / tiny custom tech | pygame, LÖVE, raylib | minimal |

Consider: target platforms, 2D vs 3D, multiplayer needs, user's language skills, licence
cost, and **what can actually be built and tested in the current environment**. The
Technical Director writes the choice + reason in `studio/DECISIONS.md`.

## 3. Per-engine cheat sheets

### Godot 4
- Layout: `scenes/`, `scripts/` (or co-located with scenes), `assets/{sprites,audio,fonts,...}`,
  `autoload/` for singletons, `tests/`. Use `snake_case` files, `PascalCase` node/class names.
- Validate project loads: `godot --headless --path . --quit` (check stderr for `ERROR`/`SCRIPT ERROR`).
- Import resources (4.3+): `godot --headless --path . --import`.
- Script syntax check: `godot --headless --path . --check-only --script res://path.gd`.
- Run a scene: `godot --path . res://scenes/main.tscn` (headless: add `--headless --quit-after 300`).
- Tests: GUT `godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`;
  GdUnit4 `addons/gdUnit4/runtest.sh -a res://tests`.
- Export: needs `export_presets.cfg` + matching export templates:
  `godot --headless --path . --export-release "Windows Desktop" build/windows/Game.exe`
  (also `"Linux"`, `"Web"`, `"Android"`; preset names must match the cfg). Web exports need
  COOP/COEP headers if threads are enabled.
- Gotchas: typed GDScript (`var hp: int`), signals over polling, `@export` for tunables,
  `_physics_process` for movement, `.import` files and `.godot/` are generated (ignore `.godot/` in git).

### Unity
- Layout: `Assets/_Project/{Scripts,Prefabs,Scenes,Art,Audio,UI,Settings}`, asmdefs per module, `Assets/_Project/Tests/{EditMode,PlayMode}`.
- Batch build: `Unity -batchmode -nographics -quit -projectPath . -executeMethod Build.BuildScript.BuildWindows -logFile -`
  (write a static `BuildScript` using `BuildPipeline.BuildPlayer`).
- Tests: `Unity -batchmode -nographics -projectPath . -runTests -testPlatform EditMode -testResults results.xml -logFile -` (no `-quit` with `-runTests`).
- Gotchas: keep `.meta` files in git, Force Text serialization, Input System package, ScriptableObjects for data, avoid `Find*` in Update, pool objects.

### Unreal Engine 5
- Layout: `Source/<Module>/{Public,Private}`, `Content/<Project>/{Characters,Environments,UI,Audio,...}`, `Config/`.
- Build/cook/package: `RunUAT.sh BuildCookRun -project=$PWD/Game.uproject -platform=Win64 -clientconfig=Shipping -build -cook -stage -pak -archive -archivedirectory=$PWD/Build`.
- Tests: `UnrealEditor-Cmd Game.uproject -ExecCmds="Automation RunTests Game; Quit" -unattended -nullrhi -log`.
- Gotchas: binary `.uasset`s can't be authored as text — use C++, Python editor scripting (`unreal` module), data tables (CSV/JSON import), and describe Blueprint steps precisely when needed. Git LFS for content.

### Roblox (Studio + Rojo)
- Layout (Rojo): `src/{server,client,shared}`, `default.project.json`; Luau with `--!strict`.
- Build: `rojo build -o build/game.rbxlx`; live sync `rojo serve`. Lint: `selene src`, format `stylua src`; type check `luau-analyze`.
- Tests: TestEZ / Jest-Lua via `run-in-roblox` or Lune for pure modules.
- Gotchas: server authority — never trust the client; RemoteEvents validated server-side; DataStore with retries & session locking; respect Roblox Community Standards.

### GameMaker
- Layout: `objects/`, `sprites/`, `rooms/`, `scripts/`, `*.yyp`. GML with `snake_case`, constructors/structs for data.
- Build: IDE, or Igor CLI (`Igor ... -project=Game.yyp -- Windows PackageZip`) when runtime installed.
- Gotchas: resource `.yy` JSON files must stay consistent with the `.yyp` resource list — edit carefully or use the IDE.

### Defold
- Layout: `main/`, `game/`, `assets/`, `game.project`. Lua scripts, message passing.
- Build/bundle: `java -jar bob.jar --platform x86_64-win32 --archive resolve build bundle -bo build/`.
- Gotchas: everything communicates via messages (`msg.post`); keep `.collection`/`.go` text files valid.

### HTML5 / Web
- Smallest viable: `index.html` + `src/*.js` (ES modules) + `assets/`. Add Vite only when bundling/TS is needed.
- Libraries: Phaser 3 (2D), PixiJS (2D render), Three.js/Babylon.js (3D), Howler/WebAudio (audio). Pin versions; vendor or use a CDN with exact versions.
- Run: `npx vite` / `python3 -m http.server 8000` (ES modules need http, not `file://`).
- Test: Playwright (Chromium preinstalled here) — load page, assert no console errors, simulate keys, read game state via a debug hook (`window.__game`), take screenshots at several viewport sizes. Unit-test pure logic with `node --test` / Vitest.
- Desktop EXE from web: Electron (`electron-builder --win`), Tauri, or NW.js. Mobile: Capacitor.
- Gotchas: fixed-timestep update loop with `requestAnimationFrame`, `devicePixelRatio` scaling, audio unlock on first user gesture, pause on `visibilitychange`, localStorage try/catch.

### Custom engines / frameworks
- pygame: `python3 main.py`; EXE via `pyinstaller --onefile --windowed main.py`.
- LÖVE: `love .`; distribute `.love` zip (+ fused exe on Windows).
- raylib/SDL2/SFML (C/C++): CMake; `cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build`; cross-compile with MinGW for Windows EXE.
- Bevy/macroquad (Rust): `cargo run`, `cargo build --release`, `--target x86_64-pc-windows-gnu` for EXE.
- MonoGame (C#): `dotnet build -c Release`, `dotnet publish -r win-x64 --self-contained`.

## 4. New or unknown technology
1. Find the official docs/CLI (`--help`, docs site via WebFetch) and the version installed.
2. Identify: project file format, scripting language, run command, headless/test options, export path.
3. Write the findings into `studio/TECHNICAL_DESIGN.md` → "Engine notes" before coding.
4. Prefer text-based, diff-able formats so the studio can author files directly.

## 5. Output platforms
- Windows EXE: Godot export / Unity / UE / pyinstaller / Electron / MinGW. Check the toolchain exists first.
- Web: static folder (zip for itch.io: `index.html` at zip root).
- macOS/iOS builds generally need macOS + signing — mark as not buildable here if on Linux.
- Android: SDK + JDK + keystore; debug keystore OK for testing, never ship it.
