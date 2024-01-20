import pygame as pg
from database import load
from database import save
from layoutessentials import display_text
from layoutessentials import display_transparent_rect

username_field_text = ""
password_field_text = ""
balance_field_text = ""
register_status = ""
register_status_position = (850, 1000)
register_status_color = (255, 0, 0)
register_status_size = 25

page_running = True


def register_window():
    global username_field_text
    global password_field_text
    global balance_field_text
    global register_status
    global register_status_position
    global register_status_color
    global register_status_size
    global page_running

    # Code to reinitialize variables when restarting the window
    username_field_text = ""
    password_field_text = ""
    balance_field_text = ""
    register_status = ""
    register_status_position = (850, 1000)
    register_status_color = (255, 0, 0)
    register_status_size = 25

    page_running = True

    # Initialize pygame
    pg.init()

    # Define width and height
    window_width, window_height = 1920, 1080

    # Font
    pg.font.init()
    font = pg.font.SysFont("Arial", 30)

    # Load images
    background = pg.image.load('graphics/register_screen.jpg')

    register_button = pg.image.load('graphics/buttons/register_button.png')
    register_button_default = pg.image.load('graphics/buttons/register_button.png')
    register_button_hover = pg.image.load('graphics/buttons/register_button_hover.png')

    exit_button = pg.image.load('graphics/buttons/quit_button.png')

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
    cursor_position_balance = 0
    cursor_width = 2

    # Function to validate the user inputs and leading to the next page
    def validate_userinput():
        global username_field_text
        global password_field_text
        global balance_field_text
        global register_status
        global register_status_position
        global register_status_color
        global register_status_size
        global page_running

        # Test if username and password field are not empty
        if username_field_text and password_field_text and balance_field_text:
            # Test if username input is in the database and if so the entered password is the same as the dictionary value
            if username_field_text in loaded_data:
                # Setting the correct login status for already used username
                register_status = "Username is already taken"
                register_status_position = [810, 970]
                register_status_color = (255, 0, 0)
                register_status_size = 28
            elif len(username_field_text) > 3 and len(password_field_text) > 3:
                # Setting the correct login status and redirecting to the game page
                register_status = "Account has been registered"
                register_status_position = [800, 970]
                register_status_color = (0, 255, 0)
                register_status_size = 28
                # Saving the userdata in the database
                save(username_field_text, password_field_text, int(balance_field_text))
                page_running = False
            else:
                # Setting the correct login status
                register_status = "Username and password length must be more than 3"
                register_status_position = [710, 975]
                register_status_color = (255, 0, 0)
                register_status_size = 25
        else:
            # Setting the correct login status
            register_status = "Please enter a username, password and balance"
            register_status_position = [700, 970]
            register_status_color = (255, 0, 0)
            register_status_size = 28

    # Function when pressing the register button
    def register_click():
        validate_userinput()

    # Main function for running the opened window
    while page_running:
        # Setup background
        screen.blit(background, (0, 0))
        screen.blit(register_button, (0, 0))
        screen.blit(exit_button, (1850, 20))

        # Eventmanager
        for event in pg.event.get():
            if event.type == pg.QUIT:
                page_running = False
            elif event.type == pg.KEYDOWN:
                # Navigate the indicator through the input text (left direction)
                if event.key == pg.K_LEFT and focussed_field == 1:
                    cursor_position_username = max(0, cursor_position_username - 1)
                elif event.key == pg.K_LEFT and focussed_field == 2:
                    cursor_position_password = max(0, cursor_position_password - 1)
                elif event.key == pg.K_LEFT and focussed_field == 3:
                    cursor_position_balance = max(0, cursor_position_balance - 1)

                # Navigate the indicator through the input text (right direction)
                if event.key == pg.K_RIGHT and focussed_field == 1:
                    cursor_position_username = min(len(username_field_text), cursor_position_username + 1)
                elif event.key == pg.K_RIGHT and focussed_field == 2:
                    cursor_position_password = min(len(password_field_text), cursor_position_password + 1)
                elif event.key == pg.K_RIGHT and focussed_field == 3:
                    cursor_position_balance = min(len(balance_field_text), cursor_position_balance + 1)

                # Validate the data by pressing enter button
                if event.key == pg.K_RETURN:
                    validate_userinput()

                # Switch the selected Text field
                if event.key == pg.K_TAB:
                    if focussed_field == 1:
                        focussed_field = 2
                    elif focussed_field == 2:
                        focussed_field = 3
                    elif focussed_field == 3:
                        focussed_field = 1

                # Delete character of username or password and update indicator position
                elif event.key == pg.K_BACKSPACE:
                    if len(username_field_text) > 0 and focussed_field == 1:
                        username_field_text = username_field_text[
                                              :max(0, cursor_position_username - 1)] + username_field_text[
                                                                                       cursor_position_username:]
                        cursor_position_username = max(0, cursor_position_username - 1)
                    elif len(password_field_text) > 0 and focussed_field == 2:
                        password_field_text = password_field_text[
                                              :max(0, cursor_position_password - 1)] + password_field_text[
                                                                                       cursor_position_password:]
                        cursor_position_password = max(0, cursor_position_password - 1)
                    elif len(balance_field_text) > 0 and focussed_field == 3:
                        balance_field_text = balance_field_text[
                                             :max(0, cursor_position_balance - 1)] + balance_field_text[
                                                                                     cursor_position_balance:]
                        cursor_position_balance = max(0, cursor_position_balance - 1)

                # Add a new character to username or password and update indicator position
                else:
                    char = event.unicode
                    if len(username_field_text) < 30 and focussed_field == 1:
                        username_field_text = username_field_text[
                                              :cursor_position_username] + char + username_field_text[
                                                                                  cursor_position_username:]
                        cursor_position_username += len(char)
                    elif len(password_field_text) < 30 and focussed_field == 2:
                        password_field_text = password_field_text[
                                              :cursor_position_password] + char + password_field_text[
                                                                                  cursor_position_password:]
                        cursor_position_password += len(char)
                    elif len(balance_field_text) < 7 and focussed_field == 3 and pg.K_0 <= event.key <= pg.K_9:
                        balance_field_text = balance_field_text[:cursor_position_balance] + char + balance_field_text[
                                                                                                   cursor_position_balance:]
                        cursor_position_balance += len(char)

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Quit button
                if pg.Rect(1850, 20, 35, 25).collidepoint(event.pos):
                    page_running = False

                # Focus a textfield to enter text / focus no field
                if pg.Rect(720, 750, 475, 40).collidepoint(event.pos):
                    focussed_field = 1
                    register_status = ""
                elif pg.Rect(720, 840, 475, 40).collidepoint(event.pos):
                    focussed_field = 2
                    register_status = ""
                elif pg.Rect(720, 930, 475, 40).collidepoint(event.pos):
                    focussed_field = 3
                    register_status = ""
                else:
                    focussed_field = 0

                # Event when clicking the register button
                if pg.Rect(845, 1025, 195, 45).collidepoint(event.pos):
                    register_click()
            # Create a button hover effect
            elif event.type == pg.MOUSEMOTION:
                if pg.Rect(845, 1025, 195, 45).collidepoint(event.pos):
                    register_button = register_button_hover
                else:
                    register_button = register_button_default

        # Display transparent rectangles behind user inputs
        display_transparent_rect(screen, (710, 750), (475, 40), (129, 229, 248, 128))
        display_transparent_rect(screen, (710, 840), (475, 40), (129, 229, 248, 128))
        display_transparent_rect(screen, (710, 930), (475, 40), (129, 229, 248, 128))

        # Display the username and password field text
        display_text(screen, username_field_text, (720, 750), (0, 0, 0))
        display_text(screen, password_field_text, (720, 840), (0, 0, 0))
        display_text(screen, balance_field_text, (720, 930), (0, 0, 0))

        # Display the text input position indicator
        if focussed_field == 1:
            prefix_text = username_field_text[:cursor_position_username]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 750, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)
        elif focussed_field == 2:
            prefix_text = password_field_text[:cursor_position_password]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 840, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)
        elif focussed_field == 3:
            prefix_text = balance_field_text[:cursor_position_balance]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 930, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)

        # Display the login status
        display_text(screen, register_status, register_status_position, register_status_color, register_status_size)

        # Refresh the given database every 60 ticks
        timer_for_database_update += 1
        if timer_for_database_update % 60 == 0:
            loaded_data = load()

        # Refresh the screen
        pg.display.update()
        clock.tick(60)


# Start the main page
if __name__ == "__main__":
    register_window()
