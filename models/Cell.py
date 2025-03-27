class Cell:
    """Différents états de la cellule"""
    def __init__(self, mine=False):
        self.mine = mine
        self.trou = True
        self.voisine = 0