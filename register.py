import pygame
import sys
import json

loaded_data = None


def register():
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

    def register_user(new_username, new_userpassword, new_usermoney):
        global loaded_data

        data = {}
        for account in loaded_data.keys():
            data.update({account: loaded_data[account]})

        data.update({new_username: [new_userpassword, int(new_usermoney)]})

        with open(accounts_data, 'w') as json_datei:
            json.dump(data, json_datei)

    laufend = True
    clock = pygame.time.Clock()

    benutzername_eingabe = ""
    passwort_eingabe = ""
    geld_eingabe = ""
    login_status = ""

    located_field = 0

    def load():
        global loaded_data
        with open(accounts_data, 'r') as json_datei:
            loaded_data = json.load(json_datei)

    load()

    while laufend:
        global loaded_data
        # Zeichne Hintergrund
        bildschirm.fill(weiß)

        register_button = pygame.Rect(300, 450, 200, 50)
        draw_button(register_button, "Register")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufend = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Überprüfe Anmeldeinformationen
                    if benutzername_eingabe and passwort_eingabe and geld_eingabe and (
                            len(benutzername_eingabe) > 3) and (len(passwort_eingabe) > 3):
                        if benutzername_eingabe in loaded_data:
                            login_status = "Benutzername schon vergeben"
                        else:
                            login_status = "Korrekt"
                            laufend = False
                            register_user(benutzername_eingabe, passwort_eingabe, geld_eingabe)
                    else:
                        login_status = "Bitte Benutzername, Passwort und Geld eingeben."
                if event.key == pygame.K_TAB:
                    if located_field == 1:
                        located_field = 2
                    elif located_field == 2:
                        located_field = 3
                    else:
                        located_field = 1
                elif event.key == pygame.K_BACKSPACE:
                    # Lösche letzten Buchstaben
                    if len(benutzername_eingabe) > 0 and located_field == 1:
                        benutzername_eingabe = benutzername_eingabe[:-1]
                    elif len(passwort_eingabe) > 0 and located_field == 2:
                        passwort_eingabe = passwort_eingabe[:-1]
                    elif len(geld_eingabe) > 0 and located_field == 3:
                        geld_eingabe = geld_eingabe[:-1]
                else:
                    # Füge Buchstaben zum Benutzernamen oder Passwort hinzu
                    if len(benutzername_eingabe) < 10 and located_field == 1:
                        benutzername_eingabe += event.unicode
                    elif len(passwort_eingabe) < 10 and located_field == 2:
                        passwort_eingabe += event.unicode
                    elif len(geld_eingabe) < 10 and located_field == 3 and pygame.K_0 <= event.key <= pygame.K_9:
                        geld_eingabe += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(300, 100, 200, 40).collidepoint(event.pos):
                    located_field = 1
                elif pygame.Rect(300, 200, 200, 40).collidepoint(event.pos):
                    located_field = 2
                elif pygame.Rect(300, 300, 200, 40).collidepoint(event.pos):
                    located_field = 3
                else:
                    located_field = 0
                if register_button.collidepoint(event.pos):
                    if benutzername_eingabe and passwort_eingabe and geld_eingabe and (
                            len(benutzername_eingabe) > 3) and (len(passwort_eingabe) > 3):
                        if benutzername_eingabe in loaded_data:
                            login_status = "Benutzername schon vergeben"
                        else:
                            login_status = "Korrekt"
                            laufend = False
                            register_user(benutzername_eingabe, passwort_eingabe, geld_eingabe)
                    else:
                        login_status = "Bitte Benutzername, Passwort und Geld eingeben."

        # Zeichne Benutzernamen und Passwort Eingabefelder
        pygame.draw.rect(bildschirm, (200, 100, 100), (300, 100, 200, 40))
        pygame.draw.rect(bildschirm, (200, 100, 100), (300, 200, 200, 40))
        pygame.draw.rect(bildschirm, (200, 100, 100), (300, 300, 200, 40))

        # Zeichne eingegebenen Benutzernamen und Passwort
        text_anzeigen("Benutzername:", 100, 100)
        text_anzeigen(benutzername_eingabe, 310, 105)

        text_anzeigen("Passwort:", 100, 200)
        text_anzeigen(passwort_eingabe, 310, 205)

        text_anzeigen("Geld:", 100, 300)
        text_anzeigen(geld_eingabe, 310, 305)

        # Zeichne Login-Status
        text_anzeigen(login_status, 100, 400)

        # Aktualisiere den Bildschirm
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    register()
