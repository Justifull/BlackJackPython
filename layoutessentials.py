import pygame as pg


def display_text(screen, text, coordinates, color, size=30, font_path=None):
    if font_path is not None:
        font = pg.font.Font(font_path, size)
    else:
        font = pg.font.SysFont("Arial", size)

    text_render = font.render(text, True, color)
    screen.blit(text_render, coordinates)


def display_button(screen, rectangle, text, color, text_color):
    pg.Rect(rectangle)

    pg.draw.rect(screen, color, rectangle)

    button_font = pg.font.Font(None, 36)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rectangle.center)

    screen.blit(text_surface, text_rect)


def display_transparent_rect(screen, coordinates, size, color):
    transparent = pg.Surface(size, pg.SRCALPHA)
    pg.draw.rect(transparent, color, (0, 0, size[0], size[1]))
    screen.blit(transparent, coordinates)


def scale_image(image, max_width, max_height):
    width, height = image.get_size()

    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)

        scaled_image = pg.transform.scale(image, (int(width * ratio), int(height * ratio)))

        return scaled_image
    else:
        return image
