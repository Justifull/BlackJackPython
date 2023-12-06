import pygame
from sys import exit
from carddeck import Carddeck
from carddeck import get_deck_value
import random
import json


player_stays = 0
game_ended = 0
card_deck = Carddeck()
bet_value = 0
bet_and_start = 0
round_over = 0
player_money = 0


def blackjack_window(username, password, money):
    global card_deck
    global bet_value
    global bet_and_start
    global round_over
    global player_money
    global game_ended

    accounts_data = "accounts.json"
    account_name = username
    account_password = password
    player_money = money

    def save():
        with open(accounts_data, 'r') as json_datei:
            loaded_data = json.load(json_datei)

        data = {}
        for account in loaded_data.keys():
            data.update({account: loaded_data[account]})

        data.update({account_name: [account_password, player_money]})

        with open(accounts_data, 'w') as json_datei:
            json.dump(data, json_datei)

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('BlackJack')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    background = pygame.image.load('graphics/background.jpg')

    max_width, max_height = 100, 100

    def draw_button(rect, text):
        pygame.draw.rect(screen, (255, 255, 255), rect)

        button_font = pygame.font.Font(None, 36)
        text_surface = button_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)

    def scale_image(image, max_width, max_height):
        width, height = image.get_size()

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)

            scaled_image = pygame.transform.scale(image, (int(width * ratio), int(height * ratio)))

            return scaled_image
        else:
            return image

    tokens = []
    position = 100
    for token in [1, 5, 25, 100, 500, 1000, 5000, 10000]:
        original_image = pygame.image.load(f'graphics/tokens/{token}.png')
        scaled_image = scale_image(original_image, max_width, max_height)

        tokens.append([scaled_image, [position, 100], token])
        position += 100

    all_in_button = pygame.Rect(position + 50, 125, 200, 50)

    bet_tokens = []

    card_deck.shuffle()

    card_stack = []
    card_stack_images = []

    def update_card_stack():
        card_stack.clear()
        card_stack_images.clear()
        card_stack.extend(card_deck.get_cards())
        position = 100
        for card in card_stack:
            card_stack_images.append([pygame.image.load('graphics/cards/Back.png'), [position, 100]])
            position += 10

    update_card_stack()

    dealer_cards = []
    dealer_cards_images = []

    def update_dealer_cards():
        dealer_cards_images.clear()
        position = 800
        for direct in dealer_cards:
            if player_stays == 1:
                dealer_cards_images.append(
                    [pygame.image.load(f'graphics/cards/{direct[0]}/{direct[1]}.png'), [position, 100]])
                position += 100
            else:
                dealer_cards_images.append(
                    [pygame.image.load('graphics/cards/Back.png'), [position, 100]])
                position += 10

    def dealer_take():
        dealer_cards.append(card_deck.take())
        update_dealer_cards()
        update_card_stack()

    dealer_take()

    player_cards = []
    player_cards_images = []

    def update_player_cards():
        player_cards_images.clear()
        position = 300
        for direct in player_cards:
            player_cards_images.append(
                [pygame.image.load(f'graphics/cards/{direct[0]}/{direct[1]}.png'), [position, 500]])
            position += 100

    update_player_cards()

    def button_click():
        player_cards.append(card_deck.take())
        update_player_cards()
        update_card_stack()

    def calc_tokens():
        global bet_value
        calc_value = 0
        for bet_token_value in bet_tokens:
            calc_value += bet_token_value[2]
        bet_value = calc_value

    def start_click():
        global bet_value
        global player_money
        global bet_and_start
        calc_tokens()
        bet_and_start = 1
        player_money -= bet_value
        bet_tokens.clear()

    def get_token_by_value(value):
        for token_value in tokens:
            if token_value[2] == value:
                return token_value

    def all_in():
        if player_money > bet_value:
            temp_value = bet_value
            while (temp_value + 10000) <= player_money:
                bet_tokens.append(get_token_by_value(10000))
                temp_value += 10000
            while (temp_value + 5000) <= player_money:
                bet_tokens.append(get_token_by_value(5000))
                temp_value += 5000
            while (temp_value + 1000) <= player_money:
                bet_tokens.append(get_token_by_value(1000))
                temp_value += 1000
            while (temp_value + 500) <= player_money:
                bet_tokens.append(get_token_by_value(500))
                temp_value += 500
            while (temp_value + 100) <= player_money:
                bet_tokens.append(get_token_by_value(100))
                temp_value += 100
            while (temp_value + 25) <= player_money:
                bet_tokens.append(get_token_by_value(25))
                temp_value += 25
            while (temp_value + 5) <= player_money:
                bet_tokens.append(get_token_by_value(5))
                temp_value += 5
            while (temp_value + 1) <= player_money:
                bet_tokens.append(get_token_by_value(1))
                temp_value += 1

    def again_click():
        global game_ended
        global player_stays
        global card_deck
        global bet_value
        global bet_and_start
        game_ended = 0
        player_stays = 0
        bet_value = 0
        bet_and_start = 0

        player_cards.clear()
        dealer_cards.clear()
        player_cards_images.clear()
        dealer_cards_images.clear()
        card_stack.clear()
        card_stack_images.clear()

        card_deck = Carddeck()
        card_deck.shuffle()

        update_card_stack()
        dealer_take()
        update_player_cards()

    def player_stay():
        global player_stays
        player_stays = 1
        while get_deck_value(dealer_cards) < 16:
            dealer_take()

    running = True
    while running:
        screen.blit(background, (0, 0))

        player_money_display = font.render(f'{player_money}', False, 'Black')
        screen.blit(player_money_display, (100, 800))
        player_money_display = font.render(f'{bet_value}', False, 'Black')
        screen.blit(player_money_display, (100, 850))

        if bet_and_start != 0:
            player_card_value = get_deck_value(player_cards)
            dealer_card_value = get_deck_value(dealer_cards)

            player_win_display = font.render('YOU Win', False, 'Green')
            player_loose_display = font.render('YOU Loose', False, 'Red')

            for image in card_stack_images:
                screen.blit(image[0], (image[1][0], image[1][1]))

            for image in player_cards_images:
                screen.blit(image[0], (image[1][0], image[1][1]))

            for image in dealer_cards_images:
                screen.blit(image[0], (image[1][0], image[1][1]))

            new_card_button = pygame.Rect(960, 900, 200, 50)
            if game_ended == 0:
                draw_button(new_card_button, "New Card")
            stay_button = pygame.Rect(960, 800, 200, 50)
            if game_ended == 0:
                draw_button(stay_button, "Stay")

            again_button = pygame.Rect(960, 850, 200, 50)
            if game_ended != 0:
                draw_button(again_button, "Accept")

            player_card_value_display = font.render(f'{player_card_value}', False, 'Black')
            screen.blit(player_card_value_display, (100, 900))

            if player_stays == 1:
                if 21 > player_card_value > dealer_card_value or (player_card_value < 21 < dealer_card_value):
                    game_ended = 1
                elif player_card_value <= dealer_card_value:
                    game_ended = -1
            elif player_card_value > 21:
                game_ended = -1
            elif player_card_value == 21:
                game_ended = 1

            if game_ended == 1:
                screen.blit(player_win_display, (960, 540))
                round_over += 1
                if round_over == 1:
                    player_money += (round(random.uniform(1, 10)) * bet_value)
            elif game_ended == -1:
                screen.blit(player_loose_display, (960, 540))
        else:
            calc_tokens()

            bet_button = pygame.Rect(960, 850, 200, 50)
            draw_button(bet_button, "Bet")

            draw_button(all_in_button, "All in")

            for value in tokens:
                screen.blit(value[0], (value[1][0], value[1][1]))

            position_x = 1300
            position_y = 850
            for value in bet_tokens:
                replace_index = bet_tokens.index(value)
                bet_tokens[replace_index] = [value[0], [position_x, position_y], value[2]]

                screen.blit(value[0], (position_x, position_y))
                position_y -= 100
                if position_y < 300:
                    position_y = 850
                    position_x += 100

            clear_bets_button = pygame.Rect(1300, 1000, 200, 50)
            draw_button(clear_bets_button, "Clear")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_ended == 0 and bet_and_start != 0:
                    if new_card_button.collidepoint(event.pos):
                        button_click()
                    if stay_button.collidepoint(event.pos):
                        player_stay()
                elif bet_and_start != 0 and again_button.collidepoint(event.pos):
                    again_click()
                elif bet_and_start == 0:
                    if bet_button.collidepoint(event.pos):
                        if bet_value > 0:
                            start_click()
                    elif all_in_button.collidepoint(event.pos):
                        all_in()
                    elif clear_bets_button.collidepoint(event.pos):
                        bet_tokens.clear()
                    else:
                        for bet_token in bet_tokens:
                            if bet_token[0].get_rect(topleft=(bet_token[1][0], bet_token[1][1])).collidepoint(
                                    event.pos):
                                bet_tokens.remove(bet_token)
                        for token in tokens:
                            if token[0].get_rect(topleft=(token[1][0], token[1][1])).collidepoint(event.pos):
                                if (bet_value + token[2]) <= player_money:
                                    bet_tokens.append(token)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    blackjack_window("Benutzer1", "Password", 999)
