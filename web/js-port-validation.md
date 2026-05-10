# JavaScript Port Validation

This document validates the planned JavaScript port against the current Pygame implementation. It is based on `main.py` and the `sim/` package and is intended to confirm structural parity before any HTML implementation is written.

## Validation goals
- Preserve the original class/function structure.
- Keep the runtime flow aligned with the current Pygame game loop.
- Map drawing, input, timing, and state updates to Canvas/JavaScript equivalents.
- Avoid refactoring or behavior changes during the port.

## Side-by-side mapping table

| Original Pygame / Python | Planned JavaScript / Canvas equivalent | Validation notes |
| --- | --- | --- |
| `main.main()` in `main.py` | `main()` or startup wrapper in JS | Thin entry point only; calls `run_game()`.
| `run_game()` in `sim/game.py` | `run_game()` driven by `requestAnimationFrame()` | Main game loop stays centralized.
| `pygame.init()` | Browser page load / canvas setup | No direct API call; setup happens in startup code.
| `pygame.display.set_mode((WIDTH, HEIGHT))` | `<canvas id="simCanvas" width height>` and `canvas.getContext('2d')` | Canvas size comes from `sim/config.py` constants.
| `pygame.display.set_caption("Random Squares")` | `<title>` element or optional DOM text | Browser title replaces window caption.
| `clock.tick(FPS)` | `requestAnimationFrame(timestamp)` + computed `dt` | `dt` is expressed in seconds.
| `clock.get_fps()` | FPS estimate from frame timing (`1 / dt`) | Used for HUD display.
| `pygame.event.get()` | `window.addEventListener(...)` / canvas event listeners | Keyboard and mouse input are handled through browser events.
| `pygame.QUIT` | Browser stop flag / unload behavior | The loop stops via a JS flag, not a Pygame quit event.
| `screen.fill(BG_COLOR)` | `ctx.fillStyle = ...; ctx.fillRect(0, 0, WIDTH, HEIGHT)` | Canvas clear step each frame.
| `pygame.display.flip()` | Canvas redraw on each animation frame | The canvas is redrawn every frame; no explicit flip call exists.
| `pygame.draw.rect(surface, color, rect)` | `ctx.fillRect(x, y, w, h)` or `ctx.strokeRect(x, y, w, h)` | Filled vs outlined rectangles depend on draw purpose.
| `pygame.draw.circle(surface, color, pos, radius)` | `ctx.beginPath(); ctx.arc(...); ctx.fill()` | Used for particle rendering.
| `surface.blit(text_surface, pos)` | `ctx.fillText(text, x, y)` | HUD text is drawn directly onto the canvas.
| `pygame.Rect(...)` | Plain JS object such as `{ x, y, w, h }` | Collision helper will use object fields.
| `rect.colliderect(other_rect)` | JS rectangle intersection helper | Same collision semantics, different implementation.
| `Particle.update(dt)` | `Particle.update(dt)` | Same method name and purpose.
| `Particle.is_dead()` | `Particle.is_dead()` | Same boolean behavior.
| `Particle.draw(surface)` | `Particle.draw(ctx)` | Only the rendering target changes.
| `Square.__init__(...)` | `Square.constructor(x, y, size, color)` | Same state setup, JS constructor syntax.
| `Square.get_rect()` | `Square.get_rect()` | Returns a JS rectangle object instead of `pygame.Rect`.
| `Square.grow(amount)` | `Square.grow(amount)` | Same size and speed update logic.
| `Square.split()` | `Square.split()` | Returns a new `Square` instance.
| `Square.is_dead()` | `Square.is_dead()` | Same age/lifespan check.
| `Square.get_predator(squares)` | `Square.get_predator(squares)` | Uses JS collision helper instead of `colliderect`.
| `Square.is_caught(squares)` | `Square.is_caught(squares)` | Same logical check.
| `Square.draw(surface)` | `Square.draw(ctx)` | Trail and square rendering mapped to Canvas.
| `apply_jitter(square)` | `apply_jitter(square)` | Same timer-driven steering adjustment.
| `compute_social_forces(square, squares)` | `compute_social_forces(square, squares)` | Same six-force output, likely as array values.
| `compute_wall_force(square, screen_w, screen_h)` | `compute_wall_force(square, screen_w, screen_h)` | Same boundary force logic.
| `apply_steering(square, steer_x, steer_y)` | `apply_steering(square, steer_x, steer_y)` | Same steering blend behavior.
| `clamp_speed(square)` | `clamp_speed(square)` | Same max-speed enforcement.
| `move_and_wrap(square, screen_w, screen_h, dt)` | `move_and_wrap(square, screen_w, screen_h, dt)` | Same motion and wrap behavior.
| `anti_stick(square, screen_w, screen_h)` | `anti_stick(square, screen_w, screen_h)` | Same edge-sticking safeguard.
| `update_square(square, screen_w, screen_h, squares, dt)` | `update_square(square, screen_w, screen_h, squares, dt)` | Orchestrator remains the same.
| `random_bright_color()` | `random_bright_color()` | Returns a JS RGB array like `[r, g, b]`.
| `create_square(screen_w, screen_h)` | `create_square(screen_w, screen_h)` | Same random-size square creation.
| `create_squares(count, screen_w, screen_h)` | `create_squares(count, screen_w, screen_h)` | JS array creation mirrors Python list creation.
| `create_death_particles(x, y, color)` | `create_death_particles(x, y, color)` | Same particle burst creation.
| `create_birth_particles(x, y, color)` | `create_birth_particles(x, y, color)` | Same respawn burst creation.
| `spawn_reborn_square(birth_x, birth_y, original_size)` | `spawn_reborn_square(birth_x, birth_y, original_size)` | Same centered rebirth setup.
| `_update_squares(...)` | `_update_squares(...)` | Same update, death, growth, and split flow.
| `_process_rebirths(...)` | `_process_rebirths(...)` | Same delayed respawn handling.
| `_draw_hud(...)` | `_draw_hud(ctx, fps, square_count)` | Text drawing only changes target API.

