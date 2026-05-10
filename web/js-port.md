# JavaScript Port Plan

Project goal
- Port the Pygame simulation in this repository to a standalone JavaScript + HTML5 Canvas implementation later, while preserving the original structure and logic flow.
- This document is the planning step only. No HTML is written yet.

Porting rules
- Keep a 1-to-1 structural mapping wherever possible.
- Python classes become JavaScript classes.
- Python functions become JavaScript functions with the same purpose and closely matching names.
- Python lists become JavaScript arrays.
- Python tuples become JavaScript arrays or fixed arrays.
- Python dictionaries would become JavaScript objects, if any are introduced later.
- The Pygame event loop will later map to requestAnimationFrame() with delta time.
- Drawing calls such as pygame.draw.rect(), pygame.draw.circle(), screen.fill(), and pygame.display.flip() will later map to Canvas API calls.
- Do not refactor logic in the port plan. Preserve the existing structure.

## File inventory and JavaScript equivalents

### 1) main.py

#### `main()`
- Python purpose: Thin entry point that calls `run_game()`.
- JavaScript equivalent: `main()` or a startup function that calls `run_game()` once the page loads.
- Notes: In the final web version, this will usually be a single startup call near the bottom of the script.

### 2) sim/config.py

This module contains constants only, not classes or functions.

#### Constants to carry into JavaScript
- `Color` -> a documentation-only type alias in JavaScript comments or JSDoc.
- `WIDTH` -> JS constant used for canvas width.
- `HEIGHT` -> JS constant used for canvas height.
- `FPS` -> JS constant used for frame pacing.
- `NUM_SQUARES` -> JS constant for the number of starting squares.
- `BG_COLOR` -> JS constant used for clear color.
- `MIN_SIZE` -> JS constant for square size bounds.
- `MAX_SIZE` -> JS constant for square size bounds.
- `MAX_SPEED` -> JS constant for speed scaling.
- `FLEE_RADIUS` -> JS constant for flee behavior.
- `CHASE_RADIUS` -> JS constant for chase behavior.
- `SEP_RADIUS` -> JS constant for separation behavior.
- `FLEE_WEIGHT` -> JS constant for steering blend.
- `CHASE_WEIGHT` -> JS constant for steering blend.
- `WALL_WEIGHT` -> JS constant for steering blend.
- `SEPARATION_WEIGHT` -> JS constant for steering blend.
- `STEER_BLEND` -> JS constant for steering interpolation.
- `WALL_MARGIN` -> JS constant for wall-force distance.
- `WALL_STRENGTH` -> JS constant for wall-force intensity.
- `DEATH_PARTICLE_COUNT` -> JS constant for death effect count.
- `BIRTH_PARTICLE_COUNT` -> JS constant for birth effect count.
- `REBIRTH_DELAY_SECONDS` -> JS constant for respawn delay.
- `REBIRTH_FREEZE_SECONDS` -> JS constant for newly spawned square freeze time.
- `TEST_MODE_ON` -> JS constant if the testing flag is ported later.
- `GROWTH_DURATION` -> JS constant if the animated growth feature is ported later.

### 3) sim/entities.py

#### `class Particle`
- Python purpose: Short-lived visual particle for death and birth effects.
- JavaScript equivalent: `class Particle`.
- Constructor equivalent: `constructor(x, y, color)`.
- Method mapping:
  - `update(dt)` -> `update(dt)`
  - `is_dead()` -> `is_dead()`
  - `draw(surface)` -> `draw(ctx)`
- Canvas notes:
  - `pygame.draw.circle()` -> `ctx.arc()` plus `ctx.fill()`.
  - `surface` becomes `ctx` from the canvas.

#### `class Square`
- Python purpose: Main simulation entity storing position, velocity, size, color, timers, and trail state.
- JavaScript equivalent: `class Square`.
- Constructor equivalent: `constructor(x, y, size, color)`.
- Method mapping:
  - `get_rect()` -> `get_rect()` returning a plain JS object like `{ x, y, w, h }`
  - `grow(amount)` -> `grow(amount)`
  - `split()` -> `split()`
  - `is_dead()` -> `is_dead()`
  - `get_predator(squares)` -> `get_predator(squares)`
  - `is_caught(squares)` -> `is_caught(squares)`
  - `draw(surface)` -> `draw(ctx)`
- Canvas notes:
  - `pygame.Rect` collision logic will later become a small JS rectangle-intersection helper.
  - `pygame.draw.rect()` -> `ctx.strokeRect()` for trail outlines and `ctx.fillRect()` for the main square.
- Data notes:
  - `trail` remains a JavaScript array of position pairs.
  - `max_trail_length` remains a numeric property.

### 4) sim/behavior.py

#### `apply_jitter(square)`
- Python purpose: Randomly changes the heading of a square after a timer expires.
- JavaScript equivalent: `apply_jitter(square)`.

#### `compute_social_forces(square, squares)`
- Python purpose: Computes flee, chase, and separation steering components.
- JavaScript equivalent: `compute_social_forces(square, squares)`.
- Return shape in JS: an array of six numbers, or an object if that is clearer later.

#### `compute_wall_force(square, screen_w, screen_h)`
- Python purpose: Computes steering force near screen boundaries.
- JavaScript equivalent: `compute_wall_force(square, screen_w, screen_h)`.

#### `apply_steering(square, steer_x, steer_y)`
- Python purpose: Blends steering into velocity using `STEER_BLEND`.
- JavaScript equivalent: `apply_steering(square, steer_x, steer_y)`.

#### `clamp_speed(square)`
- Python purpose: Prevents velocity from exceeding the square's current speed.
- JavaScript equivalent: `clamp_speed(square)`.

