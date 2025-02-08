import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40
COLS = 15
ROWS = 15
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 30
GHOST_ACTIVATION_SCORE = 100

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Simple maze layout (1: wall, 0: path with pellet, 2: empty path)
LAYOUT = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Pacman:
    def __init__(self):
        self.row = 1
        self.col = 1
        self.direction = [0, 0]
        self.score = 0

    def move(self):
        new_row = self.row + self.direction[0]
        new_col = self.col + self.direction[1]

        if (0 <= new_row < ROWS and
            0 <= new_col < COLS and
            LAYOUT[new_row][new_col] != 1):
            self.row = new_row
            self.col = new_col

            # Collect pellet
            if LAYOUT[self.row][self.col] == 0:
                LAYOUT[self.row][self.col] = 2
                self.score += 10

class Ghost:
    def __init__(self):
        self.row = 7
        self.col = 7

    def move(self, pacman):
        # Only move if score is high enough
        if pacman.score < GHOST_ACTIVATION_SCORE:
            return

        # Simple ghost AI that tries to move toward Pacman
        moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        best_move = None
        min_distance = float('inf')

        for move in moves:
            new_row = self.row + move[0]
            new_col = self.col + move[1]

            if (0 <= new_row < ROWS and
                0 <= new_col < COLS and
                LAYOUT[new_row][new_col] != 1):
                # Calculate distance to Pacman
                distance = abs(new_row - pacman.row) + abs(new_col - pacman.col)
                if distance < min_distance:
                    min_distance = distance
                    best_move = move

        if best_move:
            self.row += best_move[0]
            self.col += best_move[1]

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Pac-Man")
    clock = pygame.time.Clock()

    pacman = Pacman()
    ghost = Ghost()

    running = True
    game_over = False

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    pacman.direction = [-1, 0]
                elif event.key == pygame.K_DOWN:
                    pacman.direction = [1, 0]
                elif event.key == pygame.K_LEFT:
                    pacman.direction = [0, -1]
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = [0, 1]

        if not game_over:
            # Update game state
            pacman.move()
            ghost.move(pacman)

            # Check collision with ghost
            if ghost.row == pacman.row and ghost.col == pacman.col:
                game_over = True

        # Draw everything
        screen.fill(BLACK)

        # Draw maze and pellets
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                if LAYOUT[row][col] == 1:
                    pygame.draw.rect(screen, BLUE,
                                   (x, y, CELL_SIZE, CELL_SIZE))
                elif LAYOUT[row][col] == 0:
                    pygame.draw.circle(screen, WHITE,
                                     (x + CELL_SIZE//2, y + CELL_SIZE//2),
                                     CELL_SIZE//8)

        # Draw Pacman
        pygame.draw.circle(screen, YELLOW,
                         (pacman.col * CELL_SIZE + CELL_SIZE//2,
                          pacman.row * CELL_SIZE + CELL_SIZE//2),
                         CELL_SIZE//2 - 2)

        # Draw Ghost
        pygame.draw.circle(screen, RED,
                         (ghost.col * CELL_SIZE + CELL_SIZE//2,
                          ghost.row * CELL_SIZE + CELL_SIZE//2),
                         CELL_SIZE//2 - 2)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {pacman.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw warning message when ghost is about to activate
        if pacman.score < GHOST_ACTIVATION_SCORE:
            points_needed = GHOST_ACTIVATION_SCORE - pacman.score
            font = pygame.font.Font(None, 36)
            warning_text = font.render(f'Ghost activates in {points_needed} points!', True, WHITE)
            screen.blit(warning_text,
                       (WIDTH//2 - warning_text.get_width()//2,
                        HEIGHT - 40))

        # Draw game over
        if game_over:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('Game Over!', True, WHITE)
            screen.blit(game_over_text,
                       (WIDTH//2 - game_over_text.get_width()//2,
                        HEIGHT//2 - game_over_text.get_height()//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
