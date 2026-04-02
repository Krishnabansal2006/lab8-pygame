# My Notes - Lab 8 Pygame

## 100 Squares
Changed NUM_SQUARES from 10 to 100. Added MIN_SIZE and MAX_SIZE globals
to control the range of square sizes. Used random.randint(MIN_SIZE, MAX_SIZE)
in create_squares to vary sizes.

## Max Speed Based on Size
Added max_speed attribute to each square calculated as:
max_speed = MAX_SPEED * (MIN_SIZE / size)
This means bigger squares get a lower max speed. A size 10 square gets
full speed, a size 50 square gets 1/5 of max speed.

## Jitter Effect
Added a jitter_timer to each square. Every 30-90 frames, the speed vector
is rotated by a small random angle using math.atan2, math.cos and math.sin.
This keeps the speed magnitude the same but gradually changes direction,
creating smooth curved movement instead of straight lines.

## Questions
- Why does rotating the vector preserve speed? Because rotation is a rigid
  transform - it changes direction but not magnitude.
- Why use atan2 instead of just adding to vx and vy directly? Because atan2
  gives the angle of the vector, which we can rotate cleanly.