import random
import math
import pygame

# Window and simulation settings
WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60
NUM_SQUARES: int = 20
BG_COLOR: tuple[int, int, int] = (20, 20, 30)
MIN_SIZE: int = 10
MAX_SIZE: int = 50
MAX_SPEED: float = 4.0
FLEE_RADIUS: float = 70.0


class Particle:
    """Short-lived dot used for death burst and birth convergence effects."""

    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.color: tuple[int, int, int] = color
        # Random outward direction - overwritten for birth particles
        angle: float = random.uniform(0, 2 * math.pi)
        speed: float = random.uniform(80, 200)
        self.vx: float = math.cos(angle) * speed
        self.vy: float = math.sin(angle) * speed
        self.age: float = 0.0
        self.lifespan: float = random.uniform(0.6, 1.2)

    def update(self, dt: float) -> None:
        """Move particle and advance its age."""
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_dead(self) -> bool:
        """Returns True when particle has exceeded its lifespan."""
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        """Draw particle as a shrinking circle that fades toward end of life."""
        alpha: float = 1.0 - (self.age / self.lifespan)
        radius: int = max(1, int(4 * alpha))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)


class Square:
    """Main moving entity in the simulation."""

    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.size: int = size
        self.color: tuple[int, int, int] = color
        # Bigger squares are slower
        self.max_speed: float = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed: float = self.max_speed
        self.jitter_timer: int = random.randint(20, 60)
        # Start moving in a random direction
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)
        self.vy: float = self.speed * math.sin(angle)
        # Each square lives between 5 and 20 seconds
        self.lifespan: float = random.uniform(5, 20)
        self.age: float = 0.0
        # Freeze timer pauses movement after rebirth
        self.freeze_timer: float = 0.0

    def update(self, screen_w: int, screen_h: int, squares: list, dt: float) -> None:
        """Update position, steering, and age each frame."""

        # If frozen after rebirth, count down and skip movement
        if self.freeze_timer > 0:
            self.freeze_timer -= dt
            return

        # Age the square toward its death
        self.age += dt

        # Jitter: slightly rotate direction every few frames for organic movement
        self.jitter_timer -= 1
        if self.jitter_timer <= 0:
            angle: float = math.atan2(self.vy, self.vx) + random.uniform(-0.1, 0.1)
            self.vx = self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            self.jitter_timer = random.randint(30, 90)

        # Flee: steer away from nearby bigger squares
        flee_x: float = 0.0
        flee_y: float = 0.0
        for other in squares:
            if other is self:
                continue
            if other.size > self.size:
                dx: float = self.x - other.x
                dy: float = self.y - other.y
                dist: float = math.hypot(dx, dy)
                if 0 < dist < FLEE_RADIUS:
                    # Closer threats push harder
                    w: float = 1.0 - (dist / FLEE_RADIUS)
                    flee_x += (dx / dist) * w
                    flee_y += (dy / dist) * w

        # Wall steering: push away from edges before hitting them
        wall_x: float = 0.0
        wall_y: float = 0.0
        margin: int = 40
        wall_strength: float = 0.35

        if self.x < margin:
            wall_x += wall_strength * (1.0 - self.x / margin)
        if self.x + self.size > screen_w - margin:
            right_gap: float = screen_w - (self.x + self.size)
            wall_x -= wall_strength * (1.0 - right_gap / margin)
        if self.y < margin:
            wall_y += wall_strength * (1.0 - self.y / margin)
        if self.y + self.size > screen_h - margin:
            bottom_gap: float = screen_h - (self.y + self.size)
            wall_y -= wall_strength * (1.0 - bottom_gap / margin)

        # Combine flee and wall into one steering force
        steer_x: float = flee_x + wall_x
        steer_y: float = flee_y + wall_y
        steer_len: float = math.hypot(steer_x, steer_y)

        if steer_len > 0:
            # Normalize then blend smoothly into current velocity
            steer_x /= steer_len
            steer_y /= steer_len
            blend: float = 0.22
            self.vx = (1 - blend) * self.vx + blend * steer_x * self.speed
            self.vy = (1 - blend) * self.vy + blend * steer_y * self.speed

        # Clamp speed so no force exceeds max
        v: float = math.hypot(self.vx, self.vy)
        if v > self.speed:
            self.vx = (self.vx / v) * self.speed
            self.vy = (self.vy / v) * self.speed

        # Time-based movement: dt*60 keeps speed consistent at any frame rate
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Hard bounce off walls
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x + self.size > screen_w:
            self.x = screen_w - self.size
            self.vx = -abs(self.vx)

        if self.y < 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + self.size > screen_h:
            self.y = screen_h - self.size
            self.vy = -abs(self.vy)

        # Anti-stick: cancel velocity pointing into a wall
        eps: float = 1e-6
        if self.x <= eps and self.vx < 0:
            self.vx = 0
        if self.x + self.size >= screen_w - eps and self.vx > 0:
            self.vx = 0
        if self.y <= eps and self.vy < 0:
            self.vy = 0
        if self.y + self.size >= screen_h - eps and self.vy > 0:
            self.vy = 0

    def is_dead(self) -> bool:
        """Returns True when square has lived past its lifespan."""
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the square as a filled rectangle."""
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )


def create_square(screen_w: int, screen_h: int) -> Square:
    """Create one square at a random position with random size and color."""
    size: int = random.randint(MIN_SIZE, MAX_SIZE)
    x: float = random.uniform(0, screen_w - size)
    y: float = random.uniform(0, screen_h - size)
    color: tuple[int, int, int] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    return Square(x, y, size, color)


def create_squares(n: int, screen_w: int, screen_h: int) -> list[Square]:
    """Create n squares at random positions."""
    return [create_square(screen_w, screen_h) for _ in range(n)]


def create_death_particles(x: float, y: float, color: tuple[int, int, int]) -> list[Particle]:
    """Burst of particles flying outward from death position."""
    return [Particle(x, y, color) for _ in range(30)]


def create_birth_particles(x: float, y: float, color: tuple[int, int, int]) -> list[Particle]:
    """Particles start scattered around birth position and converge inward."""
    particles: list[Particle] = []
    for _ in range(30):
        # Start at random offset from birth point
        angle: float = random.uniform(0, 2 * math.pi)
        distance: float = random.uniform(50, 150)
        start_x: float = x + math.cos(angle) * distance
        start_y: float = y + math.sin(angle) * distance
        p: Particle = Particle(start_x, start_y, color)
        # Override velocity to point toward birth center
        speed: float = random.uniform(80, 200)
        dx: float = x - start_x
        dy: float = y - start_y
        length: float = math.hypot(dx, dy)
        p.vx = (dx / length) * speed
        p.vy = (dy / length) * speed
        particles.append(p)
    return particles


def main() -> None:
    pygame.init()
    font: pygame.font.Font = pygame.font.SysFont(None, 20)
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Squares")
    clock: pygame.time.Clock = pygame.time.Clock()
    squares: list[Square] = create_squares(NUM_SQUARES, WIDTH, HEIGHT)
    particles: list[Particle] = []
    # Each entry stores (spawn_time, x, y) for a pending rebirth
    pending_spawns: list[tuple[float, float, float]] = []
    current_time: float = 0.0

    running: bool = True
    while running:
        dt: float = clock.tick(FPS) / 1000.0
        current_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Update squares and handle deaths
        alive: list[Square] = []
        for sq in squares:
            sq.update(WIDTH, HEIGHT, squares, dt)
            if sq.is_dead():
                # Death burst at square center
                cx: float = sq.x + sq.size / 2
                cy: float = sq.y + sq.size / 2
                particles.extend(create_death_particles(cx, cy, sq.color))
                # Schedule rebirth at same position 2 seconds later
                pending_spawns.append((current_time + 2.0, cx, cy))
            else:
                alive.append(sq)
        squares = alive

        # Spawn any rebirths whose timer has elapsed
        still_pending: list[tuple[float, float, float]] = []
        for spawn_time, bx, by in pending_spawns:
            if current_time >= spawn_time:
                size: int = random.randint(MIN_SIZE, MAX_SIZE)
                color: tuple[int, int, int] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                # Spawn at death position
                new_sq: Square = Square(bx - size / 2, by - size / 2, size, color)
                new_sq.vx = 0.0
                new_sq.vy = 0.0
                new_sq.age = 0.0
                # Freeze for 1 second so birth particles can converge first
                new_sq.freeze_timer = 1.0
                particles.extend(create_birth_particles(bx, by, color))
                squares.append(new_sq)
            else:
                still_pending.append((spawn_time, bx, by))
        pending_spawns = still_pending

        # Draw squares
        for sq in squares:
            sq.draw(screen)

        # Update and draw particles
        particles = [p for p in particles if not p.is_dead()]
        for p in particles:
            p.update(dt)
            p.draw(screen)

        fps_text: pygame.Surface = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        count_text: pygame.Surface = font.render(f"Squares: {len(squares)}", True, (255, 255, 255))
        screen.blit(count_text, (10, 30))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()