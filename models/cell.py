class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mine = False
        self.revealed = False
        self.flag = None
        self.adjacent_mines = 0