# JavaScript Port Plan (Python Pygame → single-file index.html)

Goal
- Produce a single standalone `index.html` under a new local `web/` directory that reproduces the Python/Pygame simulation behavior using Vanilla JavaScript and the HTML5 Canvas API. The final implementation (when requested) will be a single `index.html` file containing minimal CSS, the `<canvas>` element and a `<script>` block with the ported logic.

High-level constraints (Structural Parity)
- 1-to-1 Mapping: Every Python `class` becomes a JavaScript `class` with the same name (camelCased where appropriate but otherwise identical). Every function and variable name must remain identical where possible (convert to camelCase only when necessary to match JS conventions, but keep recognizable).
- Data structures: Python `list` → JS `Array`; Python `dict` → JS `Object`.
- Control flow & logic: Do not refactor algorithmic logic. Keep method names and signatures aligned with Python originals.
- Simulation loop: Replace Pygame main loop and `pygame.event` with an animation loop driven by `requestAnimationFrame()` and `addEventListener` for input.

Files to inspect (starting point)
- `main.py` (entry point) — follow its data flow exactly.
- `boids_exam.py` — if used by `main.py`, include in inventory.
- `sim/` package: `game.py`, `entities.py`, `behavior.py`, `factories.py`, `config.py` — these likely contain the classes to port.

Plan of Work (draft steps; will execute only after explicit approval)
1) Inventory & Mapping (read-only)
   - List every Python `class`, `function`, global variable, and where each is referenced from `main.py`.
   - Identify drawing or input calls (pygame.draw.*, screen.fill, display.flip, event.get, mouse/keyboard usage).
   - Document dt usage (where `clock.tick()` or time-based movement is applied).

2) Porting rules & code conventions (applied consistently in port)
   - Class mapping: `class Foo:` → `class Foo { constructor(...) { ... } }` and methods preserved.
   - Methods that rely on Python-specific types keep the same names; convert parameter defaults and keyword usage to JS equivalents carefully.
   - Module-level state: export nothing — all code will be embedded in the final `index.html` script block in IIFE scope to avoid global leaks.
   - Data structures: use `[]` for lists and `{}` for dicts; when the Python code assumes ordered iteration, use `Array` methods preserving ordering.

3) Simulation loop & timing
   - Create an animation loop: `function loop(timestamp) { ... requestAnimationFrame(loop); }`.
   - Implement `dt` (delta time) as seconds: `dt = (timestamp - lastTime) / 1000`.
   - Emulate `pygame.time.Clock().tick(fps)` behavior by combining `dt` and `targetFPS` logic if original code clamps dt. If the Python code used `clock.tick(FPS)`, we will use `targetFPS = <same FPS>` and limit updates when dt is too large (cap dt at `1 / targetFPS` or similar) — preserve exact behavior from reading `main.py`.

4) Graphics mapping
   - Map `pygame.display.set_mode`, `screen.fill`, and `pygame.draw` to Canvas API equivalents (ctx.fillRect, ctx.beginPath/arc/fill, ctx.stroke, etc.).
   - Handle colors: convert Python tuples (R,G,B) to CSS `rgb(r,g,b)` strings or use `ctx.fillStyle = 'rgb(..)'`.
   - Preserve draw ordering and layering.
   - Replace `pygame.display.flip()` with a comment `// Equivalent to pygame.display.flip()` and rely on Canvas implicit flip per frame.

5) Input & events
   - Map `pygame.event.get()` mouse/keyboard checks to `window.addEventListener('keydown', ...)`, `canvas.addEventListener('mousemove', ...)`, `mousedown`, `mouseup` as required.
   - If the Python code used relative mouse positions or `pygame.mouse.get_pos()`, read `event.clientX/Y` and convert to canvas coordinates with bounding rect adjustments.

6) Code structure for final `index.html`
   - Minimal CSS: center canvas, set background color to match pygame window clear color.
   - `<canvas id="simCanvas" width=... height=...></canvas>` sized from `config.py` values.
   - `<script>` block with:
     - A small header comment and brief JSDoc on major classes explaining the Pygame equivalents (e.g. `// Equivalent to pygame.display.flip()` above the rendering loop).
     - Ported classes in the same order found in Python files (one-to-one mapping).
     - Initialization code that follows `main.py` sequence exactly: create factories/entities, call any setup functions, start the `requestAnimationFrame` loop.

7) Testing & parity checks (manual)
   - Create a checklist that verifies: same number of entities at startup, movement speeds scaled to match dt behavior, identical draw positions for a static snapshot, and equivalent input responses.

8) Deliverables
   - `web/js-port.md` (this planning file) — created now.
   - When requested: `web/index.html` (single-file port) containing fully ported logic.

Notes and choices that will be followed strictly
- Do not attempt to fix bugs or refactor logic — port must be behavior-preserving.
- Keep names identical; only use camelCase when strictly needed for JS syntax rules (e.g., `__init__` becomes `constructor`). Keep method names readable and traceable to their Python origin.
- Use `performance.now()` timestamps (via `requestAnimationFrame` timestamp argument) for `dt` calculation.

Checklist to include in the plan file (for final verification)
- [ ] All Python `class` definitions have direct JS `class` equivalents.
- [ ] All functions are ported preserving parameter order and default values where possible.
- [ ] `list` → `Array`, `dict` → `Object` conversions verified.
- [ ] `dt` computed and clamped to match original `clock.tick()` semantics.
- [ ] Canvas drawing matches `pygame.draw.*` calls.
- [ ] Input events mapped and tested for parity.

Estimated effort (rough)
- Inventory & mapping: 1–2 hours
- Port core classes & loop: 2–4 hours
- Graphics & input mapping + iterative tuning: 2–3 hours
- Final single-file consolidation & polish: 1 hour

Next action (waiting your OK)
- After you approve this plan, I will perform the inventory step and then begin porting into a single `web/index.html` file. Do you want me to start now?
