import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 448, 480
CELL_SIZE = WIDTH // 28
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Maze (1 = wall, 0 = pellet, 2 = empty)
maze = [
    "1111111111111111111111111111",
    "1000000000100000000010000001",
    "1111111111111111111111111111",
    "1000100100010010001001000101",
    "1111111111111111111111111111",
    "1000100100010010001001000101",
    "1111111111111111111111111111",
    "1000100100010010001001000101",
    "1111111111111111111111111111",
    "1000100100010010001001000101",
    "1111111111111111111111111111",
    "1000000000100000000010000001",
    "1111111111111111111111111111",
]

# Pac-Man
pacman_x = 14 * CELL_SIZE + CELL_SIZE // 2
pacman_y = 23 * CELL_SIZE + CELL_SIZE // 2
pacman_radius = CELL_SIZE // 2
pacman_speed = CELL_SIZE // 4
pacman_direction = 0  # 0: right, 1: down, 2: left, 3: up

# Ghost
ghost_x = CELL_SIZE + CELL_SIZE // 2
ghost_y = CELL_SIZE + CELL_SIZE // 2
ghost_radius = CELL_SIZE // 2
ghost_speed = CELL_SIZE // 4
ghost_direction = 0  # Initial direction

# Game variables
score = 0
game_over = False

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman_direction = 0
            elif event.key == pygame.K_DOWN:
                pacman_direction = 1
            elif event.key == pygame.K_LEFT:
                pacman_direction = 2
            elif event.key == pygame.K_UP:
                pacman_direction = 3

    # Pac-Man movement (with wall collision and boundary checks)
    new_pacman_x = pacman_x
    new_pacman_y = pacman_y

    if pacman_direction == 0:
        new_pacman_x += pacman_speed
    elif pacman_direction == 1:
        new_pacman_y += pacman_speed
    elif pacman_direction == 2:
        new_pacman_x -= pacman_speed
    elif pacman_direction == 3:
        new_pacman_y -= pacman_speed

    pacman_grid_x = new_pacman_x // CELL_SIZE
    pacman_grid_y = new_pacman_y // CELL_SIZE

    if 0 <= pacman_grid_y < len(maze) and 0 <= pacman_grid_x < len(maze[0]):
        if maze[pacman_grid_y][pacman_grid_x] != "1":
            pacman_x = new_pacman_x
            pacman_y = new_pacman_y
    else:
        if pacman_direction == 0: pacman_x -= pacman_speed
        elif pacman_direction == 1: pacman_y -= pacman_speed
        elif pacman_direction == 2: pacman_x += pacman_speed
        elif pacman_direction == 3: pacman_y += pacman_speed


    # Ghost movement (simple chase - needs improvement)
    dx = pacman_x - ghost_x
    dy = pacman_y - ghost_y
    if abs(dx) > abs(dy):
        ghost_direction = 0 if dx > 0 else 2
    else:
        ghost_direction = 1 if dy > 0 else 3

    new_ghost_x = ghost_x
    new_ghost_y = ghost_y

    if ghost_direction == 0: new_ghost_x += ghost_speed
    elif ghost_direction == 1: new_ghost_y += ghost_speed
    elif ghost_direction == 2: new_ghost_x -= ghost_speed
    elif ghost_direction == 3: new_ghost_y -= ghost_speed

    ghost_grid_x = new_ghost_x // CELL_SIZE
    ghost_grid_y = new_ghost_y // CELL_SIZE

    if 0 <= ghost_grid_y < len(maze) and 0 <= ghost_grid_x < len(maze[0]):
        if maze[ghost_grid_y][ghost_grid_x] != "1":
            ghost_x = new_ghost_x
            ghost_y = new_ghost_y
    else:
        if ghost_direction == 0: ghost_x -= ghost_speed
        elif ghost_direction == 1: ghost_y -= ghost_speed
        elif ghost_direction == 2: ghost_x += ghost_speed
        elif ghost_direction == 3: ghost_y += ghost_speed

    # Pellet collection (with boundary check)
    pellet_x = pacman_x // CELL_SIZE
    pellet_y = pacman_y // CELL_SIZE

    if 0 <= pellet_y < len(maze) and 0 <= pellet_x < len(maze[0]):
        if maze[pellet_y][pellet_x] == "0":
            maze[pellet_y] = maze[pellet_y][:pellet_x] + "2" + maze[pellet_y][pellet_x + 1:]
            score += 10

    # Draw everything
    screen.fill(BLACK)

    # Draw maze
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "1":
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == "0":
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 2)

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), pacman_radius)

    # Draw Ghost
    pygame.draw.circle(screen, RED, (ghost_x, ghost_y), ghost_radius)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
