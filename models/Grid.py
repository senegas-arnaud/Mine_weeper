import pygame
from Cell import Cell

class Grid:
    """Définir la grille et l'état des cellules (si bombe, et nombre ou vide)"""
    def __init__(self, taille, nb_mine):
        self.taille = taille
        self.nb_mine = nb_mine
        self.cases = [[Cell() for _ in range(taille)] for _ in range(taille)]
        # self.poser_balise()
        # self.calc_voisine()

    def afficher(self, screen):
        """Affiche la grille"""
        cell_size = 50
        gray = (200, 200, 200)
        black = (0, 0, 0)

        for x in range(self.taille):
            for y in range(self.taille):
                rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, gray, rect)
                pygame.draw.rect(screen, black, rect, 2)
