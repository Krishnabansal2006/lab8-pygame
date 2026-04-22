import random
import math
import pygame

# ─── Constants ────────────────────────────────────────────────────────────────
WIDTH: int = 800               
HEIGHT: int = 600              
FPS: int = 60                  
NUM_SQUARES: int = 15          
BG_COLOR: tuple[int, int, int] = (20, 20, 30)  
MIN_SIZE: int = 10            
MAX_SIZE: int = 50             
MAX_SPEED: float = 4.0         
FLEE_RADIUS: float = 70.0      # pixels - small squares detect threats within this range
CHASE_RADIUS: float = 120.0    # pixels - big squares detect prey within this range
SEP_RADIUS: float = 30.0       # pixels - squares push apart when closer than this


# ─── Particle ─────────────────────────────────────────────────────────────────
class Particle:
    """
    Short-lived visual dot.
    Used for two effects:
    - Death burst: particles fly outward from where a square died
    - Birth convergence: particles start scattered and fly inward to birth point
    """

    def __init__(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.color: tuple[int, int, int] = color
        # Default: random outward velocity (overridden for birth particles)
        angle: float = random.uniform(0, 2 * math.pi)
        speed: float = random.uniform(80, 200)  # pixels per second
        self.vx: float = math.cos(angle) * speed
        self.vy: float = math.sin(angle) * speed
        self.age: float = 0.0
        self.lifespan: float = random.uniform(0.6, 1.2)  # seconds alive

    def update(self, dt: float) -> None:
        """Move the particle forward and age it."""
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_dead(self) -> bool:
        """True when the particle has exceeded its lifespan."""
        return self.age >= self.lifespan

    def draw(self, surface: pygame.Surface) -> None:
        """Draw as a small circle that shrinks and fades as it ages."""
        alpha: float = 1.0 - (self.age / self.lifespan)  # 1.0 = fresh, 0.0 = dead
        radius: int = max(1, int(4 * alpha))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)


# ─── Square ───────────────────────────────────────────────────────────────────
class Square:
    """
    The main entity. Each square:
    - Moves with jitter (random direction changes)
    - Flees from bigger squares nearby
    - Chases smaller squares nearby
    - Separates from squares that are too close
    - Steers away from walls
    - Has a lifespan and dies when it expires or is caught
    """

    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int]) -> None:
        self.x: float = x
        self.y: float = y
        self.size: int = size
        self.color: tuple[int, int, int] = color
        # Bigger squares move slower (speed = MAX_SPEED * MIN_SIZE / size)
        self.max_speed: float = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed: float = self.max_speed
        self.jitter_timer: int = random.randint(20, 60)  # frames until next direction nudge
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)   # velocity x component
        self.vy: float = self.speed * math.sin(angle)   # velocity y component
        self.lifespan: float = random.uniform(5, 20)    # seconds until natural death
        self.age: float = 0.0                           # seconds alive so far
        self.freeze_timer: float = 0.0                  # seconds to stay frozen after rebirth

    def update(self, screen_w: int, screen_h: int, squares: list, dt: float) -> None:
        """
        Main update called every frame.
        Order: freeze check → age → jitter → flee → chase → separation 
        → wall steering → blend velocity → clamp speed → move → bounce
        """

        # 1) Freeze: new squares pause briefly after rebirth
        if self.freeze_timer > 0:
            self.freeze_timer -= dt
            return

        # 2) Age toward natural death
        self.age += dt

        # 3) Jitter: slightly rotate velocity every few frames for organic movement
        self.jitter_timer -= 1
        if self.jitter_timer <= 0:
            angle: float = math.atan2(self.vy, self.vx) + random.uniform(-0.1, 0.1)
            self.vx = self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            self.jitter_timer = random.randint(30, 90)

        # 4) Flee, Chase, Separation: calculate steering forces based on nearby squares
        flee_x: float = 0.0
        flee_y: float = 0.0
        chase_x: float = 0.0
        chase_y: float = 0.0
        sep_x: float = 0.0
        sep_y: float = 0.0

        for other in squares:
            if other is self:
                continue
            dx: float = self.x - other.x
            dy: float = self.y - other.y
            dist: float = math.hypot(dx, dy)
            if dist == 0:
                continue
            if other.size > self.size and 0 < dist < FLEE_RADIUS:
                w: float = 1.0 - (dist / FLEE_RADIUS)
                flee_x += (dx / dist) * w
                flee_y += (dy / dist) * w
            if other.size < self.size and 0 < dist < CHASE_RADIUS:
                w = 1.0 - (dist / CHASE_RADIUS)
                chase_x += (-dx / dist) * w
                chase_y += (-dy / dist) * w
            if dist < SEP_RADIUS:
                w = 1.0 - (dist / SEP_RADIUS)
                sep_x += (dx / dist) * w
                sep_y += (dy / dist) * w

        # 5) Wall steering: gentle push away from screen edges before impact
        wall_x: float = 0.0
        wall_y: float = 0.0
        margin: int = 60         # pixels from edge where push begins
        wall_strength: float = 0.8

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

        # 6) Combine forces - flee takes priority over chase
        steer_x: float = flee_x * 0.5 + chase_x * 0.2 + wall_x * 0.25 + sep_x * 0.05
        steer_y: float = flee_y * 0.5 + chase_y * 0.2 + wall_y * 0.25 + sep_y * 0.05

        steer_len: float = math.hypot(steer_x, steer_y)

        if steer_len > 0:
            # Normalize to unit vector, then blend 35% new direction into velocity
            steer_x /= steer_len
            steer_y /= steer_len
            blend: float = 0.35
            self.vx = (1 - blend) * self.vx + blend * steer_x * self.speed
            self.vy = (1 - blend) * self.vy + blend * steer_y * self.speed

        # 7) Clamp: prevent any force from exceeding max speed
        v: float = math.hypot(self.vx, self.vy)
        if v > self.speed:
            self.vx = (self.vx / v) * self.speed
            self.vy = (self.vy / v) * self.speed

        # 8) Move: time-based so speed is frame-rate independent
        # dt * 60 means at 60 FPS the multiplier is 1.0 (no change)
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # 9) Hard bounce off all four walls
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

        # 10) Anti-stick: zero out velocity pointing into a wall
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
        """True when the square has lived past its natural lifespan."""
        return self.age >= self.lifespan

    def is_caught(self, squares: list) -> bool:
        """True if a bigger square is physically overlapping this square."""
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
        """Draw as a solid colored rectangle."""
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )


