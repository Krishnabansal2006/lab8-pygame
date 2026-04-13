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
    # Short-lived visual burst used when a square dies.
    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.color: tuple[int, int, int] = color
        angle: float = random.uniform(0, 2 * math.pi)
        speed: float = random.uniform(80, 200)
        self.vx: float = math.cos(angle) * speed
        self.vy: float = math.sin(angle) * speed
        self.age: float = 0.0
        self.lifespan: float = random.uniform(0.6, 1.2)

    def update(self, dt: float) -> None:
        # Move particle outward over time.
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_dead(self) -> bool:
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        # Shrink as the particle approaches the end of its lifespan.
        alpha: float = 1.0 - (self.age / self.lifespan)
        radius: int = max(1, int(4 * alpha))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)


class Square:
    # Main moving entity in the simulation.
    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.size: int = size
        self.color: tuple[int, int, int] = color
        self.max_speed: float = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed: float = self.max_speed
        self.jitter_timer: int = random.randint(20, 60)
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)
        self.vy: float = self.speed * math.sin(angle)
        self.lifespan: float = random.uniform(5, 20)
        self.age: float = 0.0

    def update(self, screen_w: int, screen_h: int, squares: list, dt: float) -> None:
        # Age increases every frame; this drives death timing.
        self.age += dt

        # Random jitter keeps movement organic instead of perfectly straight.
        self.jitter_timer -= 1
        if self.jitter_timer <= 0:
            angle: float = math.atan2(self.vy, self.vx) + random.uniform(-0.1, 0.1)
            self.vx = self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            self.jitter_timer = random.randint(30, 90)

        # Steer away from nearby bigger squares.
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
                    w: float = 1.0 - (dist / FLEE_RADIUS)
                    flee_x += (dx / dist) * w
                    flee_y += (dy / dist) * w

                # Soft steering away from screen boundaries.
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

        # Blend flee and wall steering into current velocity.
        steer_x: float = flee_x + wall_x
        steer_y: float = flee_y + wall_y
        steer_len: float = math.hypot(steer_x, steer_y)

        if steer_len > 0:
            steer_x /= steer_len
            steer_y /= steer_len
            blend: float = 0.22
            self.vx = (1 - blend) * self.vx + blend * steer_x * self.speed
            self.vy = (1 - blend) * self.vy + blend * steer_y * self.speed

        # Clamp speed so steering does not exceed max speed.
        v: float = math.hypot(self.vx, self.vy)
        if v > self.speed:
            self.vx = (self.vx / v) * self.speed
            self.vy = (self.vy / v) * self.speed

        # Frame-rate independent movement.
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Hard bounce if crossing screen limits.
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

        # Anti-stick guard near edges.
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
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )


def create_square(screen_w: int, screen_h: int) -> Square:
    size: int = random.randint(MIN_SIZE, MAX_SIZE)
    x: float = random.uniform(0, screen_w - size)
    y: float = random.uniform(0, screen_h - size)
    color: tuple[int, int, int] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    return Square(x, y, size, color)


def create_squares(n: int, screen_w: int, screen_h: int) -> list[Square]:
    return [create_square(screen_w, screen_h) for _ in range(n)]


def create_particles(x: float, y: float, color: tuple[int, int, int]) -> list[Particle]:
    # Burst count controls how dense the scatter looks.
    return [Particle(x, y, color) for _ in range(30)]

def main() -> None:
    pygame.init()
    font: pygame.font.Font = pygame.font.SysFont(None, 20)
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Squares")
    clock: pygame.time.Clock = pygame.time.Clock()
    squares: list[Square] = create_squares(NUM_SQUARES, WIDTH, HEIGHT)
    # Particles are temporary visuals created on death.
    particles: list[Particle] = []
    # Each value is an absolute time when one new square should spawn.
    pending_spawns: list[float] = []
    current_time: float = 0.0

    running: bool = True
    while running:
        dt: float = clock.tick(FPS) / 1000.0
        current_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Update squares; dead ones are removed immediately.
        alive: list[Square] = []
        for sq in squares:
            sq.update(WIDTH, HEIGHT, squares, dt)
            if sq.is_dead():
                # Spawn a scatter burst at the square center.
                cx: float = sq.x + sq.size / 2
                cy: float = sq.y + sq.size / 2
                particles.extend(create_particles(cx, cy, sq.color))
                # Rebirth is delayed by 2 seconds.
                pending_spawns.append(current_time + 2.0)
            else:
                alive.append(sq)
        squares = alive

        # Spawn any delayed rebirths whose target time has passed.
        still_pending: list[float] = []
        for spawn_time in pending_spawns:
            if current_time >= spawn_time:
                squares.append(create_square(WIDTH, HEIGHT))
            else:
                still_pending.append(spawn_time)
        pending_spawns = still_pending

        # Draw active squares.
        for sq in squares:
            sq.draw(screen)

        # Update and draw scatter particles.
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