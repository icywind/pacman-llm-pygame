import pygame
import sys
import random

# Window dimensions
WIDTH, HEIGHT = 640, 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Pac-Man properties
PACMAN_SIZE = 20
PACMAN_SPEED = 5

# Ghost properties
GHOST_SIZE = 20
GHOST_SPEED = 3

# Pellet properties
PELLET_SIZE = 5

class PacMan:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 0
        self.vy = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Boundary collision detection
        if self.x < 0 or self.x > WIDTH - PACMAN_SIZE:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT - PACMAN_SIZE:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), PACMAN_SIZE // 2)

class Ghost:
    def __init__(self):
        self.x = random.randint(0, WIDTH - GHOST_SIZE)
        self.y = random.randint(0, HEIGHT - GHOST_SIZE)
        self.vx = random.choice([-GHOST_SPEED, GHOST_SPEED])
        self.vy = random.choice([-GHOST_SPEED, GHOST_SPEED])

    def update(self, pacman):
        if pacman.x < self.x:
            self.vx = -GHOST_SPEED
        elif pacman.x > self.x:
            self.vx = GHOST_SPEED
        if pacman.y < self.y:
            self.vy = -GHOST_SPEED
        elif pacman.y > self.y:
            self.vy = GHOST_SPEED

        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), GHOST_SIZE // 2)

class Pellet:
    def __init__(self):
        self.x = random.randint(0, WIDTH - PELLET_SIZE)
        self.y = random.randint(0, HEIGHT - PELLET_SIZE)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), PELLET_SIZE // 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pacman = PacMan()
    ghost = Ghost()
    pellets = [Pellet() for _ in range(10)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.vx = -PACMAN_SPEED
                    pacman.vy = 0
                elif event.key == pygame.K_RIGHT:
                    pacman.vx = PACMAN_SPEED
                    pacman.vy = 0
                elif event.key == pygame.K_UP:
                    pacman.vx = 0
                    pacman.vy = -PACMAN_SPEED
                elif event.key == pygame.K_DOWN:
                    pacman.vx = 0
                    pacman.vy = PACMAN_SPEED

        screen.fill(BLACK)

        pacman.update()
        pacman.draw(screen)

        ghost.update(pacman)
        ghost.draw(screen)

        for pellet in pellets:
            pellet.draw(screen)
            if (pacman.x - pellet.x) ** 2 + (pacman.y - pellet.y) ** 2 < (PACMAN_SIZE // 2 + PELLET_SIZE // 2) ** 2:
                pellets.remove(pellet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
