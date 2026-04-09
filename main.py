import random
import math
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
NUM_SQUARES = 20
BG_COLOR = (20, 20, 30)
MIN_SIZE = 10
MAX_SIZE = 50
MAX_SPEED = 4.0
FLEE_RADIUS = 70


class Square:
    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.max_speed = MAX_SPEED * (MIN_SIZE / self.size)
        self.speed = self.max_speed
        self.jitter_timer = random.randint(20, 60)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def update(self, screen_w: int, screen_h: int, squares: list) -> None:
        self.jitter_timer -= 1
        if self.jitter_timer <= 0:
            angle = math.atan2(self.vy, self.vx) + random.uniform(-0.1, 0.1)
            self.vx = self.speed * math.cos(angle)
            self.vy = self.speed * math.sin(angle)
            self.jitter_timer = random.randint(30, 90)

        flee_x = 0.0
        flee_y = 0.0
        for other in squares:
            if other is self:
                continue
            if other.size > self.size:
                dx = self.x - other.x
                dy = self.y - other.y
                dist = math.hypot(dx, dy)
                if 0 < dist < FLEE_RADIUS:
                    w = 1.0 - (dist / FLEE_RADIUS)
                    flee_x += (dx / dist) * w
                    flee_y += (dy / dist) * w

        wall_x = 0.0
        wall_y = 0.0
        margin = 40
        wall_strength = 0.35

        if self.x < margin:
            wall_x += wall_strength * (1.0 - self.x / margin)
        if self.x + self.size > screen_w - margin:
            right_gap = screen_w - (self.x + self.size)
            wall_x -= wall_strength * (1.0 - right_gap / margin)
        if self.y < margin:
            wall_y += wall_strength * (1.0 - self.y / margin)
        if self.y + self.size > screen_h - margin:
            bottom_gap = screen_h - (self.y + self.size)
            wall_y -= wall_strength * (1.0 - bottom_gap / margin)

        steer_x = flee_x + wall_x
        steer_y = flee_y + wall_y
        steer_len = math.hypot(steer_x, steer_y)

        if steer_len > 0:
            steer_x /= steer_len
            steer_y /= steer_len
            blend = 0.22
            self.vx = (1 - blend) * self.vx + blend * steer_x * self.speed
            self.vy = (1 - blend) * self.vy + blend * steer_y * self.speed

        v = math.hypot(self.vx, self.vy)
        if v > self.speed:
            self.vx = (self.vx / v) * self.speed
            self.vy = (self.vy / v) * self.speed

        self.x += self.vx
        self.y += self.vy

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

        eps = 1e-6
        if self.x <= eps and self.vx < 0:
            self.vx = 0
        if self.x + self.size >= screen_w - eps and self.vx > 0:
            self.vx = 0
        if self.y <= eps and self.vy < 0:
            self.vy = 0
        if self.y + self.size >= screen_h - eps and self.vy > 0:
            self.vy = 0

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(int(self.x), int(self.y), self.size, self.size),
        )


def create_squares(n: int, screen_w: int, screen_h: int) -> list[Square]:
    squares: list[Square] = []
    for _ in range(n):
        size = random.randint(MIN_SIZE, MAX_SIZE)
        x = random.uniform(0, screen_w - size)
        y = random.uniform(0, screen_h - size)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        squares.append(Square(x, y, size, color))
    return squares


def main() -> None:
    pygame.init()
    font = pygame.font.SysFont(None, 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Squares")
    clock = pygame.time.Clock()
    squares = create_squares(NUM_SQUARES, WIDTH, HEIGHT)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_COLOR)
        for sq in squares:
            sq.update(WIDTH, HEIGHT, squares)
            sq.draw(screen)
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        count_text = font.render(f"Squares: {len(squares)}", True, (255, 255, 255))
        screen.blit(count_text, (10, 30))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()