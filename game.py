import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 40)

# Function to draw the Sudoku grid
def draw_grid():
    cell_size = WIDTH // 12
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(SCREEN, BLACK, (0, i * cell_size), (WIDTH - 5 - WIDTH/4, i * cell_size), 3)
            pygame.draw.line(SCREEN, BLACK, (i * cell_size, 0), (i * cell_size, WIDTH), 3)
        else:
            pygame.draw.line(SCREEN, BLACK, (0, i * cell_size), (WIDTH - 5 - WIDTH/4, i * cell_size), 1)
            pygame.draw.line(SCREEN, BLACK, (i * cell_size, 0), (i * cell_size, WIDTH), 1)

# Function to draw numbers onto the grid
def draw_numbers():
    cell_size = WIDTH // 12
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                SCREEN.blit(text, text_rect)

# Function to check if the move is valid
def is_valid_move(row, col, num):
    # Check row
    if num in grid[row]:
        return False
    # Check column
    if num in [grid[i][col] for i in range(9)]:
        return False
    # Check 3x3 square
    square_row, square_col = 3 * (row // 3), 3 * (col // 3)
    if num in [grid[i][j] for i in range(square_row, square_row + 3) for j in range(square_col, square_col + 3)]:
        return False
    return True

# Function to solve Sudoku using backtracking
def solve_sudoku():
    empty_cell = find_empty_cell()
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(row, col, num):
            grid[row][col] = num
            if solve_sudoku():
                return True
            grid[row][col] = 0
    return False

# Function to find an empty cell
def find_empty_cell():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

# Function to generate a random Sudoku puzzle
def generate_sudoku():
    solve_sudoku()  # Start with a solved puzzle
    # Remove numbers to create a puzzle
    for _ in range(45):  # Adjust difficulty by changing the number of iterations
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0

# Button class for GUI
class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text=''):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)

# Initialize grid
grid = [[0] * 9 for _ in range(9)]

# Initialize buttons
button_width, button_height = 200, 100
start_button = Button(GRAY, WIDTH - WIDTH/4, 50, button_width, button_height, 'Start')
pause_button = Button(GRAY, WIDTH - WIDTH/4, 200, button_width, button_height, 'Pause')
quit_button = Button(GRAY, WIDTH - WIDTH/4, 350, button_width, button_height, 'Quit')

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    SCREEN.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                generate_sudoku()
            elif pause_button.rect.collidepoint(event.pos):
                # Your pause logic here
                pass
            elif quit_button.rect.collidepoint(event.pos):
                running = False
        elif event.type == pygame.KEYDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // (HEIGHT // 9)
            col = x // (WIDTH // 12)
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                num = event.key - pygame.K_1 + 1
                if is_valid_move(row, col, num):
                    grid[row][col] = num
                else:
                    SCREEN.fill(RED)  # Fill the screen with red
                    pygame.display.flip()
                    pygame.time.wait(100)  # Wait for 100 milliseconds
                    SCREEN.fill(WHITE)  # Fill the screen with background color
                    pygame.display.flip()
            elif event.key == pygame.K_BACKSPACE:
                grid[row][col] = 0

    draw_grid()
    draw_numbers()

    # Draw buttons
    start_button.draw(SCREEN)
    pause_button.draw(SCREEN)
    quit_button.draw(SCREEN)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
