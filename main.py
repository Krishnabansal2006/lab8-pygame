import random
import math
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
NUM_SQUARES = 100
BG_COLOR = (20, 20, 30)
MIN_SIZE = 10
MAX_SIZE = 50
MAX_SPEED = 4.0


class Square:
    def __init__(self, x: float, y: float, size: int, color: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.max_speed = MAX_SPEED * (MIN_SIZE / self.size)
        self.jitter_timer = random.randint(20, 60)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = self.max_speed * math.cos(angle)
        self.vy = self.max_speed * math.sin(angle)

    def update(self, screen_w: int, screen_h: int) -> None:
        self.jitter_timer -= 1
        if self.jitter_timer <= 0:
            angle = math.atan2(self.vy, self.vx)
            angle += random.uniform(-0.05, 0.05)
            speed = math.hypot(self.vx, self.vy)
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.jitter_timer = random.randint(30, 90)

        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        if self.x + self.size > screen_w:
            self.x = screen_w - self.size
            self.vx = -abs(self.vx)
        if self.y < 0:
            self.y = 0
            self.vy = abs(self.vy)
        if self.y + self.size > screen_h:
            self.y = screen_h - self.size
            self.vy = -abs(self.vy)

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
            sq.update(WIDTH, HEIGHT)
            sq.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()