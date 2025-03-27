import pygame
from Grid import Grid

class Game:
    """Programmer le jeu"""
    def __init__(self, taille=5, nb_mine=5):
        self.grid = Grid(taille, nb_mine)
        
        pygame.init()
        self.screen = pygame.display.set_mode((taille * 50, taille * 50))
        pygame.display.set_caption("Démineur")

    def run(self):
        """Boucle principale"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.grid.afficher(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
