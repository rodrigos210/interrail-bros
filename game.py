# game.py

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from player import Player
from level import Level
from levels.level_manager import LevelManager
from ui.map_screen import draw_map


GAME_MAP = "map"
GAME_LEVEL = "level"
GAME_END = "end"

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Interrail Bros.")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player()
        self.level_manager = LevelManager()
        self.level = Level(self.level_manager.get_selected_layout())
        self.player.rect.topleft = (self.level.spawn_x, self.level.spawn_y)
        self.game_state = GAME_MAP
        self.heart_image = pygame.image.load("ui/lives.png").convert_alpha()
        



    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # --- Keyboard navigation ---
            if event.type == pygame.KEYDOWN and self.game_state == GAME_MAP:
                if event.key == pygame.K_RIGHT:
                    self.level_manager.move_selection(1)

                elif event.key == pygame.K_LEFT:
                    self.level_manager.move_selection(-1)

                elif event.key == pygame.K_RETURN:
                    layout = self.level_manager.get_selected_layout()
                    self.level = Level(layout)
                    self.player = Player()
                    self.player.rect.topleft = (
                        self.level.spawn_x,
                        self.level.spawn_y
                    )
                    self.game_state = GAME_LEVEL

            # --- Mouse selection ---
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == GAME_MAP:
                mx, my = event.pos

                for i, level in enumerate(self.level_manager.levels):
                    x, y = level["pos"]
                    if (mx - x) ** 2 + (my - y) ** 2 <= 12 ** 2:
                        self.level_manager.selected_index = i



    def reset_player_position(self):
        self.player.rect.topleft = (
            self.level.spawn_x,
            self.level.spawn_y
        )
        self.player.velocity_y = 0


    def update(self):
        if self.game_state == GAME_LEVEL:
            #self.level.check_player_hole_entry(self.player)
            self.player.update(self.level.get_colliders(self.player))
            self.level.update(self.player)
            self.level.update_state(self.player)
            self.level.check_exit(self.player)
            self.level.scroll(self.player)

            if self.level.state == "exiting" and self.level_finished():
                if self.level_manager.advance():
                    self.game_state = GAME_MAP
                else:
                    self.game_state = GAME_END
        if self.player.rect.top > SCREEN_HEIGHT + 50:
            self.player.take_damage()
            self.reset_player_position()

        if self.player.lives <= 0:
            self.game_state = GAME_MAP
            self.level_manager.reset_progress()


        
    def draw_lives(self):
        spacing = 6
        x_start = 20
        y = 20

        for i in range(self.player.lives):
            x = x_start + i * (self.heart_image.get_width() + spacing)
            self.screen.blit(self.heart_image, (x, y))



    def draw(self):
        if self.game_state == GAME_MAP:
            draw_map(self.screen, self.level_manager)

            
        elif self.game_state == GAME_LEVEL:
            self.screen.fill(BG_COLOR)
            self.level.draw(self.screen, self.player)
            self.player.draw(self.screen)
            # --- LIVES HUD ---
            self.draw_lives()
            

        pygame.display.flip()