#### `move_and_wrap(square, screen_w, screen_h, dt)`
- Python purpose: Moves the square, records trail positions, and wraps at edges.
- JavaScript equivalent: `move_and_wrap(square, screen_w, screen_h, dt)`.
- Canvas notes:
  - Trail storage becomes a JavaScript array of point pairs.

#### `anti_stick(square, screen_w, screen_h)`
- Python purpose: Removes edge sticking by zeroing velocity in corner cases.
- JavaScript equivalent: `anti_stick(square, screen_w, screen_h)`.

#### `update_square(square, screen_w, screen_h, squares, dt)`
- Python purpose: Orchestrates timer updates, jitter, steering, movement, wrapping, and anti-stick handling.
- JavaScript equivalent: `update_square(square, screen_w, screen_h, squares, dt)`.

### 5) sim/factories.py

#### `random_bright_color()`
- Python purpose: Creates a bright RGB color tuple.
- JavaScript equivalent: `random_bright_color()` returning a JS RGB array such as `[r, g, b]`.

#### `create_square(screen_w, screen_h)`
- Python purpose: Creates a square with a random size and random color.
- JavaScript equivalent: `create_square(screen_w, screen_h)`.

#### `create_squares(count, screen_w, screen_h)`
- Python purpose: Creates a list of squares with the given count.
- JavaScript equivalent: `create_squares(count, screen_w, screen_h)`.

#### `create_death_particles(x, y, color)`
- Python purpose: Creates particles for the death effect.
- JavaScript equivalent: `create_death_particles(x, y, color)`.

#### `create_birth_particles(x, y, color)`
- Python purpose: Creates particles for the birth effect.
- JavaScript equivalent: `create_birth_particles(x, y, color)`.

#### `spawn_reborn_square(birth_x, birth_y, original_size)`
- Python purpose: Creates a square that respawns after a delay, centered on the death position.
- JavaScript equivalent: `spawn_reborn_square(birth_x, birth_y, original_size)`.

#### `create_fixed_square(screen_w, screen_h, size)`
- Python purpose: Creates a square with a fixed requested size.
- JavaScript equivalent: `create_fixed_square(screen_w, screen_h, size)`.

### 6) sim/game.py

#### `_update_squares(squares, particles, pending_spawns, current_time, dt)`
- Python purpose: Updates every square, handles death, growth, splitting, particle effects, and respawn scheduling.
- JavaScript equivalent: `_update_squares(squares, particles, pending_spawns, current_time, dt)`.
- Return shape in JS: an array of surviving squares, with any newly split squares appended.

#### `_process_rebirths(squares, particles, pending_spawns, current_time)`
- Python purpose: Spawns any squares whose rebirth timer has elapsed.
- JavaScript equivalent: `_process_rebirths(squares, particles, pending_spawns, current_time)`.
- Return shape in JS: a filtered array of still-pending respawn entries.

#### `_draw_hud(screen, font, clock, square_count)`
- Python purpose: Draws FPS and square count text on the screen.
- JavaScript equivalent: `_draw_hud(ctx, fps, square_count)`.
- Canvas notes:
  - `font.render()` and `screen.blit()` become `ctx.fillText()`.
  - `clock.get_fps()` becomes a JS FPS estimate from frame timing.

#### `run_game()`
- Python purpose: Sets up Pygame, creates the initial squares, runs the main loop, processes events, updates simulation state, draws everything, and flips the display.
- JavaScript equivalent: `run_game()` driven by `requestAnimationFrame()`.
- Event mapping:
  - `pygame.event.get()` -> `window.addEventListener(...)` or canvas event listeners.
  - `pygame.QUIT` -> a JavaScript stop flag and page event handling.
- Timing mapping:
  - `clock.tick(FPS)` -> `requestAnimationFrame(timestamp)` plus `dt` in seconds.
- Rendering mapping:
  - `screen.fill(BG_COLOR)` -> `ctx.fillRect(0, 0, WIDTH, HEIGHT)` after setting fill style.
  - `pygame.display.flip()` -> Canvas redraw on each frame.

## Implementation order for the later HTML port
1. Define constants from `sim/config.py`.
2. Port `Particle` and `Square` from `sim/entities.py`.
3. Port all behavior helpers from `sim/behavior.py`.
4. Port all factory helpers from `sim/factories.py`.
5. Port the game-loop helpers and `run_game()` from `sim/game.py`.
6. Call `run_game()` from the JS startup code.

## JavaScript data-shape decisions
- Colors: keep as `[r, g, b]` arrays.
- Rectangles: keep as plain objects like `{ x, y, w, h }`.
- Trails: keep as arrays of `[x, y]` pairs.
- Pending spawns: keep as arrays of tuples-like arrays, for example `[spawnTime, birthX, birthY, originalSize]`.

## Notes on parity
- The port will preserve the current structure rather than improving it.
- The same startup sequence will be used: initialize simulation state, create the starting squares, then enter the frame loop.
- No HTML, CSS, or canvas implementation is written at this stage.

## Checklist for the later implementation
- [ ] `main()` has a direct startup equivalent in JavaScript.
- [ ] Every class in `sim/entities.py` has a JavaScript class equivalent.
- [ ] Every function in `sim/behavior.py`, `sim/factories.py`, and `sim/game.py` has a JavaScript function equivalent.
- [ ] Configuration constants from `sim/config.py` are preserved in JavaScript.
- [ ] Pygame drawing calls are mapped to Canvas API calls.
- [ ] The main loop uses `requestAnimationFrame()` and `dt`.
- [ ] No refactoring is introduced during the port.
