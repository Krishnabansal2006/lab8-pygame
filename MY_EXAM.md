## Exercise 4: Collision Implementation in Game Logic

### Logic Integration
The `game_2.py` file acts as the coordinator. By updating the `is_caught` call within `_update_squares`, the game now utilizes the `pygame.Rect` collision logic defined in the `Square` class. 

### Key Adjustments
- **Type Safety**: Updated the `pending_spawns` list throughout the file to ensure the `size` (int) is tracked from death to rebirth.
- **Efficiency**: Instead of calculating distances between every square, we now leverage Pygame's optimized `colliderect` method.


## Exercise 6: Splitting Logic Thinking

### Goal
Prevent a single square from dominating the screen by splitting it when it becomes too large.

### Implementation Strategy
1. **Size Threshold**: I set a maximum size limit of 30 pixels. Once a predator reaches or exceeds this size after eating, the split logic triggers.
2. **Method**: The `split()` method in the `Square` class reduces the parent square's size by half and returns a new square instance with that same half-size.
3. **Conservation**: Both resulting squares have their speeds recalculated based on their new smaller size, making them faster again.

### Verification
- I observed that large squares no longer grow past 30 pixels; instead, they immediately turn into two smaller squares.

- This maintains the total "square population" count properly because the prey dies but the predator splits, resulting in a net population change that keeps the simulation dynamic.