import pygame
import sys
import random

# --- Constantes ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
MINES = 10

# --- Couleurs ---
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Démineur")
font = pygame.font.SysFont(None, 24)

# --- Classe Cellule ---
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.is_mine = False
        self.is_revealed = False
        self.adjacent_mines = 0

    def draw(self):
        color = DARK_GRAY if self.is_revealed else GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

        if self.is_revealed and self.adjacent_mines > 0 and not self.is_mine:
            text = font.render(str(self.adjacent_mines), True, BLACK)
            screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

# --- Fonctions utilitaires ---
def create_grid():
    return [[Cell(x, y) for y in range(ROWS)] for x in range(COLS)]

def place_mines(grid):
    mines_placed = 0
    while mines_placed < MINES:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if not grid[x][y].is_mine:
            grid[x][y].is_mine = True
            mines_placed += 1

def count_adjacent_mines(grid):
    for x in range(COLS):
        for y in range(ROWS):
            if grid[x][y].is_mine:
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        if grid[nx][ny].is_mine:
                            count += 1
            grid[x][y].adjacent_mines = count

# --- Initialisation ---
grid = create_grid()
place_mines(grid)
count_adjacent_mines(grid)

# --- Boucle principale ---
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            cell = grid[gx][gy]
            cell.is_revealed = True

    for row in grid:
        for cell in row:
            cell.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
