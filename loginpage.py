import pygame as pg
import sys
from choosegamepage import choose_game_window
from registerpage import register_window
from database import load
from layoutessentials import display_text
from layoutessentials import display_transparent_rect

username_field_text = ""
password_field_text = ""
login_status = ""
login_status_position = (850, 1000)
login_status_color = (255, 0, 0)

page_running = True


def login_window():
    global username_field_text
    global password_field_text
    global login_status
    global login_status_position
    global login_status_color
    global page_running

    # Code to reinitialize variables when restarting the window
    username_field_text = ""
    password_field_text = ""
    login_status = ""
    login_status_position = (850, 1000)
    login_status_color = (255, 0, 0)

    page_running = True

    # Initialize pygame
    pg.init()

    # Define width and height
    window_width, window_height = 1920, 1080

    # Font
    pg.font.init()
    font = pg.font.SysFont("Arial", 30)

    # Load images
    background = pg.image.load('graphics/login_screen.jpg')

    leaderboard = pg.image.load('graphics/leaderboard_overlay.png')

    login_button = pg.image.load('graphics/buttons/login_button.png')
    login_button_default = pg.image.load('graphics/buttons/login_button.png')
    login_button_hover = pg.image.load('graphics/buttons/login_button_hover.png')

    register_text = pg.image.load('graphics/buttons/register_text.png')
    register_text_default = pg.image.load('graphics/buttons/register_text.png')
    register_text_hover = pg.image.load('graphics/buttons/register_text_hover.png')

    # Initialize window
    screen = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption("Casino - Rick and Morty")

    # Set data for window
    clock = pg.time.Clock()
    focussed_field = 0

    # Loading Database content and initializing the timer for a database update
    timer_for_database_update = 0
    loaded_data = load()

    # Setting up a textfield indicator
    cursor_position_username = 0
    cursor_position_password = 0
    cursor_width = 2

    # Function to validate the user inputs and leading to the next page
    def validate_userinput():
        global username_field_text
        global password_field_text
        global login_status
        global login_status_position
        global login_status_color
        global page_running

        # Test if username and password field are not empty
        if username_field_text and password_field_text:
            # Test if username input is in the database and if so the entered password is the same as the dictionary value
            if username_field_text in loaded_data and password_field_text == \
                    loaded_data[username_field_text][0]:
                # Setting the correct login status and redirecting to the game page
                login_status = "Logging in.."
                login_status_position = [850, 1000]
                login_status_color = (0, 255, 0)
                choose_game_window(username_field_text, loaded_data[username_field_text][0])
            else:
                # Setting the correct login status
                login_status = "Password or username is wrong"
                login_status_position = [770, 1000]
                login_status_color = (255, 0, 0)
        else:
            # Setting the correct login status
            login_status = "Please enter a username and password"
            login_status_position = [730, 1000]
            login_status_color = (255, 0, 0)

    # Function when pressing the register button
    def register_click():
        register_window()

    # Function when pressing the login button
    def login_click():
        validate_userinput()

    # Validate the leaderboard entries
    def validate_leaderboard():
        sorted_dict = dict(sorted(loaded_data.items(), key=lambda item: item[1][1], reverse=True))
        sorted_list = list(sorted_dict.keys())
        first_place = "..."
        second_place = "..."
        third_place = "..."
        if len(sorted_list) >= 1:
            first_place = sorted_list[0]
        if len(sorted_list) >= 2:
            second_place = sorted_list[1]
        if len(sorted_list) >= 3:
            third_place = sorted_list[2]
        return first_place, second_place, third_place

    # Main function for running the opened window
    while page_running:
        # Setup background
        screen.blit(background, (0, 0))
        screen.blit(leaderboard, (0, 0))
        screen.blit(login_button, (0, 0))
        screen.blit(register_text, (0, 0))

        # Display leaderboard entries
        first, second, third = validate_leaderboard()
        display_text(screen, first, (100, 152), (22, 172, 201), 40)
        display_text(screen, second, (100, 210), (22, 172, 201), 40)
        display_text(screen, third, (100, 270), (22, 172, 201), 40)

        # Eventmanager
        for event in pg.event.get():
            if event.type == pg.QUIT:
                page_running = False
            elif event.type == pg.KEYDOWN:
                # Navigate the indicator through the input text (left direction)
                if event.key == pg.K_LEFT and focussed_field == 1:
                    cursor_position_username = max(0, cursor_position_username - 1)
                elif event.key == pg.K_LEFT and focussed_field == -1:
                    cursor_position_password = max(0, cursor_position_password - 1)

                # Navigate the indicator through the input text (right direction)
                if event.key == pg.K_RIGHT and focussed_field == 1:
                    cursor_position_username = min(len(username_field_text), cursor_position_username + 1)
                elif event.key == pg.K_RIGHT and focussed_field == -1:
                    cursor_position_password = min(len(password_field_text), cursor_position_password + 1)

                # Validate the data by pressing enter button
                if event.key == pg.K_RETURN:
                    validate_userinput()

                # Switch the selected Text field
                if event.key == pg.K_TAB:
                    if focussed_field == 1:
                        focussed_field = -1
                    elif focussed_field == -1:
                        focussed_field = 1

                # Delete character of username or password and update indicator position
                elif event.key == pg.K_BACKSPACE:
                    if len(username_field_text) > 0 and focussed_field == 1:
                        username_field_text = username_field_text[:max(0, cursor_position_username - 1)] + username_field_text[cursor_position_username:]
                        cursor_position_username = max(0, cursor_position_username - 1)
                    elif len(password_field_text) > 0 and focussed_field == -1:
                        password_field_text = password_field_text[:max(0, cursor_position_password - 1)] + password_field_text[cursor_position_password:]
                        cursor_position_password = max(0, cursor_position_password - 1)

                # Add a new character to username or password and update indicator position
                else:
                    char = event.unicode
                    if len(username_field_text) < 30 and focussed_field == 1:
                        username_field_text = username_field_text[:cursor_position_username] + char + username_field_text[cursor_position_username:]
                        cursor_position_username += len(char)
                    elif len(password_field_text) < 30 and focussed_field == -1:
                        password_field_text = password_field_text[:cursor_position_password] + char + password_field_text[cursor_position_password:]
                        cursor_position_password += len(char)

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Focus a textfield to enter text / focus no field
                if pg.Rect(720, 750, 475, 40).collidepoint(event.pos):
                    focussed_field = 1
                    login_status = ""
                elif pg.Rect(720, 840, 475, 40).collidepoint(event.pos):
                    focussed_field = -1
                    login_status = ""
                else:
                    focussed_field = 0

                # Event when clicking the register text or login button
                if pg.Rect(1080, 890, 105, 30).collidepoint(event.pos):
                    register_click()
                if pg.Rect(850, 950, 190, 50).collidepoint(event.pos):
                    login_click()

            # Create a button hover effect
            elif event.type == pg.MOUSEMOTION:
                if pg.Rect(850, 950, 190, 50).collidepoint(event.pos):
                    login_button = login_button_hover
                elif pg.Rect(1080, 890, 105, 30).collidepoint(event.pos):
                    register_text = register_text_hover
                else:
                    login_button = login_button_default
                    register_text = register_text_default

        # Display transparent rectangles behind user inputs
        display_transparent_rect(screen, (710, 750), (475, 40), (129, 229, 248, 128))
        display_transparent_rect(screen, (710, 840), (475, 40), (129, 229, 248, 128))

        # Display the username and password field text
        display_text(screen, username_field_text, (720, 750), (0, 0, 0))
        display_text(screen, password_field_text, (720, 840), (0, 0, 0))

        # Display the text input position indicator
        if focussed_field == 1:
            prefix_text = username_field_text[:cursor_position_username]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 750, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)
        elif focussed_field == -1:
            prefix_text = password_field_text[:cursor_position_password]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 840, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)

        # Display the login status
        display_text(screen, login_status, login_status_position, login_status_color)

        # Refresh the given database every 60 ticks
        timer_for_database_update += 1
        if timer_for_database_update % 60 == 0:
            loaded_data = load()

        # Refresh the screen
        pg.display.update()
        clock.tick(60)

    # Quit the application
    pg.quit()
    sys.exit()


# Start the main page
if __name__ == "__main__":
    login_window()
