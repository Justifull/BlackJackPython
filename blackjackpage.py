import pygame as pg
from carddeck import get_deck_value
from database import save
from database import load
from blackjackgame import BlackJackGame
from blackjackplayer import BlackJackPlayer
from layoutessentials import display_text
from depositpage import deposit_window

game = BlackJackGame()
player = BlackJackPlayer()
dealer = BlackJackPlayer()
player_money = 0
increasing_value = 0
bet_amount = 0

page_running = True


def blackjack_window(username, password):
    global game
    global player
    global dealer
    global page_running
    global player_money
    global increasing_value
    global bet_amount

    # Code to reinitialize variables when restarting the window
    game = BlackJackGame()
    player = BlackJackPlayer()
    dealer = BlackJackPlayer()
    player_money = 0
    increasing_value = 0
    bet_amount = 0

    page_running = True

    dealer.add_card(game.take_card())
    dealer.update_cards(True, True)

    # Initialize pygame
    pg.init()

    # Define width and height
    window_width, window_height = 1920, 1080

    # Font
    pg.font.init()

    # Path for custom font for winning screen
    font_path = "graphics/fonts/get_schwifty.ttf"

    # Load images
    background = pg.image.load('graphics/games/blackjack/blackjack_screen.jpg')
    background_bet = pg.image.load('graphics/games/blackjack/blackjack_bet_screen.jpg')

    win_overlay = pg.image.load('graphics/games/blackjack/win_overlay.png')
    loose_overlay = pg.image.load('graphics/games/blackjack/loose_overlay.png')

    all_in_button = pg.image.load('graphics/buttons/all_in_button.png')
    all_in_button_default = pg.image.load('graphics/buttons/all_in_button.png')
    all_in_button_hover = pg.image.load('graphics/buttons/all_in_button_hover.png')

    clear_button = pg.image.load('graphics/buttons/clear_button.png')
    clear_button_default = pg.image.load('graphics/buttons/clear_button.png')
    clear_button_hover = pg.image.load('graphics/buttons/clear_button_hover.png')

    bet_button = pg.image.load('graphics/buttons/bet_button.png')
    bet_button_default = pg.image.load('graphics/buttons/bet_button.png')
    bet_button_hover = pg.image.load('graphics/buttons/bet_button_hover.png')

    take_button = pg.image.load('graphics/buttons/take_button.png')
    take_button_default = pg.image.load('graphics/buttons/take_button.png')
    take_button_hover = pg.image.load('graphics/buttons/take_button_hover.png')

    stay_button = pg.image.load('graphics/buttons/stay_button.png')
    stay_button_default = pg.image.load('graphics/buttons/stay_button.png')
    stay_button_hover = pg.image.load('graphics/buttons/stay_button_hover.png')

    next_button = pg.image.load('graphics/buttons/next_button.png')
    next_button_default = pg.image.load('graphics/buttons/next_button.png')
    next_button_hover = pg.image.load('graphics/buttons/next_button_hover.png')

    deposit_button = pg.image.load('graphics/buttons/deposit_button.png')
    deposit_button_default = pg.image.load('graphics/buttons/deposit_button.png')
    deposit_button_hover = pg.image.load('graphics/buttons/deposit_button_hover.png')

    # Initialize window
    screen = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption("BlackJack - Rick and Morty")

    # Set data for window
    clock = pg.time.Clock()

    # Loading Database content and initializing the timer for a database update
    timer_for_database_update = 0
    loaded_data = load()

    # Load the users money
    player_money = loaded_data[username][1]

    # Initialize value to only give money to player once
    round_over = 0

    # Initialize value that increases until it reached win value
    increasing_value = 0

    # Used when clicking the bet button to deposit a bet and remove the amount from the players balance
    def bet_click():
        global player_money
        global bet_amount
        game.make_ready()
        player_money -= game.get_bet_token_value()
        bet_amount = game.get_bet_token_value()
        game.clear_bets()
        save(username, password, player_money)

    # Used when clicking the new card button to add a card to the players deck, remove one from the main card deck
    # and update the players card inventory
    def new_card_click():
        player.add_card(game.take_card())
        player.update_cards(False, False)

    # Used when clicking the stay button to let the system know that the player does not want any new cards
    def player_stay_click():
        player.stay()
        while get_deck_value(dealer.get_cards()) < 16:
            dealer.add_card(game.take_card())
        dealer.update_cards(False, True)

    # Used when clicking the next game button to start a new blackjack round
    def next_click():
        global player
        global dealer
        global game
        global increasing_value
        player = BlackJackPlayer()
        dealer = BlackJackPlayer()
        game = BlackJackGame()
        increasing_value = 0

        dealer.add_card(game.take_card())
        player.update_cards(False, False)
        dealer.update_cards(True, True)

    # Used to get the token out of the token list just by its value
    def get_token_by_value(request_value):
        for token_value in game.get_tokens():
            if token_value[2] == request_value:
                return token_value

    # Used when clicking the all-in button to add enough tokens to the players bet inventory until they are worth
    # as much as its balance or the amount of tokens is more than 105 (because of design)
    def all_in():
        if player_money > game.get_bet_token_value():
            temp_value = game.get_bet_token_value()
            while (temp_value + 10000) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(10000))
                temp_value += 10000
            while (temp_value + 5000) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(5000))
                temp_value += 5000
            while (temp_value + 1000) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(1000))
                temp_value += 1000
            while (temp_value + 500) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(500))
                temp_value += 500
            while (temp_value + 100) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(100))
                temp_value += 100
            while (temp_value + 25) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(25))
                temp_value += 25
            while (temp_value + 5) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(5))
                temp_value += 5
            while (temp_value + 1) <= player_money and len(game.get_bet_tokens()) < 105:
                game.add_bet_token(get_token_by_value(1))
                temp_value += 1

    # Main function for running the opened window
    while page_running:
        # Setup background for playing area
        screen.blit(background, (0, 0))

        if game.is_ready():
            player_card_value = get_deck_value(player.get_cards())
            dealer_card_value = get_deck_value(dealer.get_cards())

            for image in game.get_unused_card_stack():
                screen.blit(image[1][0], (image[1][1][0], image[1][1][1]))

            for image in player.get_card_images():
                screen.blit(image[0], (image[1][0], image[1][1]))

            for image in dealer.get_card_images():
                screen.blit(image[0], (image[1][0], image[1][1]))

            if not game.is_over():
                screen.blit(take_button, (0, 0))
                if not player.is_staying():
                    screen.blit(stay_button, (0, 0))
            else:
                if game.is_won() == 1:
                    screen.blit(win_overlay, (0, 0))

                    increasing_value_color = (0, 0, 255)
                    if increasing_value >= 1000000:
                        increasing_value_color = (0, 255, 0)
                    elif increasing_value >= 100000:
                        increasing_value_color = (0, 255, 64)
                    elif increasing_value >= 10000:
                        increasing_value_color = (0, 255, 128)
                    elif increasing_value >= 1000:
                        increasing_value_color = (0, 192, 255)
                    elif increasing_value >= 100:
                        increasing_value_color = (0, 128, 255)
                    elif increasing_value >= 10:
                        increasing_value_color = (0, 64, 255)

                    font = pg.font.Font(font_path, 140)
                    text_render = font.render(str(increasing_value), True, increasing_value_color)
                    text_rect = text_render.get_rect()
                    text_rect.center = (970, 600)
                    text_rect.topleft = (970 - text_rect.width // 2, 600 - text_rect.height // 2)
                    screen.blit(text_render, text_rect.topleft)

                    if (increasing_value + 10000) < ((bet_amount * 2) - 20000):
                        increasing_value += 10000
                    elif (increasing_value + 1000) < ((bet_amount * 2) - 5000):
                        increasing_value += 1000
                    elif (increasing_value + 100) <= ((bet_amount * 2) - 100):
                        increasing_value += 100
                    elif increasing_value < (bet_amount * 2):
                        increasing_value += 1

                    round_over += 1
                    if round_over == 1:
                        player_money += 2 * bet_amount
                        save(username, password, player_money)
                elif game.is_won() == -1:
                    screen.blit(loose_overlay, (0, 0))
                screen.blit(next_button, (0, 0))

            if player.is_staying() and game.is_won() == 0:
                if 21 > player_card_value > dealer_card_value or (player_card_value < 21 < dealer_card_value):
                    game.end_game()
                    game.won(1)
                elif player_card_value <= dealer_card_value:
                    game.end_game()
                    game.won(-1)
            elif player_card_value > 21 and game.is_won() == 0:
                game.end_game()
                game.won(-1)
            elif player_card_value == 21 and game.is_won() == 0:
                game.end_game()
                game.won(1)

        else:
            # Setup background for betting area
            screen.blit(background_bet, (0, 0))

            # Display current bet tokens value
            display_text(screen, f"{game.get_bet_token_value()}$", (320, 192), (0, 0, 0), 35)

            screen.blit(bet_button, (0, 0))
            screen.blit(all_in_button, (0, 0))

            for value in game.get_tokens():
                screen.blit(value[0], (value[1][0], value[1][1]))

            bet_tokens = game.get_bet_tokens()
            position_x = 370
            position_y = 850
            for value in bet_tokens:
                replace_index = bet_tokens.index(value)
                bet_tokens[replace_index] = [value[0], [position_x, position_y], value[2]]

                screen.blit(value[0], (position_x, position_y))
                position_y -= 90
                if position_y < 300:
                    position_y = 850
                    position_x += 90

            if len(bet_tokens) > 0:
                screen.blit(clear_button, (0, 0))

        screen.blit(deposit_button, (0, 0))

        # Display the current balance
        display_text(screen, f"{loaded_data[username][1]}$", (1550, 36), (0, 0, 0), 35)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                save(username, password, player_money)
                page_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not game.is_over() and game.is_ready():
                    if pg.Rect(1515, 890, 190, 45).collidepoint(event.pos):
                        new_card_click()
                    if pg.Rect(1515, 820, 190, 45).collidepoint(event.pos):
                        player_stay_click()

                elif pg.Rect(810, 685, 305, 75).collidepoint(event.pos) and game.is_over():
                    next_click()

                elif not game.is_ready():
                    if pg.Rect(890, 960, 140, 90).collidepoint(event.pos):
                        if game.get_bet_token_value() > 0:
                            bet_click()
                    elif pg.Rect(160, 115, 85, 45).collidepoint(event.pos):
                        all_in()
                    elif pg.Rect(310, 115, 85, 45).collidepoint(event.pos):
                        game.clear_bets()
                    elif pg.Rect(1720, 36, 43, 43).collidepoint(event.pos):
                        deposit_window(username, password)
                    else:
                        for bet_token in game.get_bet_tokens():
                            if bet_token[0].get_rect(topleft=(bet_token[1][0], bet_token[1][1])).collidepoint(
                                    event.pos):
                                game.remove_bet_token(bet_token)
                        for token in game.get_tokens():
                            if token[0].get_rect(topleft=(token[1][0], token[1][1])).collidepoint(event.pos):
                                if (game.get_bet_token_value() + token[2]) <= player_money and len(game.get_bet_tokens()) < 105:
                                    game.add_bet_token(token)

            elif event.type == pg.MOUSEMOTION:
                if pg.Rect(890, 960, 140, 90).collidepoint(event.pos):
                    bet_button = bet_button_hover
                elif pg.Rect(310, 115, 85, 45).collidepoint(event.pos):
                    clear_button = clear_button_hover
                    all_in_button = all_in_button_default
                elif pg.Rect(160, 115, 85, 45).collidepoint(event.pos):
                    all_in_button = all_in_button_hover
                    clear_button = clear_button_default
                elif pg.Rect(1515, 890, 190, 45).collidepoint(event.pos):
                    take_button = take_button_hover
                    stay_button = stay_button_default
                elif pg.Rect(1515, 820, 190, 45).collidepoint(event.pos):
                    stay_button = stay_button_hover
                    take_button = take_button_default
                elif pg.Rect(1720, 36, 43, 43).collidepoint(event.pos):
                    deposit_button = deposit_button_hover
                elif pg.Rect(810, 685, 305, 75).collidepoint(event.pos) and game.is_over():
                    next_button = next_button_hover
                else:
                    bet_button = bet_button_default
                    clear_button = clear_button_default
                    all_in_button = all_in_button_default
                    take_button = take_button_default
                    stay_button = stay_button_default
                    deposit_button = deposit_button_default
                    next_button = next_button_default

        # Refresh the given database every 60 ticks
        timer_for_database_update += 1
        if timer_for_database_update % 60 == 0:
            loaded_data = load()
            player_money = loaded_data[username][1]

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    blackjack_window("test", "test")
