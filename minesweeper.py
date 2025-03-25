import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

class Cell:
    """different etat de la cellule"""
    def __init__(self, mine=False):
        self.mine = mine
        self.trou = True
        self.voisine = 0
        
        
class Grid:
    """definir la grille et l'état des cellules (si bombe, et nombre ou vide)"""
    def __init__(self, taille, nb_mine):
        self.taille = taille
        self.nb_mine = nb_mine
        self.cases = [[Cell() for _ in range(taille)] for _ in range(taille)]
        self.poser_balise()
        self.calc_voisine()


class Game:
    """programmer le jeu"""
    def __init__(self, taille=0, nb_mine=0):
        self.grid = Grid(taille, nb_mine)
    
    
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()