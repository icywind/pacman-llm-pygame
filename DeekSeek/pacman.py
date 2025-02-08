import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Maze layout (1 = wall, 0 = path, 'P' = pellet)
maze = [
    "11111111111111111111",
    "1P0000000100000000P1",
    "1011110101010111101",
    "1010000100010000101",
    "101011111111110101",
    "101010000000010101",
    "10001011111010001",
    "11111010001011111",
    "10000010001000001",
    "11111111111111111111"
]

# Tile size
TILE_SIZE = 20

# Pac-Man properties
pacman_pos = [1, 1]
pacman_speed = 2

# Ghost properties
ghost_pos = [9, 9]
ghost_speed = 1

# Pellets
pellets = []
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 'P':
            pellets.append((x, y))

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '1':
                pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 'P':
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 3)

# Function to check if a position is valid (not a wall)
def is_valid_position(x, y):
    if x < 0 or x >= len(maze[0]) or y < 0 or y >= len(maze):
        return False
    return maze[y][x] != '1'

# Function to move the ghost towards Pac-Man
def move_ghost():
    global ghost_pos
    ghost_x, ghost_y = ghost_pos
    pacman_x, pacman_y = pacman_pos

    # Calculate direction towards Pac-Man
    if ghost_x < pacman_x and is_valid_position(ghost_x + 1, ghost_y):
        ghost_x += 1
    elif ghost_x > pacman_x and is_valid_position(ghost_x - 1, ghost_y):
        ghost_x -= 1
    elif ghost_y < pacman_y and is_valid_position(ghost_x, ghost_y + 1):
        ghost_y += 1
    elif ghost_y > pacman_y and is_valid_position(ghost_x, ghost_y - 1):
        ghost_y -= 1

    ghost_pos = [ghost_x, ghost_y]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Pac-Man movement
    keys = pygame.key.get_pressed()
    new_pacman_pos = pacman_pos.copy()
    if keys[pygame.K_UP]:
        new_pacman_pos[1] -= 1
    if keys[pygame.K_DOWN]:
        new_pacman_pos[1] += 1
    if keys[pygame.K_LEFT]:
        new_pacman_pos[0] -= 1
    if keys[pygame.K_RIGHT]:
        new_pacman_pos[0] += 1

    # Check if the new position is valid
    if is_valid_position(new_pacman_pos[0], new_pacman_pos[1]):
        pacman_pos = new_pacman_pos

    # Move the ghost
    move_ghost()

    # Check if Pac-Man collides with a pellet
    for pellet in pellets[:]:
        if (pacman_pos[0], pacman_pos[1]) == pellet:
            pellets.remove(pellet)

    # Check if Pac-Man collides with the ghost
    if pacman_pos == ghost_pos:
        print("Game Over!")
        running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the maze
    draw_maze()

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2, pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

    # Draw the ghost
    pygame.draw.circle(screen, RED, (ghost_pos[0] * TILE_SIZE + TILE_SIZE // 2, ghost_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

    # Draw pellets
    for pellet in pellets:
        pygame.draw.circle(screen, WHITE, (pellet[0] * TILE_SIZE + TILE_SIZE // 2, pellet[1] * TILE_SIZE + TILE_SIZE // 2), 3)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
sys.exit()
