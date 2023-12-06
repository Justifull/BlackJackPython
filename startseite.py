import pygame
# import pygame as pg
import sys
import json
from choosegame import choose_game_window
from register import register

loaded_data = None


def startseite():
    # Initialisiere Pygame
    pygame.init()

    # Fenstergröße
    fenster_breite, fenster_hoehe = 800, 600

    # Farben
    weiß = (255, 255, 255)
    schwarz = (100, 0, 0)

    accounts_data = "accounts.json"

    # Schriftart
    pygame.font.init()
    schriftart = pygame.font.SysFont("Arial", 30)

    # Pygame-Fenster einrichten
    bildschirm = pygame.display.set_mode((fenster_breite, fenster_hoehe))
    pygame.display.set_caption("Login-Seite")

    # Funktion zum Anzeigen von Text
    def text_anzeigen(text, x, y):
        text_render = schriftart.render(text, True, schwarz)
        bildschirm.blit(text_render, (x, y))

    def draw_button(rect, text):
        pygame.draw.rect(bildschirm, (255, 200, 255), rect)

        button_font = pygame.font.Font(None, 36)
        text_surface = button_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)

        bildschirm.blit(text_surface, text_rect)

    def register_click():
        register()

    def load():
        global loaded_data
        with open(accounts_data, 'r') as json_datei:
            loaded_data = json.load(json_datei)

    load()

    laufend = True
    clock = pygame.time.Clock()

    benutzername_eingabe = ""
    passwort_eingabe = ""
    login_status = ""

    located_field = 0

    timer_for_database_update = 0

    while laufend:
        global loaded_data
        # Zeichne Hintergrund
        bildschirm.fill(weiß)

        register_button = pygame.Rect(300, 450, 200, 50)
        draw_button(register_button, "Register")
        login_button = pygame.Rect(300, 500, 200, 50)
        draw_button(login_button, "Login")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufend = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Überprüfe Anmeldeinformationen
                    if benutzername_eingabe and passwort_eingabe:
                        if benutzername_eingabe in loaded_data and passwort_eingabe == \
                                loaded_data[benutzername_eingabe][0]:
                            login_status = "Korrekt"
                            laufend = False
                            choose_game_window(benutzername_eingabe, loaded_data[benutzername_eingabe][0],
                                             loaded_data[benutzername_eingabe][1])
                        else:
                            login_status = "Nicht korrekt"
                    else:
                        login_status = "Bitte Benutzername und Passwort eingeben."
                if event.key == pygame.K_TAB:
                    if located_field == 1:
                        located_field = -1
                    else:
                        located_field = 1

                elif event.key == pygame.K_BACKSPACE:
                    # Lösche letzten Buchstaben
                    if len(benutzername_eingabe) > 0 and located_field == 1:
                        benutzername_eingabe = benutzername_eingabe[:-1]
                    elif len(passwort_eingabe) > 0 and located_field == -1:
                        passwort_eingabe = passwort_eingabe[:-1]
                else:
                    # Füge Buchstaben zum Benutzernamen oder Passwort hinzu
                    if len(benutzername_eingabe) < 10 and located_field == 1:
                        benutzername_eingabe += event.unicode
                    elif len(passwort_eingabe) < 10 and located_field == -1:
                        passwort_eingabe += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(300, 200, 200, 40).collidepoint(event.pos):
                    located_field = 1
                elif pygame.Rect(300, 300, 200, 40).collidepoint(event.pos):
                    located_field = -1
                else:
                    located_field = 0
                if register_button.collidepoint(event.pos):
                    register_click()
                if login_button.collidepoint(event.pos):
                    if benutzername_eingabe and passwort_eingabe:
                        if benutzername_eingabe in loaded_data and passwort_eingabe == \
                                loaded_data[benutzername_eingabe][0]:
                            login_status = "Korrekt"
                            choose_game_window(benutzername_eingabe, loaded_data[benutzername_eingabe][0],
                                             loaded_data[benutzername_eingabe][1])
                        else:
                            login_status = "Nicht korrekt"
                    else:
                        login_status = "Bitte Benutzername und Passwort eingeben."

        # Zeichne Benutzernamen und Passwort Eingabefelder
        pygame.draw.rect(bildschirm, (200, 100, 100), (300, 200, 200, 40))
        pygame.draw.rect(bildschirm, (200, 100, 100), (300, 300, 200, 40))

        # Zeichne eingegebenen Benutzernamen und Passwort
        text_anzeigen("Benutzername:", 100, 200)
        text_anzeigen(benutzername_eingabe, 310, 205)

        text_anzeigen("Passwort:", 100, 300)
        # text_anzeigen("*" * len(passwort_eingabe), 310, 305)
        text_anzeigen(passwort_eingabe, 310, 305)

        # Zeichne Login-Status
        text_anzeigen(login_status, 100, 400)

        timer_for_database_update += 1

        if timer_for_database_update % 120 == 0:
            load()

        # Aktualisiere den Bildschirm
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    startseite()