## Data structure validation

| Python structure | JavaScript structure | Reason |
| --- | --- | --- |
| `tuple[int, int, int]` for `Color` | `[r, g, b]` array | Easier direct mapping to Canvas color strings.
| `list[Square]` | `Square[]` | Ordered entity collection stays ordered.
| `list[Particle]` | `Particle[]` | Ordered particle collection stays ordered.
| `list[tuple[float, float, float, int]]` for pending spawns | Array of arrays | Preserves positional unpacking in the same order.
| `pygame.Rect` | Plain object `{ x, y, w, h }` | Lightweight collision representation in JS.
| `list[tuple[float, float]]` for trail | Array of `[x, y]` pairs | Matches the original ordered trail history.

## Timing and loop validation
- `dt` should be computed from the `requestAnimationFrame()` timestamp in seconds.
- The JS loop should preserve the same update order as the Pygame loop:
  1. compute `dt`
  2. update square state
  3. process deaths and rebirths
  4. draw squares
  5. draw particles
  6. draw HUD
  7. continue animation
- `FPS` remains a target constant for timing and display, not a hard `clock.tick()` call.

## Input validation
- Keyboard input should use browser events, most likely `keydown`.
- Quit behavior should be represented by a stop flag rather than `pygame.QUIT`.
- If mouse input is added later, it should use Canvas-relative coordinates.

## Behavioral equivalence checklist
- [ ] `main()` still starts the simulation through `run_game()`.
- [ ] Every class in `sim/entities.py` has a direct JS class equivalent.
- [ ] Every function in `sim/behavior.py`, `sim/factories.py`, and `sim/game.py` has a JS function equivalent.
- [ ] Canvas drawing replaces Pygame draw calls one-for-one.
- [ ] `dt` is derived from animation frame timing.
- [ ] Lists, tuples, and rectangle objects are mapped to arrays/objects consistently.
- [ ] No bug fixes or logic improvements are introduced during porting.
- [ ] The planning document remains separate from the final HTML implementation.

## Port readiness conclusion
- The current Pygame code is structurally ready for a direct JavaScript port.
- The main implementation risk is preserving the exact timing feel when converting `clock.tick(FPS)` to `requestAnimationFrame()`.
- The next step after this validation document would be to generate `web/index.html`.
