from Models.cell import Cell
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




