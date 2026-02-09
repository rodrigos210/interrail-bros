import pygame
from ui.text import draw_text

CITY_RADIUS = 12
HOVER_RADIUS = 18
#MAP_IMAGE = pygame.image.load("visuals/map1.png").convert()
MAP_IMAGE = None

def draw_map(screen, level_manager):
    # screen.fill((220, 235, 245))
    # map_image = pygame.image.load("visuals/map1.png").convert()

    global MAP_IMAGE

    if MAP_IMAGE is None:
        MAP_IMAGE = pygame.image.load("visuals/map1.png").convert()

    screen.blit(MAP_IMAGE, (0,0))


    mouse_pos = pygame.mouse.get_pos()

    for i, level in enumerate(level_manager.levels):
        #x, y = level["pos"]

        # Base color
        color = (100, 100, 100)

        # Completed
        if i < level_manager.current_index:
            color = (140, 140, 140)

        # Hover effect
        # dist_sq = (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2
        # hovering = dist_sq < CITY_RADIUS ** 2

        for i, level in enumerate(level_manager.levels):
            rect = level["rect"]

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=4)

            if i == level_manager.selected_index:
                pygame.draw.rect(screen, (255, 180, 0), rect, 2, border_radius=4)

        
        # draw_text(screen, level["name"][:3], 16, x, y + 28)

    # draw_text(
    #     screen,
    #     "Use ← → or click. ENTER to travel.",
    #     22,
    #     screen.get_width() // 2,
    #     360
    # )
