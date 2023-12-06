import pygame
import sys
from main import blackjack_window
import json


loaded_data = None


def choose_game_window(username, password, money):
    account_name = username
    account_password = password
    player_money = money

    # Initialisiere Pygame
    pygame.init()

    # Farben
    weiß = (255, 255, 255)
    schwarz = (100, 0, 0)

    accounts_data = "accounts.json"

    # Schriftart
    pygame.font.init()
    schriftart = pygame.font.SysFont("Arial", 30)

    # Pygame-Fenster einrichten
    bildschirm = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Login-Seite")

    game_left = pygame.image.load('graphics/games/game_left.png')
    game_mid = pygame.image.load('graphics/games/game_mid.png')
    game_right = pygame.image.load('graphics/games/game_right.png')

    def text_anzeigen(text, x, y):
        text_render = schriftart.render(text, True, schwarz)
        bildschirm.blit(text_render, (x, y))

    def load():
        global loaded_data
        with open(accounts_data, 'r') as json_datei:
            loaded_data = json.load(json_datei)

    load()

    laufend = True
    clock = pygame.time.Clock()

    timer_for_database_update = 0

    while laufend:
        global loaded_data
        # Zeichne Hintergrund
        bildschirm.fill(weiß)
        bildschirm.blit(game_left, (0, 0))
        bildschirm.blit(game_mid, (0, 0))
        bildschirm.blit(game_right, (0, 0))

        pygame.draw.rect(bildschirm, (200, 100, 100), (100, 100, 200, 40))
        text_anzeigen(f"Geld: {money}", 100, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufend = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(0, 0, 640, 1080).collidepoint(event.pos):
                    blackjack_window(account_name, account_password, loaded_data[account_name][1])
                elif pygame.Rect(640, 0, 640, 1080).collidepoint(event.pos):
                    print("Pferde Rennen")
                elif pygame.Rect(1280, 0, 640, 1080).collidepoint(event.pos):
                    print("Slots")

        # Aktualisiere den Bildschirm
        pygame.display.update()
        clock.tick(60)

        timer_for_database_update += 1

        if timer_for_database_update % 120 == 0:
            load()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    choose_game_window("Benutzer1", "Password", 999)
