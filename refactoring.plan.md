# Overview

This project is a single-file Pygame simulation where squares move with steering behaviors (jitter, flee, chase, separation, wall avoidance), die based on lifespan or overlap, and respawn with particle effects.

The code is functional and already readable, but it has one very large update method, repeated random color logic, a few "magic numbers" in logic, and one potential robustness edge case in particle birth velocity normalization.

# Refactoring Goals

- Improve readability by splitting long logic into small helper functions.
- Improve naming clarity for behavior weights and timers.
- Reduce duplication (especially random color and spawn setup).
- Improve robustness for edge cases while preserving behavior.
- Keep the structure beginner-friendly and close to the original design.

# Step-by-Step Refactoring Plan

## Step 1: Group constants and remove magic numbers

What to do:
- Introduce named constants for values currently embedded in logic (for example `WALL_MARGIN`, `WALL_STRENGTH`, `STEER_BLEND`, and force weights for flee/chase/wall/separation).
- Keep existing constants and place new ones in the same constants section.

Why this helps:
- Named constants make behavior tuning easier and reduce confusion about why a value exists.
- Students can quickly see what is configurable vs. what is algorithm structure.

Inline comment requirement for final code:
- Add short inline comments next to each new constant explaining what changed (moved from hardcoded value) and why (better readability/tuning).

Optional before/after snippet:

```python
# Before
blend: float = 0.35

# After
STEER_BLEND: float = 0.35  # Changed: extracted hardcoded blend value into a named constant for readability.
```

## Step 2: Extract random color creation into one helper

What to do:
- Add a helper function such as `random_bright_color() -> tuple[int, int, int]`.
- Replace repeated color tuple creation in `create_square()` and rebirth logic in `main()` with this helper.

Why this helps:
- Removes duplication and makes intent obvious.
- If color generation rules change later, only one function needs edits.

Inline comment requirement for final code:
- Add one concise comment in the helper saying this centralizes repeated color-generation logic.

Optional before/after snippet:

```python
# Before
color = (
    random.randint(100, 255),
    random.randint(100, 255),
    random.randint(100, 255),
)

# After
color = random_bright_color()  # Changed: replaced duplicated tuple logic with one reusable helper.
```

## Step 3: Split `Square.update()` into small helper methods

What to do:
- Keep `Square.update()` as the orchestrator, but move blocks into helper methods:
  - `_apply_jitter()`
  - `_compute_social_forces(squares)`
  - `_compute_wall_force(screen_w, screen_h)`
  - `_apply_steering(...)`
  - `_move_and_bounce(screen_w, screen_h, dt)`
  - `_anti_stick(screen_w, screen_h)`
- Preserve current behavior and order of operations.

Why this helps:
- Students can understand each concept separately instead of parsing one long method.
- Smaller functions are easier to test and debug.

Inline comment requirement for final code:
- Add one short comment above each helper call in `update()` describing what changed (logic extracted) and why (single responsibility/readability).

Optional before/after snippet:

```python
# Before
# many lines of jitter + force + wall + movement in update()

# After
self._apply_jitter()
flee_x, flee_y, chase_x, chase_y, sep_x, sep_y = self._compute_social_forces(squares)
```

## Step 4: Add a small safety guard in `create_birth_particles()`

What to do:
- Before dividing by `length`, add a guard for the rare case `length == 0`.
- If zero, either skip that particle or assign a tiny fallback direction.

Why this helps:
- Prevents possible division-by-zero crash in edge cases.
- Demonstrates defensive programming for numeric code.

Inline comment requirement for final code:
- Add one concise comment explaining the guard and the programming concept (defensive checks before division).

Optional before/after snippet:

```python
# Before
p.vx = (dx / length) * speed

# After
if length == 0:
    continue  # Changed: defensive guard to avoid division by zero in rare overlap case.
p.vx = (dx / length) * speed
```

## Step 5: Extract rebirth creation into helper function

What to do:
- Create a helper like `spawn_reborn_square(bx, by) -> Square`.
- Move setup logic (`size`, `color`, constructor, `vx/vy`, `age`, `freeze_timer`) from `main()` into that helper.

Why this helps:
- Makes the main loop cleaner and easier to read.
- Rebirth behavior becomes explicit and reusable.

Inline comment requirement for final code:
- Add a brief comment in the helper noting that initialization details were centralized for maintainability.

## Step 6: Lightly improve type hints and naming clarity

What to do:
- Replace broad `list` annotations with more specific forms where practical (for example `list[Square]`).
- Rename very short temporary names where it improves clarity (for example `v` to `velocity_magnitude` in clamping block).
- Keep changes minimal and beginner-friendly; do not redesign data structures.

Why this helps:
- Better type hints support readability and tooling.
- Clear variable names help students reason about math-heavy code.

Inline comment requirement for final code:
- Add short comments where variable renaming happened to explain that meaning was clarified, not behavior changed.

## Step 7: Keep docs aligned with code behavior

What to do:
- Update README to match current constant values (for example current number of squares).
- Verify feature text reflects actual implementation.

Why this helps:
- Prevents confusion when students compare docs to runtime behavior.
- Reinforces that code and documentation should evolve together.

Inline comment requirement for final code:
- No inline code comment needed here (documentation-only step), but mention in commit notes that docs were synchronized with implementation.

# Final Output Requirements (Mandatory)

When this plan is executed, the output MUST:

- Contain only the refactored code.
- Include inline comments that explain:
  - What changed.
  - Why the change improves readability, maintainability, or correctness.
  - Relevant programming concepts (for example single responsibility, defensive programming, avoiding duplication).
- Keep all explanations concise and beginner-friendly.
- Preserve original behavior and game feel as closely as possible.

# Key Concepts for Students

- Single Responsibility Principle: each function should do one clear job.
- DRY (Don’t Repeat Yourself): extract repeated logic into helpers.
- Defensive Programming: check risky assumptions before operations like division.
- Readability over cleverness: clear names and short functions improve maintainability.
- Behavior preservation during refactoring: change structure first, not features.

# Safety Notes

- Refactor in small steps and run the game after each step.
- Avoid changing multiple behaviors at once; isolate structure-only edits first.
- If movement feels different after a change, compare constants and force weights before continuing.
- Keep a backup or use version control checkpoints between major steps.
- Test edge cases: crowded squares, wall contact, and repeated death/rebirth cycles.
