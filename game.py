import pygame
import random
from utils import *
from card import *

class SolitaireGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.card_images = {}
        self.card_back = None
        self.bg = None
        self.reset_stock = None
        self.win_img = None
        self.load_assets()
        self.stock = Pile(STOCK_POS)
        self.waste = Pile(WASTE_POS)
        self.foundations = [Pile((FOUNDATION_X[i], FOUNDATION_Y)) for i in range(4)]
        self.tableau = [Pile((TABLEAU_X[i], TABLEAU_Y)) for i in range(7)]
        self.dragging = []
        self.dragging_from = None
        self.create_new_game()
        self.won = False

    def load_assets(self):
        bg_img = pygame.image.load("assets/bg.jpg")
        self.bg = pygame.transform.smoothscale(bg_img, (SCREEN_W,SCREEN_H))
        
        won_img = pygame.image.load("assets/won.png")
        self.win_img = pygame.transform.smoothscale(won_img, (SCREEN_W,SCREEN_H))

        reset_img = pygame.image.load("assets/reset.png")
        self.reset_stock = pygame.transform.smoothscale(reset_img, (CARD_WIDTH,CARD_HEIGHT))

        back_image = pygame.image.load('assets/card_back.png')
        self.card_back = pygame.transform.smoothscale(back_image, (CARD_WIDTH,CARD_HEIGHT))

        for s in SUITS:
            for r in RANKS:
                card_image = pygame.image.load(f"assets/cards/{r}{s}.png")
                self.card_images[f"{r}{s}"] = pygame.transform.smoothscale(card_image, (CARD_WIDTH, CARD_HEIGHT))

    def create_deck(self):
        deck = []
        for s in SUITS:
            for r in RANKS:
                img = self.card_images.get(f"{r}{s}")
                c = Card(r, s, img, self.card_back)
                deck.append(c)
        random.shuffle(deck)
        return deck

    def create_new_game(self):
        for p in [self.stock, self.waste] + self.foundations + self.tableau:
            p.cards.clear()
        deck = self.create_deck()
        for i in range(7):
            for j in range(i+1):
                c = deck.pop()
                c.face_up = (j==i)
                self.tableau[i].add(c)
        while deck:
            c = deck.pop()
            c.face_up = False
            self.stock.add(c)

    def can_place_on_tableau(self, moving, dest):
        if dest is None:
            return moving.rank==13
        return moving.color()!=dest.color() and moving.rank==dest.rank-1

    def can_place_on_foundation(self, moving, pile):
        top = pile.top()
        if top is None:
            return moving.rank==1
        return moving.suit==top.suit and moving.rank==top.rank+1

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for f in self.foundations:
            f.draw(self.screen, spacing=0 , is_foundation = True)

        if self.stock.top():
            self.stock.top().draw(self.screen, self.stock.pos)
        else:
            self.screen.blit(self.reset_stock, self.stock.pos)
            
        if self.waste.top():
            self.waste.top().draw(self.screen, self.waste.pos)

        for t in self.tableau:
            t.draw(self.screen)

        if self.dragging:
            for i, card in enumerate(self.dragging):
                mx, my = pygame.mouse.get_pos()
                x, y = mx - 50 , my + i*20 -70
                card.draw(self.screen, (x, y))
            
        if self.won:
            self.screen.blit(self.win_img, (0,0))

        pygame.display.flip()

    def win(self):
        for pile in self.tableau:
            for card in pile.cards:
                if not card.face_up:
                    self.won = False
                    return None
        self.won = True

    def run(self):
        running = True
        
        while running:
            self.win()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                
                if self.won:
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        mx, my = e.pos
                        new_game_rect = pygame.Rect((310, 490), (380, 130))
                        if new_game_rect.collidepoint(mx, my):
                            self.create_new_game()
                            self.won = False

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    for pile in reversed(self.tableau):
                        for i, card in enumerate(pile.cards):
                            if card.face_up and card.rect.collidepoint(mx, my):
                                self.dragging = pile.remove_from(i)
                                self.dragging_from = pile
                                break

                    if not self.dragging and self.waste.top() and self.waste.top().rect.collidepoint(mx, my):
                        card = self.waste.cards.pop()
                        self.dragging = [card]
                        self.dragging_from = self.waste
                    
                    if not self.dragging and self.stock.top() and self.stock.top().rect.collidepoint(mx, my):
                        card = self.stock.top()
                        self.stock.cards.pop()
                        card.face_up = True
                        self.waste.add(card)

                    elif not self.dragging and not self.stock.cards:
                        stock_rect = pygame.Rect(self.stock.pos, (CARD_WIDTH, CARD_HEIGHT))
                        if stock_rect.collidepoint(mx, my):
                            while self.waste.cards:
                                c = self.waste.cards.pop()
                                c.face_up = False
                                self.stock.add(c)

                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dragging:
                    mx, my = e.pos
                    dropped = False

                    for pile in self.tableau:
                        if pile.cards:
                            target = pile.top()
                            if target.rect.collidepoint(mx, my) and self.can_place_on_tableau(self.dragging[0], target):
                                pile.add(self.dragging)
                                dropped = True
                                break
                        else:
                            rect = pygame.Rect(pile.pos, (CARD_WIDTH, CARD_HEIGHT))
                            if rect.collidepoint(mx, my) and self.can_place_on_tableau(self.dragging[0], None):
                                pile.add(self.dragging)
                                dropped = True
                                break
                   
                    for pile in self.foundations:
                        rect = pygame.Rect(pile.pos, (CARD_WIDTH, CARD_HEIGHT))
                        if rect.collidepoint(mx, my) and self.can_place_on_foundation(self.dragging[0], pile):
                            pile.add(self.dragging)
                            dropped = True
                            break

                    if not dropped and self.dragging_from:
                        self.dragging_from.add(self.dragging)

                    if self.dragging_from and self.dragging_from.cards:
                        self.dragging_from.top().face_up = True

                    self.dragging = []
                    self.dragging_from = None

            self.draw()
            self.clock.tick(FPS)
