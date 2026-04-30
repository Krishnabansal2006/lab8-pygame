Color = tuple[int, int, int]

WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60
NUM_SQUARES: int = 15
BG_COLOR: Color = (20, 20, 30)

MIN_SIZE: int = 10
MAX_SIZE: int = 50
MAX_SPEED: float = 4.0

FLEE_RADIUS: float = 70.0
CHASE_RADIUS: float = 120.0
SEP_RADIUS: float = 30.0

# Steering and wall behavior weights.
FLEE_WEIGHT: float = 0.5
CHASE_WEIGHT: float = 0.2
WALL_WEIGHT: float = 0.25
SEPARATION_WEIGHT: float = 0.05
STEER_BLEND: float = 0.35

# Boundary and particle/rebirth behavior.
WALL_MARGIN: int = 60
WALL_STRENGTH: float = 0.8
DEATH_PARTICLE_COUNT: int = 30
BIRTH_PARTICLE_COUNT: int = 30
REBIRTH_DELAY_SECONDS: float = 2.0
REBIRTH_FREEZE_SECONDS: float = 1.0
