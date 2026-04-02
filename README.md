# Lab 8: Random Squares

This project is a small Pygame animation that fills the window with moving colored squares. Each square starts with a random size, position, color, and direction, then bounces around the screen while occasionally changing direction a little to feel less rigid.

## What it does

When you run the app, a Pygame window opens and animates a field of squares at 60 FPS. The squares move continuously, bounce off the window edges, and keep updating until you close the window.

## How to run it

1. Make sure Python 3 is installed.
2. Install Pygame if you do not already have it:

	```bash
	python -m pip install pygame
	```

3. Start the app from the project root:

	```bash
	python main.py
	```

## Features implemented so far

- Opens an `800 x 600` Pygame window.
- Spawns `100` squares at random positions.
- Gives each square a random size between `10` and `50` pixels.
- Assigns each square a random color.
- Moves squares in random initial directions.
- Applies occasional jitter so movement changes slightly over time.
- Bounces squares off all four window edges.
- Renders the animation at `60 FPS`.

## Main files

- `main.py`: the full animation and game loop.
- `JOURNAL.md`: chronological log of changes made during the project.
