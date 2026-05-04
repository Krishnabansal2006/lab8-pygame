import math
import random

from .config import (
    CHASE_RADIUS,
    CHASE_WEIGHT,
    FLEE_RADIUS,
    FLEE_WEIGHT,
    SEPARATION_WEIGHT,
    SEP_RADIUS,
    STEER_BLEND,
    WALL_MARGIN,
    WALL_STRENGTH,
    WALL_WEIGHT,
)
from .entities import Square


def apply_jitter(square: Square) -> None:
    square.jitter_timer -= 1
    if square.jitter_timer <= 0:
        angle: float = math.atan2(square.vy, square.vx) + random.uniform(-0.1, 0.1)
        square.vx = square.speed * math.cos(angle)
        square.vy = square.speed * math.sin(angle)
        square.jitter_timer = random.randint(30, 90)


def compute_social_forces(
    square: Square, squares: list[Square]
) -> tuple[float, float, float, float, float, float]:
    flee_x: float = 0.0
    flee_y: float = 0.0
    chase_x: float = 0.0
    chase_y: float = 0.0
    sep_x: float = 0.0
    sep_y: float = 0.0

    for other in squares:
        if other is square:
            continue
        dx: float = square.x - other.x
        dy: float = square.y - other.y
        dist: float = math.hypot(dx, dy)
        if dist == 0:
            continue

        if other.size > square.size and dist < FLEE_RADIUS:
            weight: float = 1.0 - (dist / FLEE_RADIUS)
            flee_x += (dx / dist) * weight
            flee_y += (dy / dist) * weight

        if other.size < square.size and dist < CHASE_RADIUS:
            weight = 1.0 - (dist / CHASE_RADIUS)
            chase_x += (-dx / dist) * weight
            chase_y += (-dy / dist) * weight

        if dist < SEP_RADIUS:
            weight = 1.0 - (dist / SEP_RADIUS)
            sep_x += (dx / dist) * weight
            sep_y += (dy / dist) * weight

    return flee_x, flee_y, chase_x, chase_y, sep_x, sep_y


def compute_wall_force(
    square: Square, screen_w: int, screen_h: int
) -> tuple[float, float]:
    wall_x: float = 0.0
    wall_y: float = 0.0

    if square.x < WALL_MARGIN:
        wall_x += WALL_STRENGTH * (1.0 - square.x / WALL_MARGIN)
    if square.x + square.size > screen_w - WALL_MARGIN:
        right_gap: float = screen_w - (square.x + square.size)
        wall_x -= WALL_STRENGTH * (1.0 - right_gap / WALL_MARGIN)
    if square.y < WALL_MARGIN:
        wall_y += WALL_STRENGTH * (1.0 - square.y / WALL_MARGIN)
    if square.y + square.size > screen_h - WALL_MARGIN:
        bottom_gap: float = screen_h - (square.y + square.size)
        wall_y -= WALL_STRENGTH * (1.0 - bottom_gap / WALL_MARGIN)

    return wall_x, wall_y


def apply_steering(square: Square, steer_x: float, steer_y: float) -> None:
    steer_length: float = math.hypot(steer_x, steer_y)
    if steer_length > 0:
        steer_x /= steer_length
        steer_y /= steer_length
        square.vx = (1 - STEER_BLEND) * square.vx + STEER_BLEND * steer_x * square.speed
        square.vy = (1 - STEER_BLEND) * square.vy + STEER_BLEND * steer_y * square.speed


def clamp_speed(square: Square) -> None:
    velocity_magnitude: float = math.hypot(square.vx, square.vy)
    if velocity_magnitude > square.speed:
        square.vx = (square.vx / velocity_magnitude) * square.speed
        square.vy = (square.vy / velocity_magnitude) * square.speed


def move_and_wrap(square: Square, screen_w: int, screen_h: int, dt: float) -> None:
    """Exercise 3: Squares wrap around the screen edges instead of bouncing."""
    square.x += square.vx * dt * 60
    square.y += square.vy * dt * 60

    if square.x < 0:
        square.x = screen_w
    elif square.x > screen_w:
        square.x = 0

    if square.y < 0:
        square.y = screen_h
    elif square.y > screen_h:
        square.y = 0


def anti_stick(square: Square, screen_w: int, screen_h: int) -> None:
    eps: float = 1e-6
    if square.x <= eps and square.vx < 0:
        square.vx = 0
    if square.x + square.size >= screen_w - eps and square.vx > 0:
        square.vx = 0
    if square.y <= eps and square.vy < 0:
        square.vy = 0
    if square.y + square.size >= screen_h - eps and square.vy > 0:
        square.vy = 0


def update_square(
    square: Square, screen_w: int, screen_h: int, squares: list[Square], dt: float
) -> None:
    if square.freeze_timer > 0:
        square.freeze_timer -= dt
        return

    square.age += dt
    apply_jitter(square)

    flee_x, flee_y, chase_x, chase_y, sep_x, sep_y = compute_social_forces(
        square, squares
    )
    wall_x, wall_y = compute_wall_force(square, screen_w, screen_h)

    steer_x: float = (
        flee_x * FLEE_WEIGHT
        + chase_x * CHASE_WEIGHT
        + wall_x * WALL_WEIGHT
        + sep_x * SEPARATION_WEIGHT
    )
    steer_y: float = (
        flee_y * FLEE_WEIGHT
        + chase_y * CHASE_WEIGHT
        + wall_y * WALL_WEIGHT
        + sep_y * SEPARATION_WEIGHT
    )

    apply_steering(square, steer_x, steer_y)
    clamp_speed(square)
    # Updated for Exercise 3
    move_and_wrap(square, screen_w, screen_h, dt)
    anti_stick(square, screen_w, screen_h)
