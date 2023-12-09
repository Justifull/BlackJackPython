import pygame as pg
from layoutessentials import scale_image
from carddeck import Carddeck


class BlackJackGame:
    def __init__(self):
        self.tokens = []
        position = 190
        for token in [1, 5, 25, 100, 500, 1000, 5000, 10000]:
            original_image = pg.image.load(f'graphics/tokens/{token}.png')
            scaled_image = scale_image(original_image, 85, 85)

            self.tokens.append([scaled_image, [160, position], token])
            position += 90

        self.bet_tokens = []
        self.carddeck = Carddeck()
        self.carddeck.shuffle()
        self.ready = False
        self.game_over = False
        self.game_won = 0

        self.unused_card_stack = []
        self.unused_card_stack.extend(self.get_carddeck())
        position = 100
        for card in self.unused_card_stack:
            self.unused_card_stack[self.unused_card_stack.index(card)] = (card, (pg.image.load('graphics/cards/Back.png'), (position, 100)))
            position += 10

    def get_tokens(self):
        return self.tokens

    def is_won(self):
        return self.game_won

    def add_bet_token(self, token):
        self.bet_tokens.append(token)

    def get_bet_token_value(self):
        calc_value = 0
        for bet_token_value in self.bet_tokens:
            calc_value += bet_token_value[2]
        return calc_value

    def take_card(self):
        card = self.carddeck.take()
        self.update_card_stack()
        return card

    def make_ready(self):
        current = self.ready
        if current:
            self.ready = False
        else:
            self.ready = True

    def end_game(self):
        current = self.game_over
        if current:
            self.game_over = False
        else:
            self.game_over = True

    def won(self, value):
        self.game_won = value

    def get_bet_tokens(self):
        return self.bet_tokens

    def get_carddeck(self):
        return self.carddeck.cards

    def get_unused_card_stack(self):
        return self.unused_card_stack

    def update_card_stack(self):
        self.unused_card_stack.clear()
        self.unused_card_stack.extend(self.get_carddeck())
        position = 100
        for card in self.unused_card_stack:
            self.unused_card_stack[self.unused_card_stack.index(card)] = (card, (pg.image.load('graphics/cards/Back.png'), (position, 100)))
            position += 10

    def is_ready(self):
        return self.ready

    def is_over(self):
        return self.game_over

    def clear_bets(self):
        self.bet_tokens.clear()

    def remove_bet_token(self, token):
        self.bet_tokens.remove(token)
