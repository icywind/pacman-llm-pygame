import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game objects
pacman = pygame.Rect(300, 300, 20, 20)
ghost = pygame.Rect(100, 100, 20, 20)

# Score
score = 0

# Pellets
pellets = []
for i in range(100):
    x = random.randint(0, WIDTH - 10) // 10 * 10
    y = random.randint(0, HEIGHT - 10) // 10 * 10
    pellets.append(pygame.Rect(x, y, 10, 10))

# Maze walls
walls = [
    pygame.Rect(0, 0, WIDTH, 10),  # Top wall
    pygame.Rect(0, 0, 10, HEIGHT),  # Left wall
    pygame.Rect(WIDTH - 10, 0, 10, HEIGHT),  # Right wall
    pygame.Rect(0, HEIGHT - 10, WIDTH, 10),  # Bottom wall
    pygame.Rect(100, 100, 400, 10),  # Horizontal middle wall
    pygame.Rect(100, 500, 400, 10),  # Horizontal middle wall
    pygame.Rect(100, 100, 10, 400),  # Vertical middle wall
    pygame.Rect(500, 100, 10, 400),  # Vertical middle wall
]

# Ghost movement flag
ghost_moving = False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement keys for Pac-Man
    keys = pygame.key.get_pressed()
    new_x, new_y = pacman.x, pacman.y

    if keys[pygame.K_LEFT]:
        new_x -= 5
    if keys[pygame.K_RIGHT]:
        new_x += 5
    if keys[pygame.K_UP]:
        new_y -= 5
    if keys[pygame.K_DOWN]:
        new_y += 5

    # Check for wall collision for Pac-Man
    new_pacman = pygame.Rect(new_x, new_y, pacman.width, pacman.height)
    if not any(new_pacman.colliderect(wall) for wall in walls):
        pacman.x, pacman.y = new_x, new_y

    # Eating pellets
    for pellet in pellets[:]:
        if pacman.colliderect(pellet):
            pellets.remove(pellet)
            score += 10

    # Ghost movement logic
    if score >= 100:
        ghost_moving = True

    if ghost_moving:
        # Move ghost towards Pac-Man
        if ghost.x < pacman.x:
            ghost.x += 2
        elif ghost.x > pacman.x:
            ghost.x -= 2

        if ghost.y < pacman.y:
            ghost.y += 2
        elif ghost.y > pacman.y:
            ghost.y -= 2

    # Check for ghost collision
    if pacman.colliderect(ghost):
        print(f"Game Over! Your score: {score}")
        running = False

    # Drawing
    screen.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)
    for pellet in pellets:
        pygame.draw.rect(screen, WHITE, pellet)
    pygame.draw.rect(screen, YELLOW, pacman)
    pygame.draw.rect(screen, RED, ghost)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
