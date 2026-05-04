## Exercise 4: Collision Implementation in Game Logic

### Logic Integration
The `game_2.py` file acts as the coordinator. By updating the `is_caught` call within `_update_squares`, the game now utilizes the `pygame.Rect` collision logic defined in the `Square` class. 

### Key Adjustments
- **Type Safety**: Updated the `pending_spawns` list throughout the file to ensure the `size` (int) is tracked from death to rebirth.
- **Efficiency**: Instead of calculating distances between every square, we now leverage Pygame's optimized `colliderect` method.