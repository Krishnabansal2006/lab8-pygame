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


# Fleeing Feature - My Thinking

## What needs to happen
- Smaller squares need to detect nearby bigger squares
- When a bigger square is close, the smaller one should move away from it
- Squares should still keep some randomness in their movement

## How to detect "nearby"
- Calculate distance between two squares using their x, y positions
- Distance formula: sqrt((x2-x1)² + (y2-y1)²)
- If distance is less than a threshold, the small square should flee

## How to flee
- Calculate the direction FROM the big square TO the small square
- Move the small square in that direction
- Keep some jitter so it doesn't look robotic

## Edge cases
- What if multiple big squares are nearby? Average the flee directions
- What if the square is cornered? It should still try to move away


# Life Span + Rebirth - My Thinking

## What needs to happen
- Each square has a random life span (between 30 and 180 seconds)
- When a square reaches the end of its life, it dies
- A new square is created to replace it

## How to implement
- Add a `lifespan` attribute to Square (random between 30 and 180)
- Add an `age` attribute starting at 0
- Each frame, increase age by dt
- When age >= lifespan, the square is dead
- In main loop, check for dead squares and replace them

## Life Span + Rebirth - Design Decisions

- Particles: 10 small dots at the dead square's location
- Particles keep the dying square's color
- 2 second delay per dead square (independent timers)

### Data structures needed
- squares: list of alive Square objects
- particles: list of small visual dots (short life 0.5s)
- pending_spawns: list of floats (timestamps when to spawn new square)


## Chase Feature - My Thinking

### What needs to happen
- Bigger squares should chase smaller ones
- Smaller squares still flee from bigger ones
- All squares keep some random wandering movement

### How to implement
- In update(), bigger squares need to detect nearby smaller squares
- Calculate direction FROM bigger square TOWARD smaller square
- Steer toward the closest smaller square
- Keep jitter so it doesn't look robotic

### Reusing existing code
- The flee logic already calculates dx, dy, dist between squares
- Instead of steering AWAY (flee), steer TOWARD (chase)
- Same distance weighting can be used