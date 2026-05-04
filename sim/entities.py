import math
import random
import pygame
from .config import Color, MAX_SPEED, MIN_SIZE


class Particle:
    """Short-lived visual dot used for death and birth effects."""

    def __init__(self, x: float, y: float, color: Color) -> None:
        self.x: float = x
        self.y: float = y
        self.color: Color = color

        angle: float = random.uniform(0, 2 * math.pi)
        speed: float = random.uniform(80, 200)
        self.vx: float = math.cos(angle) * speed
        self.vy: float = math.sin(angle) * speed

        self.age: float = 0.0
        self.lifespan: float = random.uniform(0.6, 1.2)

    def update(self, dt: float) -> None:
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_dead(self) -> bool:
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        alpha: float = 1.0 - (self.age / self.lifespan)
        radius: int = max(1, int(4 * alpha))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)


class Square:
    """Main simulation entity with state only; movement rules are external."""

    def __init__(self, x: float, y: float, size: int, color: Color) -> None:
        self.x: float = x
        self.y: float = y
        self.size: int = size
        self.color: Color = color

        self.max_speed: float = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed: float = self.max_speed

        self.jitter_timer: int = random.randint(10, 60)
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)
        self.vy: float = self.speed * math.sin(angle)

        self.lifespan: float = random.uniform(20, 60)
        self.age: float = 0.0
        self.freeze_timer: float = 0.0

    def get_rect(self) -> pygame.Rect:
        """Exercise 4: Returns a pygame Rect for collision detection."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def grow(self, amount: int) -> None:
        """Exercise 5: Increase size and update max speed accordingly."""
        self.size += amount
        self.max_speed = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed = self.max_speed

    def split(self) -> "Square":
        """Exercise 6: Splits the square into two."""
        new_size = self.size // 2  # Half the size
        self.size = new_size
        # Update speed for the original square
        self.max_speed = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed = self.max_speed

        # Create the 'child' square at the same position
        return Square(self.x, self.y, new_size, self.color)

    def is_dead(self) -> bool:
        return self.age >= self.lifespan

    def get_predator(self, squares: list["Square"]) -> "Square | None":
        """Exercise 5: Identify if a larger square is eating this one."""
        my_rect = self.get_rect()
        for other in squares:
            if other is self:
                continue
            if other.size > self.size:
                if my_rect.colliderect(other.get_rect()):
                    return other
        return None

    def is_caught(self, squares: list["Square"]) -> bool:
        """Exercise 4/5: Check for predator collision."""
        return self.get_predator(squares) is not None

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            self.get_rect(),
        )