# ─── Factory functions ────────────────────────────────────────────────────────

def create_square(screen_w: int, screen_h: int) -> Square:
    """Create one square with random size, position and color."""
    size: int = random.randint(MIN_SIZE, MAX_SIZE)
    x: float = random.uniform(0, screen_w - size)
    y: float = random.uniform(0, screen_h - size)
    color: tuple[int, int, int] = (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255),
    )
    return Square(x, y, size, color)


def create_squares(n: int, screen_w: int, screen_h: int) -> list[Square]:
    """Create n squares."""
    return [create_square(screen_w, screen_h) for _ in range(n)]


def create_death_particles(x: float, y: float, color: tuple[int, int, int]) -> list[Particle]:
    """30 particles bursting outward from death position."""
    return [Particle(x, y, color) for _ in range(30)]


def create_birth_particles(x: float, y: float, color: tuple[int, int, int]) -> list[Particle]:
    """
    30 particles that start scattered and converge toward birth position.
    Each particle starts at a random offset and its velocity points inward.
    """
    particles: list[Particle] = []
    for _ in range(30):
        angle: float = random.uniform(0, 2 * math.pi)
        distance: float = random.uniform(50, 150)
        start_x: float = x + math.cos(angle) * distance
        start_y: float = y + math.sin(angle) * distance
        p: Particle = Particle(start_x, start_y, color)
        speed: float = random.uniform(80, 200)
        dx: float = x - start_x
        dy: float = y - start_y
        length: float = math.hypot(dx, dy)
        # Override default outward velocity with inward direction
        p.vx = (dx / length) * speed
        p.vy = (dy / length) * speed
        particles.append(p)
    return particles


# ─── Main loop ────────────────────────────────────────────────────────────────

def main() -> None:
    pygame.init()
    font: pygame.font.Font = pygame.font.SysFont(None, 20)
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Squares")
    clock: pygame.time.Clock = pygame.time.Clock()

    squares: list[Square] = create_squares(NUM_SQUARES, WIDTH, HEIGHT)
    particles: list[Particle] = []
    # pending_spawns: list of (target_time, x, y) for delayed rebirths
    pending_spawns: list[tuple[float, float, float]] = []
    current_time: float = 0.0

    running: bool = True
    while running:
        dt: float = clock.tick(FPS) / 1000.0  # seconds since last frame
        current_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Update all squares and collect dead ones
        alive: list[Square] = []
        for sq in squares:
            sq.update(WIDTH, HEIGHT, squares, dt)
            if sq.is_dead() or sq.is_caught(squares):
                # Square died - burst particles and schedule rebirth
                cx: float = sq.x + sq.size / 2
                cy: float = sq.y + sq.size / 2
                particles.extend(create_death_particles(cx, cy, sq.color))
                pending_spawns.append((current_time + 2.0, cx, cy))
            else:
                alive.append(sq)
        squares = alive  # safe swap - never mutate list during iteration

        # Spawn rebirths whose delay has elapsed
        still_pending: list[tuple[float, float, float]] = []
        for spawn_time, bx, by in pending_spawns:
            if current_time >= spawn_time:
                size: int = random.randint(MIN_SIZE, MAX_SIZE)
                color: tuple[int, int, int] = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                )
                new_sq: Square = Square(bx - size / 2, by - size / 2, size, color)
                new_sq.vx = 0.0
                new_sq.vy = 0.0
                new_sq.age = 0.0
                new_sq.freeze_timer = 1.0  # pause while birth particles converge
                particles.extend(create_birth_particles(bx, by, color))
                squares.append(new_sq)
            else:
                still_pending.append((spawn_time, bx, by))
        pending_spawns = still_pending

        # Draw squares
        for sq in squares:
            sq.draw(screen)

        # Update and draw particles, removing expired ones
        particles = [p for p in particles if not p.is_dead()]
        for p in particles:
            p.update(dt)
            p.draw(screen)

        # HUD
        fps_text: pygame.Surface = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        count_text: pygame.Surface = font.render(f"Squares: {len(squares)}", True, (255, 255, 255))
        screen.blit(count_text, (10, 30))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()