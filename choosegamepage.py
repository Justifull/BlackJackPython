import pygame as pg
import math
from blackjackpage import blackjack_window
from database import load
from layoutessentials import display_text
from depositpage import deposit_window

page_running = True


def choose_game_window(username, password):
    global page_running

    # Code to reinitialize variables when restarting the window
    page_running = True

    # Initialize pygame
    pg.init()

    # Define width and height
    window_width, window_height = 1920, 1080

    # Font
    pg.font.init()
    font = pg.font.SysFont("Arial", 30)

    # Load images
    background = pg.image.load('graphics/choose_game_screen.jpg')

    games_radius = 220
    game_left_center = (397, 670)
    game_left = pg.image.load('graphics/games/game_left.png')
    game_left_default = pg.image.load('graphics/games/game_left.png')
    game_left_hover = pg.image.load('graphics/games/game_left_hover.png')

    game_mid_center = (960, 670)
    game_mid = pg.image.load('graphics/games/game_mid.png')
    game_mid_default = pg.image.load('graphics/games/game_mid.png')
    game_mid_hover = pg.image.load('graphics/games/game_mid_hover.png')

    game_right_center = (1513, 670)
    game_right = pg.image.load('graphics/games/game_right.png')
    game_right_default = pg.image.load('graphics/games/game_right.png')
    game_right_hover = pg.image.load('graphics/games/game_right_hover.png')

    deposit_button = pg.image.load('graphics/buttons/deposit_button.png')
    deposit_button_default = pg.image.load('graphics/buttons/deposit_button.png')
    deposit_button_hover = pg.image.load('graphics/buttons/deposit_button_hover.png')

    # Initialize window
    screen = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption("Casino - Rick and Morty")

    # Set data for window
    clock = pg.time.Clock()

    # Loading Database content and initializing the timer for a database update
    timer_for_database_update = 0
    loaded_data = load()

    def get_distances(mousepos):
        distance_left = math.sqrt(
            (mousepos[0] - game_left_center[0]) ** 2 + (mousepos[1] - game_left_center[1]) ** 2)
        distance_mid = math.sqrt(
            (mousepos[0] - game_mid_center[0]) ** 2 + (mousepos[1] - game_mid_center[1]) ** 2)
        distance_right = math.sqrt(
            (mousepos[0] - game_right_center[0]) ** 2 + (mousepos[1] - game_right_center[1]) ** 2)
        return (distance_left, distance_mid, distance_right)

    while page_running:
        # Setup background
        screen.blit(background, (0, 0))
        screen.blit(game_left, (0, 0))
        screen.blit(game_mid, (0, 0))
        screen.blit(game_right, (0, 0))
        screen.blit(deposit_button, (0, 0))

        # Display the current balance
        display_text(screen, f"{loaded_data[username][1]}$", (1550, 36), (0, 0, 0), 35)

        # Eventmanager
        for event in pg.event.get():
            if event.type == pg.QUIT:
                page_running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                distances = get_distances(event.pos)
                # Event when clicking each game icon
                if distances[0] <= games_radius:
                    blackjack_window(username, password)
                elif distances[1] <= games_radius:
                    print("mid")
                elif distances[2] <= games_radius:
                    print("right")
                elif pg.Rect(1720, 36, 43, 43).collidepoint(event.pos):
                    deposit_window(username, password)

            # Create a game and deposit button hover effect
            elif event.type == pg.MOUSEMOTION:
                distances = get_distances(event.pos)
                if distances[0] <= games_radius:
                    game_left = game_left_hover
                    game_mid = game_mid_default
                    game_right = game_right_default
                    deposit_button = deposit_button_default
                elif distances[1] <= games_radius:
                    game_mid = game_mid_hover
                    game_left = game_left_default
                    game_right = game_right_default
                    deposit_button = deposit_button_default
                elif distances[2] <= games_radius:
                    game_right = game_right_hover
                    game_left = game_left_default
                    game_mid = game_mid_default
                    deposit_button = deposit_button_default
                elif pg.Rect(1720, 36, 43, 43).collidepoint(event.pos):
                    deposit_button = deposit_button_hover
                    game_left = game_left_default
                    game_mid = game_mid_default
                    game_right = game_right_default
                else:
                    game_left = game_left_default
                    game_mid = game_mid_default
                    game_right = game_right_default
                    deposit_button = deposit_button_default

        # Refresh the given database every 60 ticks
        timer_for_database_update += 1
        if timer_for_database_update % 60 == 0:
            loaded_data = load()

        # Refresh the screen
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    choose_game_window("test", "test")
