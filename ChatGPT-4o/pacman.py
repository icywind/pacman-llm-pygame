import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 30
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pac-Man settings
pacman_x, pacman_y = 1 * TILE_SIZE, 1 * TILE_SIZE
pacman_speed = TILE_SIZE

# Ghost settings
ghost_x, ghost_y = 8 * TILE_SIZE, 8 * TILE_SIZE
ghost_speed = TILE_SIZE // 2

# Score
score = 0
font = pygame.font.Font(None, 36)

# Maze layout (1 = wall, 0 = path, 2 = pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 2, 1, 0, 1, 2, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 2, 0, 1],
    [1, 0, 0, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 2, 1, 0, 1],
    [1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 2, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 2, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 2, 0, 0, 2, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ghost movement with **safe** boundary checks
    ghost_dx = ghost_speed if pacman_x > ghost_x else -ghost_speed
    ghost_dy = ghost_speed if pacman_y > ghost_y else -ghost_speed

    new_ghost_x = ghost_x + ghost_dx
    new_ghost_y = ghost_y + ghost_dy

    if 0 <= new_ghost_x // TILE_SIZE < COLS and 0 <= ghost_y // TILE_SIZE < ROWS:
        if maze[ghost_y // TILE_SIZE][new_ghost_x // TILE_SIZE] != 1:
            ghost_x = new_ghost_x

    if 0 <= ghost_x // TILE_SIZE < COLS and 0 <= new_ghost_y // TILE_SIZE < ROWS:
        if maze[new_ghost_y // TILE_SIZE][ghost_x // TILE_SIZE] != 1:
            ghost_y = new_ghost_y

    # Draw Pac-Man & Ghost
    pygame.draw.circle(screen, YELLOW, (pacman_x + TILE_SIZE // 2, pacman_y + TILE_SIZE // 2), TILE_SIZE // 2)
    pygame.draw.circle(screen, RED, (ghost_x + TILE_SIZE // 2, ghost_y + TILE_SIZE // 2), TILE_SIZE // 2)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

