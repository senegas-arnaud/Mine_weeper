import tkinter as tk
from tkinter import messagebox
import time
from grid import Grid

class Minesweeper:
    DIFFICULTIES = {
        "Easy": (8, 8, 10),
        "Medium": (12, 12, 25),
        "Hard": (16, 16, 40)
    }

    COLORS = {
        "unrevealed": "#A3D977",
        "revealed": "#D2B48C",
        "mine": "#FF0000",
        "flag": "#FF8C00",
        "numbers": ["", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Choose a difficulty:", font=("Arial", 14)).pack()
        
        for level in self.DIFFICULTIES.keys():
            tk.Button(self.menu_frame, text=level, font=("Arial", 12), command=lambda l=level: self.start_game(l)).pack(pady=5)

    def start_game(self, level):
        self.menu_frame.destroy()
        rows, cols, mines = self.DIFFICULTIES[level]
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = Grid(rows, cols, mines)
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.start_time = None
        self.timer_running = False
        self.flags_count = 0
        self.create_widgets()

    def create_widgets(self):
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack()

        self.timer_label = tk.Label(self.frame_top, text="Time: 0s", font=("Arial", 14))
        self.timer_label.pack(side="left", padx=10)

        self.mine_label = tk.Label(self.frame_top, text=f"Mines: {self.mines}", font=("Arial", 14))
        self.mine_label.pack(side="left", padx=10)

        self.flag_label = tk.Label(self.frame_top, text=f"Flags: 0", font=("Arial", 14))
        self.flag_label.pack(side="left", padx=10)

        self.reset_button = tk.Button(self.frame_top, text="Reset", font=("Arial", 12), command=self.reset_game)
        self.reset_button.pack(side="right", padx=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        for x in range(self.rows):
            for y in range(self.cols):
                btn = tk.Button(self.frame, width=3, height=1, font=("Arial", 14), bg=self.COLORS["unrevealed"],
                                command=lambda x=x, y=y: self.on_left_click(x, y))
                btn.bind("<Button-3>", lambda event, x=x, y=y: self.on_right_click(x, y))
                btn.grid(row=x, column=y, padx=1, pady=1)
                self.buttons[x][y] = btn

    def on_left_click(self, x, y):
        if not self.grid.mines_placed:
            self.grid.place_mines((x, y))
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

        self.grid.reveal_cell(x, y)
        self.update_board()

        if self.grid.grid[x][y].mine:
            self.end_game(False)
        else:
            self.check_victory()

    def update_board(self):
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.grid.grid[x][y]
                btn = self.buttons[x][y]

                if cell.revealed:
                    btn.config(bg=self.COLORS["revealed"], state="disabled")
                    if cell.mine:
                        btn.config(bg=self.COLORS["mine"])
                    elif cell.adjacent_mines > 0:
                        btn.config(text=str(cell.adjacent_mines), fg=self.COLORS["numbers"][cell.adjacent_mines])

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer)

    def check_victory(self):
        total_revealed = sum(1 for row in self.grid.grid for cell in row if cell.revealed)
        if total_revealed == self.rows * self.cols - self.mines:
            self.end_game(True)

    def end_game(self, won):
        self.timer_running = False
        messagebox.showinfo("Game Over", "Congratulations, you won!" if won else "Game Over!")

    def reset_game(self):
        self.frame.destroy()
        self.frame_top.destroy()
        self.start_game("Easy")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
