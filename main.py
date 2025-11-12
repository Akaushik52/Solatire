import pygame
from game import *
from utils import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Solitaire')
game = SolitaireGame(screen)
game.run()
pygame.quit()