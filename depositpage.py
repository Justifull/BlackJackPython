import pygame as pg
from database import load
from database import save
from layoutessentials import display_text
from layoutessentials import display_transparent_rect

deposit_amount_field_text = ""
deposit_status = ""
deposit_status_position = (850, 1000)
deposit_status_color = (255, 0, 0)

page_running = True


def deposit_window(username, password):
    global deposit_amount_field_text
    global deposit_status
    global deposit_status_position
    global deposit_status_color
    global page_running

    # Code to reinitialize variables when restarting the window
    deposit_amount_field_text = ""
    deposit_status = ""
    deposit_status_position = (850, 1000)
    deposit_status_color = (255, 0, 0)

    page_running = True

    # Initialize pygame
    pg.init()

    # Define width and height
    window_width, window_height = 1920, 1080

    # Font
    pg.font.init()
    font = pg.font.SysFont("Arial", 30)

    # Load images
    background = pg.image.load('graphics/deposit_screen.jpg')

    deposit_button = pg.image.load('graphics/buttons/deposit_button_deposit.png')
    deposit_button_default = pg.image.load('graphics/buttons/deposit_button_deposit.png')
    deposit_button_hover = pg.image.load('graphics/buttons/deposit_button_deposit_hover.png')

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
    cursor_position_deposit = 0
    cursor_width = 2

    # Function to validate the user inputs and leading to the next page
    def validate_userinput():
        global deposit_amount_field_text
        global deposit_status
        global deposit_status_position
        global deposit_status_color
        global page_running

        # Test if deposit amount field is not empty
        if deposit_amount_field_text:
            # Setting the correct login status and closing deposit window
            deposit_status = "Depositing.."
            deposit_status_position = [850, 1000]
            deposit_status_color = (0, 255, 0)
            page_running = False
            save(username, password, int(deposit_amount_field_text) + loaded_data[username][1])
        else:
            # Setting the correct login status
            deposit_status = "Please enter a value to deposit"
            deposit_status_position = [730, 1000]
            deposit_status_color = (255, 0, 0)

    # Function when pressing the deposit button
    def deposit_click():
        validate_userinput()

    # Main function for running the opened window
    while page_running:
        # Setup background
        screen.blit(background, (0, 0))
        screen.blit(deposit_button, (0, 0))

        # Eventmanager
        for event in pg.event.get():
            if event.type == pg.QUIT:
                page_running = False
            elif event.type == pg.KEYDOWN:
                # Navigate the indicator through the input text (left direction)
                if event.key == pg.K_LEFT and focussed_field == 1:
                    cursor_position_deposit = max(0, cursor_position_deposit - 1)

                # Navigate the indicator through the input text (right direction)
                if event.key == pg.K_RIGHT and focussed_field == 1:
                    cursor_position_deposit = min(len(deposit_amount_field_text), cursor_position_deposit + 1)

                # Validate the data by pressing enter button
                if event.key == pg.K_RETURN:
                    validate_userinput()

                # Delete character of the deposit amount and update indicator position
                elif event.key == pg.K_BACKSPACE:
                    if len(deposit_amount_field_text) > 0 and focussed_field == 1:
                        deposit_amount_field_text = deposit_amount_field_text[:max(0, cursor_position_deposit - 1)] + deposit_amount_field_text[cursor_position_deposit:]
                        cursor_position_deposit = max(0, cursor_position_deposit - 1)

                # Add a new character to username or password and update indicator position
                else:
                    char = event.unicode
                    if len(deposit_amount_field_text) < 7 and focussed_field == 1 and pg.K_0 <= event.key <= pg.K_9:
                        deposit_amount_field_text = deposit_amount_field_text[:cursor_position_deposit] + char + deposit_amount_field_text[cursor_position_deposit:]
                        cursor_position_deposit += len(char)

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Focus a textfield to enter text / focus no field
                if pg.Rect(720, 840, 475, 40).collidepoint(event.pos):
                    focussed_field = 1
                    login_status = ""
                else:
                    focussed_field = 0

                # Event when clicking the register text or login button
                if pg.Rect(850, 950, 190, 50).collidepoint(event.pos):
                    deposit_click()

            # Create a button hover effect
            elif event.type == pg.MOUSEMOTION:
                if pg.Rect(850, 950, 190, 50).collidepoint(event.pos):
                    deposit_button = deposit_button_hover
                else:
                    deposit_button = deposit_button_default

        # Display transparent rectangles behind user inputs
        display_transparent_rect(screen, (710, 750), (475, 40), (129, 229, 248, 128))
        display_transparent_rect(screen, (710, 840), (475, 40), (129, 229, 248, 128))

        # Display the deposit amount field text
        display_text(screen, f"{loaded_data[username][1]}$", (720, 750), (0, 0, 0))
        display_text(screen, deposit_amount_field_text, (720, 840), (0, 0, 0))

        # Display the text input position indicator
        if focussed_field == 1:
            prefix_text = deposit_amount_field_text[:cursor_position_deposit]
            prefix_width = font.size(prefix_text)[0]
            text_rect = pg.Rect(720, 840, 475, 40)
            pg.draw.line(screen, (0, 0, 0), (text_rect.left + prefix_width, text_rect.bottom - 5),
                         (text_rect.left + prefix_width, text_rect.top + 5), cursor_width)

        # Display the login status
        display_text(screen, deposit_status, deposit_status_position, deposit_status_color)

        # Refresh the given database every 60 ticks
        timer_for_database_update += 1
        if timer_for_database_update % 60 == 0:
            loaded_data = load()

        # Refresh the screen
        pg.display.update()
        clock.tick(60)


# Start the main page
if __name__ == "__main__":
    deposit_window("test", "test")
