import pygame
from utils import *

class Card:
    def __init__(self, rank, suit, image, back_image):
        self.rank = rank
        self.suit = suit
        self.image = image
        self.back_image = back_image
        self.rect = self.image.get_rect()
        self.face_up = False

    def draw(self, surface, pos):
        x, y = pos
        self.rect.topleft = (x, y)
        surface.blit(self.image if self.face_up else self.back_image, (x, y))

    def color(self):
        return COLOR_OF_SUIT[self.suit]
    
class Pile:
    def __init__(self, pos):
        self.cards = []
        self.pos = pos

    def size(self):
        return len(self.cards)

    def top(self):
        return self.cards[-1] if self.cards else None

    def add(self, cards):
        if isinstance(cards, list):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)

    def remove_from(self, index):
        sub = self.cards[index:]
        self.cards = self.cards[:index]
        return sub

    def draw(self, surface, spacing=30, is_foundation = False):
        x, y = self.pos
        if not self.cards and is_foundation:
            pygame.draw.rect(surface, (240,240,240), (x,y,CARD_WIDTH,CARD_HEIGHT), 4, border_radius=6)
            
        else:
            for i,card in enumerate(self.cards):
                card.draw(surface, (x, y + i*spacing))