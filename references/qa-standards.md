# QA Standards — test planning, bug reporting, verification

## 1. Golden rules
1. **Evidence or it didn't happen.** Every PASS cites a command output, log, screenshot or
   explicit manual step that was actually performed. Anything not executed is **NOT RUN**.
2. Test the **real artifact** for release checks (built EXE/web bundle), not just the editor.
3. Reproduce before reporting; verify after fixing; re-run regression after each fix batch.
4. QA writes tests and reports; QA does not silently fix gameplay code (it opens bugs).

## 2. Severity & priority
| Severity | Meaning | Examples |
|---|---|---|
| **S1 – Blocker** | crash, can't start, progress impossible, data loss, security hole | game won't launch; save wipes; softlock |
| **S2 – Major** | core feature broken or badly wrong, no reasonable workaround | jump doesn't work on gamepad; boss can't be damaged |
| **S3 – Minor** | feature works with issues / workaround exists | wrong SFX; UI overlaps at 4:3 |
| **S4 – Trivial** | cosmetic, typo, polish | 1-px misalignment |

Priority P1 (fix now) – P3 (backlog) is set by Coordinator/Producer. Release rule: no open
S1; S2 only with explicit acceptance by Executive Producer and the user informed.

## 3. Bug report format (`studio/BUGS.md`)
```markdown
### BUG-014 — Player falls through moving platform at high speed
- **Severity:** S2 | **Priority:** P1 | **Status:** OPEN → FIXED → VERIFIED (or REOPENED / WONTFIX)
- **Area/Owner:** physics-combat-programmer
- **Build/Commit:** 0.4.2 / a1b2c3d
- **Environment:** Chromium 1xx headless, 1280×720 | Godot 4.3 Linux
- **Steps:** 1. Start level 2  2. Ride platform P3  3. Dash downward
- **Expected:** player lands on platform
- **Actual:** player passes through, dies
- **Repro rate:** 4/5
- **Evidence:** `qa/screens/bug014.png`, log excerpt
- **Fix notes / verification:** (filled by owner / QA)
```

## 4. Test plan (`studio/QA_REPORT.md` or `tests/README.md`)
For each feature: test cases with ID, preconditions, steps, expected result, type
(auto/manual), result (PASS/FAIL/NOT RUN), evidence.

Coverage categories:
- **Smoke:** launches, main menu, start game, play 60 s, pause, quit — no errors in log.
- **Functional:** each GDD mechanic & acceptance criterion.
- **Gameplay/progression:** win/lose conditions, level completion, difficulty, softlock search.
- **UI/UX:** every button/screen reachable & returns; focus navigation (keyboard/gamepad); text overflow.
- **Input:** keyboard, mouse, gamepad, touch as targeted; rebinding if present.
- **Save/load:** save, quit, reload, continue; corrupt/missing save handling; version migration.
- **Audio:** each event triggers; volume settings persist.
- **Performance:** FPS/frame time in heaviest scene, memory trend over 5+ min, load time.
- **Resolution/aspect:** 1280×720, 1920×1080, 2560×1080 (21:9), 1024×768 (4:3); mobile portrait 390×844 if mobile/web.
- **Compatibility:** target OS/browsers; fullscreen/windowed toggle.
- **Network (multiplayer):** join/leave, latency 100–300 ms, packet loss, host migration/disconnect, cheating attempts (client sending invalid data).
- **Regression:** previously fixed bugs + core smoke after every fix batch.

## 5. Automation by engine
| Engine | Tools |
|---|---|
| Web/HTML5 | Playwright (Chromium preinstalled in this environment): load, collect `console` errors and `pageerror`, simulate input via `page.keyboard`, read state through a dev hook (`window.__game`), screenshots per viewport; `node --test` / Vitest for logic |
| Godot | GUT or GdUnit4 headless; `godot --headless --path . --quit` load check; scripted scene runs with `--quit-after` |
| Unity | Unity Test Framework (EditMode/PlayMode) via `-runTests` |
| Unreal | Automation framework / Functional tests via `-ExecCmds="Automation RunTests"` |
| Roblox | TestEZ / Jest-Lua; Lune for pure modules |
| Python/pygame | pytest; `SDL_VIDEODRIVER=dummy` for headless runs |
| Others | engine CLI + log scan for errors |

Minimal Playwright smoke pattern (web):
```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = [];
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto('http://localhost:8000/');
  await page.waitForTimeout(1000);
  await page.keyboard.press('Enter');            // start
  await page.keyboard.down('ArrowRight'); await page.waitForTimeout(500); await page.keyboard.up('ArrowRight');
  const state = await page.evaluate(() => window.__game && window.__game.getState());
  await page.screenshot({ path: 'qa/screens/smoke_1280x720.png' });
  console.log(JSON.stringify({ errors, state }));
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
```

## 6. Performance measurement
- Web: `performance.now()` frame deltas sampled via the dev hook; report avg/p95 frame time.
- Engines: built-in profilers/monitors (Godot `Performance.get_monitor`, Unity Profiler, UE `stat unit`).
- Report numbers with scene, resolution and machine context; compare to budget in coding-standards §7.

## 7. QA report summary format
```
QA PASS <date> — build <version/commit>
Smoke: PASS | Functional: 18/20 PASS, 2 FAIL | Perf: avg 4.1 ms/frame (budget 16.6) | NOT RUN: gamepad (no device)
Open bugs: S1 0 · S2 1 (BUG-014) · S3 3 · S4 2
Verdict: NOT READY (BUG-014) | READY
```
