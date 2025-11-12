import pygame
import random
from utils import *
from card import *

class SolitaireGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 18)
        self.card_images = {}
        self.card_back = None
        self.bg = None
        self.won = None
        self.reset_stock = None
        self.load_assets()
        self.stock = Pile(STOCK_POS)
        self.waste = Pile(WASTE_POS)
        self.foundations = [Pile((FOUNDATION_X[i], FOUNDATION_Y)) for i in range(4)]
        self.tableau = [Pile((TABLEAU_X[i], TABLEAU_Y)) for i in range(7)]
        self.undo_stack = []
        self.score = 0
        self.moves = 0
        self.dragging = None
        self.create_new_game()

    def load_assets(self):
        bg_img = pygame.image.load("assets/bg.jpg")
        self.bg = pygame.transform.smoothscale(bg_img, (SCREEN_W,SCREEN_H))
        
        won_img = pygame.image.load("assets/won.png")
        self.won = pygame.transform.smoothscale(won_img, (SCREEN_W,SCREEN_H))

        reset_img = pygame.image.load("assets/reset.png")
        self.reset_stock = pygame.transform.smoothscale(reset_img, (CARD_WIDTH,CARD_HEIGHT-40))

        back_image = pygame.image.load('assets/card_back.png')
        self.card_back = pygame.transform.smoothscale(back_image, (CARD_WIDTH,CARD_HEIGHT))

        for s in SUITS:
            for r in RANKS:
                card_image = pygame.image.load(f"assets/cards/{r}{s}.png")
                temp = card_image.convert_alpha()
                temp = pygame.transform.smoothscale(temp, (CARD_WIDTH, CARD_HEIGHT))
                self.card_images[f"{r}{s}"] = temp

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
            self.screen.blit(self.reset_stock, (self.stock.pos[0], self.stock.pos[1]))
            
        if self.waste.top():
            self.waste.top().draw(self.screen, self.waste.pos)

        for t in self.tableau:
            t.draw(self.screen)

        if self.dragging:
            for i, card in enumerate(self.dragging):
                pos = pygame.mouse.get_pos()
                x, y = pos[0] - 50 , pos[1] + i*20 -70
                card.draw(self.screen, (x, y))

        if self.win():
            self.screen.blit(self.won,(0,0))

        pygame.display.flip()

    def win(self):
        for pile in self.tableau:
            for card in pile.cards:
                if card.face_up != False:
                    return False
        return True

    def run(self):
        running = True
        dragging_cards = []
        dragging_from = None
        
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                if e.type == pygame.KEYDOWN and self.win():
                    self.create_new_game()

                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    for pile in reversed(self.tableau):
                        for i, card in enumerate(pile.cards):
                            if card.face_up and card.rect.collidepoint(mx, my):
                                dragging_cards = pile.remove_from(i)
                                dragging_from = pile
                                break
                        if dragging_cards:
                            self.dragging = dragging_cards
                            break

                    if not dragging_cards and self.waste.top() and self.waste.top().rect.collidepoint(mx, my):
                        card = self.waste.cards.pop()
                        dragging_cards = [card]
                        dragging_from = self.waste
                    
                    if not dragging_cards and self.stock.top() and self.stock.top().rect.collidepoint(mx, my):
                        card = self.stock.top()
                        self.stock.cards.pop()
                        card.face_up = True
                        self.waste.add(card)

                    elif not dragging_cards and not self.stock.cards:
                        stock_rect = pygame.Rect(self.stock.pos, (CARD_WIDTH, CARD_HEIGHT))
                        if stock_rect.collidepoint(mx, my):
                            while self.waste.cards:
                                c = self.waste.cards.pop()
                                c.face_up = False
                                self.stock.add(c)

                    if dragging_cards:
                        self.dragging = dragging_cards
                        break

                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and dragging_cards:
                    mx, my = e.pos
                    dropped = False
                    self.dragging = []

                    for pile in self.tableau:
                        if pile.cards:
                            target = pile.cards[-1]
                            if target.rect.collidepoint(mx, my) and self.can_place_on_tableau(dragging_cards[0], target):
                                pile.add(dragging_cards)
                                dropped = True
                                break
                        else:
                            rect = pygame.Rect(pile.pos, (CARD_WIDTH, CARD_HEIGHT))
                            if rect.collidepoint(mx, my) and self.can_place_on_tableau(dragging_cards[0], None):
                                pile.add(dragging_cards)
                                dropped = True
                                break
                   
                    if not dropped:
                        for pile in self.foundations:
                            rect = pygame.Rect(pile.pos, (CARD_WIDTH, CARD_HEIGHT))
                            if rect.collidepoint(mx, my) and self.can_place_on_foundation(dragging_cards[0], pile):
                                pile.add(dragging_cards)
                                dropped = True
                                break

                    if not dropped and dragging_from:
                        dragging_from.add(dragging_cards)

                    if dragging_from and dragging_from.cards:
                        dragging_from.cards[-1].face_up = True

                    dragging_cards = []
                    dragging_from = None
            
            self.draw()
            self.win()
            
        pygame.quit()

