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

        self.jitter_timer: int = random.randint(20, 60)
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)
        self.vy: float = self.speed * math.sin(angle)

        self.lifespan: float = random.uniform(5, 20)
        self.age: float = 0.0
        self.freeze_timer: float = 0.0

    def is_dead(self) -> bool:
        return self.age >= self.lifespan

    def is_caught(self, squares: list["Square"]) -> bool:
        cx1: float = self.x + self.size / 2
        cy1: float = self.y + self.size / 2

        for other in squares:
            if other is self:
                continue
            if other.size > self.size:
                cx2: float = other.x + other.size / 2
                cy2: float = other.y + other.size / 2
                dist: float = math.hypot(cx1 - cx2, cy1 - cy2)
                if dist < (self.size + other.size) / 2:
                    return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )
