import math
import random

from .config import (
    BIRTH_PARTICLE_COUNT,
    DEATH_PARTICLE_COUNT,
    MAX_SIZE,
    MIN_SIZE,
    REBIRTH_FREEZE_SECONDS,
)
from .config import Color
from .entities import Particle, Square


def random_bright_color() -> Color:
    return (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255),
    )


def create_square(screen_w: int, screen_h: int) -> Square:
    size: int = random.randint(MIN_SIZE, MAX_SIZE)
    x: float = random.uniform(0, screen_w - size)
    y: float = random.uniform(0, screen_h - size)
    return Square(x, y, size, random_bright_color())


def create_squares(count: int, screen_w: int, screen_h: int) -> list[Square]:
    return [create_square(screen_w, screen_h) for _ in range(count)]


def create_death_particles(x: float, y: float, color: Color) -> list[Particle]:
    return [Particle(x, y, color) for _ in range(DEATH_PARTICLE_COUNT)]


def create_birth_particles(x: float, y: float, color: Color) -> list[Particle]:
    particles: list[Particle] = []
    for _ in range(BIRTH_PARTICLE_COUNT):
        angle: float = random.uniform(0, 2 * math.pi)
        distance: float = random.uniform(50, 150)
        start_x: float = x + math.cos(angle) * distance
        start_y: float = y + math.sin(angle) * distance

        particle: Particle = Particle(start_x, start_y, color)
        speed: float = random.uniform(80, 200)
        dx: float = x - start_x
        dy: float = y - start_y
        length: float = math.hypot(dx, dy)

        # Defensive programming: avoid dividing by zero for degenerate vectors.
        if length == 0:
            continue

        particle.vx = (dx / length) * speed
        particle.vy = (dy / length) * speed
        particles.append(particle)

    return particles


def spawn_reborn_square(birth_x: float, birth_y: float) -> Square:
    size: int = random.randint(MIN_SIZE, MAX_SIZE)
    color: Color = random_bright_color()
    square: Square = Square(birth_x - size / 2, birth_y - size / 2, size, color)
    square.vx = 0.0
    square.vy = 0.0
    square.age = 0.0
    square.freeze_timer = REBIRTH_FREEZE_SECONDS
    return square


def create_fixed_square(screen_w: int, screen_h: int, size: int) -> Square:
    """Exercise 1: Creates a square with a specific fixed size."""
    x: float = random.uniform(0, screen_w - size)
    y: float = random.uniform(0, screen_h - size)
    return Square(x, y, size, random_bright_color())
