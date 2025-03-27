
import tkinter as tk
from Models.game import Game
import time


class Game:


    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        


    def start_game(self, niveau):

        rows, cols, mines = self.difficulty[niveau]
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = Board(rows, cols, mines)
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.flags_count = 0

    def on_left_click(self, x, y):
        if not self.grid.mines_placed:
            self.grid.place_mines((x, y))
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

        self.grid.reveal_case(x, y)
        self.update_board()

        if self.grid.grid[x][y].mine:
            self.end_game(False)
        else:
            self.check_victory()

    def on_right_click(self, x, y):
        case = self.grid.grid[x][y]
        btn = self.buttons[x][y]

        if case.revealed:
            return

        if case.flag is None:
            case.flag = "X"
            btn.config(text="X", bg=self.colors["flag"])
            self.flags_count += 1
        elif case.flag == "X":
            case.flag = "?"
            btn.config(text="?", bg="yellow")
            self.flags_count -= 1
        else:
            case.flag = None
            btn.config(text="", bg=self.colors["unrevealed"])

        self.flag_label.config(text=f"Drapeaux : {self.flags_count}")


    def update_board(self):
        for x in range(self.rows):
            for y in range(self.cols):
                case = self.grid.grid[x][y]
                btn = self.buttons[x][y]

                if case.revealed:
                    btn.config(bg=self.colors["revealed"], state="disabled")
                    if case.mine:
                        btn.config(bg=self.colors["mine"])
                    elif case.adjacent_mines > 0:
                        btn.config(text=str(case.adjacent_mines), fg=self.colors["numbers"][case.adjacent_mines])

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
