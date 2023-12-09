import pygame as pg


class BlackJackPlayer:
    def __init__(self):
        self.dead = False
        self.stays = False
        self.cards = list()
        self.cards_images = list()

    def get_cards(self):
        return self.cards

    def get_card_images(self):
        return self.cards_images

    def is_staying(self):
        return self.stays

    def is_dead(self):
        return self.dead

    def add_card(self, card):
        self.cards.append(card)

    def stay(self):
        current = self.stays
        if current:
            self.stays = False
        else:
            self.stays = True

    def kill(self):
        current = self.dead
        if current:
            self.dead = False
        else:
            self.dead = True

    def update_cards(self, show_back_site, is_dealer):
        self.cards_images.clear()
        if is_dealer:
            position = 800
        else:
            position = 600
        for card in self.cards:
            if is_dealer:
                if show_back_site:
                    self.cards_images.append((pg.image.load('graphics/cards/Back.png'), (position, 100)))
                    position += 10
                else:
                    self.cards_images.append((pg.image.load(f'graphics/cards/{card[0]}/{card[1]}.png'), (position, 100)))
                    position += 100
            else:
                self.cards_images.append((pg.image.load(f'graphics/cards/{card[0]}/{card[1]}.png'), (position, 800)))
                position += 100
