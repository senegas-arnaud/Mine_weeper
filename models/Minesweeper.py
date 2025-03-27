import tkinter as tk
import random
from tkinter import messagebox

class Case:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mine = False
        self.revealed = False
        self.adjacent_mines = 0

class Grille:
    def __init__(self, rows, cols, mines):
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = [[Case(x, y) for y in range(cols)] for x in range(rows)]
        self.mines_placed = False

    def place_mines(self, first_click):
        positions = [(x, y) for x in range(self.rows) for y in range(self.cols)]
        positions.remove(first_click)
        for x, y in random.sample(positions, self.mines):
            self.grid[x][y].mine = True
        self.calculate_adjacent_mines()
        self.mines_placed = True

    def calculate_adjacent_mines(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if not self.grid[x][y].mine:
                    self.grid[x][y].adjacent_mines = sum(
                        self.grid[nx][ny].mine
                        for nx in range(max(0, x-1), min(self.rows, x+2))
                        for ny in range(max(0, y-1), min(self.cols, y+2))
                        if (nx, ny) != (x, y)
                    )

    def reveal_case(self, x, y):
        if self.grid[x][y].revealed or self.grid[x][y].mine:
            return
        self.grid[x][y].revealed = True
        if self.grid[x][y].adjacent_mines == 0:
            for nx in range(max(0, x-1), min(self.rows, x+2)):
                for ny in range(max(0, y-1), min(self.cols, y+2)):
                    if not self.grid[nx][ny].revealed:
                        self.reveal_case(nx, ny)

class Démineur:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.rows, self.cols, self.mines = 8, 8, 10
        self.grid = Grille(self.rows, self.cols, self.mines)
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_board()

    def on_left_click(self, x, y):
        if not self.grid.mines_placed:
            self.grid.place_mines((x, y))

        if self.grid.grid[x][y].mine:
            messagebox.showinfo("Game Over", "Vous avez perdu !")
            self.reset_game()
            return

        self.grid.reveal_case(x, y)
        self.update_board()

    def create_board(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for x in range(self.rows):
            for y in range(self.cols):
                btn = tk.Button(self.frame, width=3, height=1, font=("Arial", 14),
                                command=lambda x=x, y=y: self.on_left_click(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

    def update_board(self):
        for x in range(self.rows):
            for y in range(self.cols):
                case = self.grid.grid[x][y]
                btn = self.buttons[x][y]
                if case.revealed:
                    btn.config(text=str(case.adjacent_mines) if case.adjacent_mines > 0 else "", state="disabled")

    def reset_game(self):
        self.frame.destroy()
        self.__init__(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    game = Démineur(root)
    root.mainloop()
