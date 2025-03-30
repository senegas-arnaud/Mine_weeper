import tkinter as tk
from tkinter import messagebox
import random
import time

class Case:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mine = False
        self.revealed = False
        self.flag = None
        self.adjacent_mines = 0

class Grille:
    def __init__(self, rows, cols, mines):
        self.rows, self.cols = rows, cols
        self.mines = mines
        self.grid = [[Case(x, y) for y in range(cols)] for x in range(rows)]
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

class Démineur:
    DIFFICULTÉS = {
        "Facile": (8, 8, 10),
        "Moyen": (12, 12, 25),
        "Difficile": (16, 16, 40)
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
        self.root.title("Démineur")
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Choisissez un niveau :", font=("Arial", 14)).pack()
        
        for niveau in self.DIFFICULTÉS.keys():
            tk.Button(self.menu_frame, text=niveau, font=("Arial", 12), command=lambda n=niveau: self.start_game(n)).pack(pady=5)

    def start_game(self, niveau):
        self.menu_frame.destroy()
        rows, cols, mines = self.DIFFICULTÉS[niveau]
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = Grille(rows, cols, mines)
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.start_time = None
        self.timer_running = False
        self.flags_count = 0
        self.create_widgets()

    def create_widgets(self):
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack()

        self.timer_label = tk.Label(self.frame_top, text="Temps : 0s", font=("Arial", 14))
        self.timer_label.pack(side="left", padx=10)

        self.mine_label = tk.Label(self.frame_top, text=f"Mines : {self.mines}", font=("Arial", 14))
        self.mine_label.pack(side="left", padx=10)

        self.flag_label = tk.Label(self.frame_top, text=f"Drapeaux : 0", font=("Arial", 14))
        self.flag_label.pack(side="left", padx=10)

        self.reset_button = tk.Button(self.frame_top, text="Réinitialiser", font=("Arial", 12), command=self.reset_game)
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
            btn.config(text="X", bg=self.COLORS["flag"])
            self.flags_count += 1
        elif case.flag == "X":
            case.flag = "?"
            btn.config(text="?", bg="yellow")
            self.flags_count -= 1
        else:
            case.flag = None
            btn.config(text="", bg=self.COLORS["unrevealed"])

        self.flag_label.config(text=f"Drapeaux : {self.flags_count}")

    def update_board(self):
        for x in range(self.rows):
            for y in range(self.cols):
                case = self.grid.grid[x][y]
                btn = self.buttons[x][y]

                if case.revealed:
                    btn.config(bg=self.COLORS["revealed"], state="disabled")
                    if case.mine:
                        btn.config(bg=self.COLORS["mine"])
                    elif case.adjacent_mines > 0:
                        btn.config(text=str(case.adjacent_mines), fg=self.COLORS["numbers"][case.adjacent_mines])

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Temps : {elapsed_time}s")
            self.root.after(1000, self.update_timer)

    def check_victory(self):
        total_revealed = sum(1 for row in self.grid.grid for case in row if case.revealed)
        if total_revealed == self.rows * self.cols - self.mines:
            self.end_game(True)

    def end_game(self, won):
        self.timer_running = False
        messagebox.showinfo("Fin de partie", "Bravo, vous avez gagné !" if won else "Game Over !")

    def reset_game(self):
        self.frame.destroy()
        self.frame_top.destroy()
        self.start_game("Facile")

if __name__ == "__main__":
    root = tk.Tk()
    game = Démineur(root)
    root.mainloop()