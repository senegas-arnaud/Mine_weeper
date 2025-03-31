from cell import Cell
import random

class Board:
    def __init__(self, rows, cols, mines):
        self.rows, self.cols = rows, cols
        self.mines = mines
        self.grid = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
        self.mines_placed = False

    def place_mines(self, first_click):
        positions = [(x, y) for x in range(self.rows) for y in range(self.cols)]
        positions.remove(first_click)
        mine_positions = random.sample(positions, self.mines)
        
        for x, y in mine_positions:
            self.grid[x][y].mine = True

        self.calculate_adjacent_mines()
        self.mines_placed = True

    def calculate_adjacent_mines(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y].mine:
                    continue
                count = sum(
                    self.grid[nx][ny].mine
                    for nx in range(max(0, x-1), min(self.rows, x+2))
                    for ny in range(max(0, y-1), min(self.cols, y+2))
                    if (nx, ny) != (x, y)
                )
                self.grid[x][y].adjacent_mines = count

    def reveal_case(self, x, y):
        if self.grid[x][y].revealed or self.grid[x][y].flag:
            return
        
        self.grid[x][y].revealed = True
        if self.grid[x][y].adjacent_mines == 0 and not self.grid[x][y].mine:
            for nx in range(max(0, x-1), min(self.rows, x+2)):
                for ny in range(max(0, y-1), min(self.cols, y+2)):
                    if (nx, ny) != (x, y):
                        self.reveal_case(nx, ny)



