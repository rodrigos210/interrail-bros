# ui/text.py

import pygame

def draw_text(
    screen,
    text,
    size,
    x,
    y,
    color=(0, 0, 0),
    center=True
):
    font = pygame.font.Font("ui/LowresPixel-Regular.otf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    screen.blit(text_surface, text_rect)
