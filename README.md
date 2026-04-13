# Lab 8: Random Moving Squares

A Pygame simulation of colored squares that move, flee, age, and respawn.

## What it does

A window opens showing 20 colored squares moving around the screen.
Smaller squares flee from bigger ones when they get too close.
Each square has a random lifespan — when it dies, it bursts into particles
and a new square is spawned 2 seconds later to replace it.

## Features

- 20 squares with random size, color, speed and direction
- Bigger squares move slower than smaller ones
- Jitter: each square slightly rotates its direction over time
- Flee: smaller squares detect and flee from nearby bigger ones
- Wall steering: squares are pushed away from edges before hitting them
- Life span: each square lives between 5 and 20 seconds
- Rebirth: when a square dies, a particle burst appears and a new square spawns 2 seconds later
- Time-based movement: speed is frame-rate independent using dt
- FPS and square count shown on screen

## How to run

1. Install Python 3
2. Install Pygame:
    ```bash
    python3 -m pip install pygame
    ```
3. Run the app:
    ```bash
    python3 main.py
    ```

## Files

- `main.py` — simulation logic and game loop
- `JOURNAL.md` — log of all Copilot interactions
- `prompts_history.md` — prompt history
- `MYNOTES.md` — design thinking and feature notes
- `REPORT.md` — project reflection