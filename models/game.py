from Models.board import Board


import time


class Game:


    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        


    def start_game(self):

        rows, cols, mines = 12,12,10
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = Board(rows, cols, mines)
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.flags_count = 0
