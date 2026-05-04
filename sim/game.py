import pygame

from .behavior import update_square
from .config import BG_COLOR, FPS, HEIGHT, NUM_SQUARES, REBIRTH_DELAY_SECONDS, WIDTH
from .entities import Particle, Square
from .factories import (
    create_birth_particles,
    create_death_particles,
    create_squares,
    spawn_reborn_square,
    create_fixed_square,
)


def _update_squares(
    squares: list[Square],
    particles: list[Particle],
    pending_spawns: list[tuple[float, float, float, int]],
    current_time: float,
    dt: float,
) -> list[Square]:
    """Update all squares and collect death effects plus rebirth schedules."""
    alive: list[Square] = []
    newly_split: list[Square] = []

    for square in squares:
        update_square(square, WIDTH, HEIGHT, squares, dt)

        predator = square.get_predator(squares)

        if square.is_dead() or predator is not None:
            if predator is not None:
                predator.grow(2)
                # Exercise 6: Split if size exceeds 30
                if predator.size >= 30:
                    newly_split.append(predator.split())

            center_x: float = square.x + square.size / 2
            center_y: float = square.y + square.size / 2
            particles.extend(create_death_particles(center_x, center_y, square.color))
            pending_spawns.append(
                (current_time + REBIRTH_DELAY_SECONDS, center_x, center_y, square.size)
            )
        else:
            alive.append(square)

    return alive + newly_split


def _process_rebirths(
    squares: list[Square],
    particles: list[Particle],
    pending_spawns: list[tuple[float, float, float, int]],
    current_time: float,
) -> list[tuple[float, float, float, int]]:
    """Spawn squares whose timers elapsed and keep the remaining schedule."""
    still_pending: list[tuple[float, float, float, int]] = []

    for spawn_time, birth_x, birth_y, original_size in pending_spawns:
        if current_time >= spawn_time:
            new_square: Square = spawn_reborn_square(birth_x, birth_y, original_size)
            particles.extend(create_birth_particles(birth_x, birth_y, new_square.color))
            squares.append(new_square)
        else:
            still_pending.append((spawn_time, birth_x, birth_y, original_size))

    return still_pending


def _draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    square_count: int,
) -> None:
    fps_text: pygame.Surface = font.render(
        f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255)
    )
    count_text: pygame.Surface = font.render(
        f"Squares: {square_count}", True, (255, 255, 255)
    )
    screen.blit(fps_text, (10, 10))
    screen.blit(count_text, (10, 30))


def run_game() -> None:
    pygame.init()
    font: pygame.font.Font = pygame.font.SysFont(None, 20)
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Squares")
    clock: pygame.time.Clock = pygame.time.Clock()

    squares: list[Square] = []
    for _ in range(5):
        squares.append(create_fixed_square(WIDTH, HEIGHT, 25))
    for _ in range(10):
        squares.append(create_fixed_square(WIDTH, HEIGHT, 10))
    for _ in range(30):
        squares.append(create_fixed_square(WIDTH, HEIGHT, 4))

    particles: list[Particle] = []
    pending_spawns: list[tuple[float, float, float, int]] = []
    current_time: float = 0.0

    running: bool = True
    while running:
        dt: float = clock.tick(FPS) / 1000.0
        current_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        squares = _update_squares(squares, particles, pending_spawns, current_time, dt)
        pending_spawns = _process_rebirths(
            squares, particles, pending_spawns, current_time
        )

        for square in squares:
            square.draw(screen)

        particles = [particle for particle in particles if not particle.is_dead()]
        for particle in particles:
            particle.update(dt)
            particle.draw(screen)

        _draw_hud(screen, font, clock, len(squares))
        pygame.display.flip()

    pygame.quit()
