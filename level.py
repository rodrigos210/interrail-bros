# level.py

import pygame
from settings import SCREEN_HEIGHT, CAMERA_LEFT_THRESHOLD, CAMERA_RIGHT_THRESHOLD, SCREEN_WIDTH
from levels.level_data import LEVEL_1
from ui.text import draw_text
from player import Player
import math


TILE_SIZE = 40

class Level:
    def __init__(self, layout=None):
        if layout is None:
            layout = LEVEL_1

        self.layout = layout
        self.platforms = []
        self.revisor_spawns = []

        self.ui_font = pygame.font.Font("ui/LowresPixel-Regular.otf", 18)

        self.platform_tiles = {
            "#": pygame.image.load("visuals/platform1.png").convert_alpha(),
            "W": pygame.image.load("visuals/plataformas/parede_teste.png").convert_alpha(),
            "T": pygame.image.load("visuals/plataformas/terra1.png").convert_alpha(),
            "R": pygame.image.load("visuals/plataformas/relva1.png").convert_alpha(),
            "w": pygame.image.load("visuals/plataformas/parede_teste3.png").convert_alpha(),
            "M": pygame.image.load("visuals/plataformas/madeira1.png").convert_alpha(),
            "m": pygame.image.load("visuals/plataformas/madeira2.png").convert_alpha(),
            "S": pygame.image.load("visuals/plataformas/stone_c3.png").convert_alpha(),
            "s": pygame.image.load("visuals/plataformas/stone_c2.png").convert_alpha(),
            "A": pygame.image.load("visuals/plataformas/sand.png").convert_alpha(),
            "a": pygame.image.load("visuals/plataformas/sand2.png").convert_alpha()
        }
        self.load_level(self.layout)

        # floor_height = self.platform_tiles["#"].get_height()
        # self.floor = pygame.Rect(
        #     0,
        #     SCREEN_HEIGHT - TILE_SIZE,
        #     5000,
        #     TILE_SIZE
        # )

        # self.floor = pygame.Rect(0, SCREEN_HEIGHT - 40, 5000, 40)
        self.world_shift = 0
        self.level_width = len(self.layout[0]) * TILE_SIZE

        self.background_images = [
            # {
            #     "name": "palace1",
            #     "img": pygame.image.load(
            #         "visuals/backgrounds/pol_bg_1.png"
            #     ).convert_alpha(),
            #     "x": 1000,
            #     "y": SCREEN_HEIGHT - 300,
            #     "parallax": 0.4
            # },
            # {
            #     "name": "far_bg_1",
            #     "img": pygame.image.load(
            #         "visuals/backgrounds/pol_bg_2.png"
            #     ).convert_alpha(),
            #     "x": 0,
            #     "y": 0,
            #     "parallax": 0.1
            # },
            {
                "name": "far_bg_2",
                "img": pygame.image.load(
                    "visuals/backgrounds/pol_bg_5.png"
                ).convert_alpha(),
                "x": 0,
                "y": -100,
                "parallax": 0.05
            }
        ]


        self.sign_images = {
            "Warsaw": pygame.image.load(
                "visuals/placas/warsaw_placa.png"
            ).convert_alpha()
        }

        self.background_signs = [
            {
                "name": "Warsaw",
                "x": 170,
                "y": SCREEN_HEIGHT - 150
            }
        ]

        self.intro_text = {
            "text": (
                "Olá, amigo! Bem vindo à Polónia.\n"
                "Os controlos são muito simples,\n"
                "é tudo nas setas por isso tu safas-te\n"
                "Neste nível, para te ajudar, prendi o pica.\n"
                "Mas nos próximos ele vai te logicamente perseguir \n"
                "e não há como te livrares dele."
            ),
            "x": 100,
            "y": SCREEN_HEIGHT - 400,
            "width": 500,
            "size": 25,
            "color": (255, 255, 255)
        }

        self.background_texts = [
            {
                "text": "Pica",
                "x": 20,
                "y": SCREEN_HEIGHT - 190,
                "size": 15,
                "color": "white"
            },
            {
                "text": "KRAKÓW",
                "x": 1300,
                "y": SCREEN_HEIGHT - 200,
                "size": 32,
                "color": (40, 40, 40)
            },
            {
                "text": "OŚWIĘCIM",
                "x": 2500,
                "y": SCREEN_HEIGHT - 200,
                "size": 32,
                "color": (40, 40, 40)
            }
        ]


        self.sleep_monsters = [
            {
                "rect": pygame.Rect(600, SCREEN_HEIGHT - 140, 32, 32),
                "base_x": 600,
                "base_y": SCREEN_HEIGHT - 140,
                "phase": 0,
                "alive": True
            }
        ]

        
        self.revisors = []

        REVISOR_WIDTH = 30
        REVISOR_HEIGHT = 50

        for spawn_x in self.revisor_spawns:
            ground_y = self.find_ground_y(spawn_x)

            if ground_y is None:
                continue  # invalid spawn, skip safely

            self.revisors.append({
                "rect": pygame.Rect(
                    spawn_x - REVISOR_WIDTH // 2,
                    ground_y - REVISOR_HEIGHT,
                    REVISOR_WIDTH,
                    REVISOR_HEIGHT
                ),
                "base_x": spawn_x - REVISOR_WIDTH // 2,
                "base_y": ground_y - REVISOR_HEIGHT,
                "direction": -1,
                "speed": 1.2,
                "walk_timer": 0,
                "frame_index": 0,
                "alive": True,
                "velocity_y": 0
            })


        # self.revisors = [
        #     {
        #         "rect": pygame.Rect(1000, SCREEN_HEIGHT - 90, 30, 50),
        #         "base_x": 0, 
        #         "base_y": SCREEN_HEIGHT-90,
        #         "direction": -1,
        #         "speed": 1.2,
        #         "walk_timer": 0,
        #         "frame_index": 0,
        #         "alive": True,
        #         "velocity_y": 0
        #     }
        # ]


        self.state = "intro"
        self.intro_duration = 2500
        self.intro_start_time = pygame.time.get_ticks()
        self.intro_walk_distance = 80
        self.intro_start_x = None
        self.exit_train_rect = pygame.Rect(self.level_width-200, SCREEN_HEIGHT - 120, 120, 80)
        self.transport_type = "train"
        self.train_rect = pygame.Rect(40, SCREEN_HEIGHT-120, 120,80)
        self.spawn_x = self.train_rect.left + 60
        self.spawn_y = self.train_rect.bottom - 60
        # self.floor_tile = pygame.image.load(
        #     "visuals/floor1.png"
        # ).convert_alpha()
        self.platform_tile = pygame.image.load("visuals/platform1.png").convert_alpha()
        self.train_tile = pygame.image.load("visuals/train1.png").convert_alpha()
        self.exit_train_tile = pygame.image.load("visuals/train1.png").convert_alpha()
        self.sleep_monster_image = pygame.image.load(
            "visuals/mobs/sleep_monster.png"
        ).convert_alpha()

        self.revisor_frames = [
            pygame.image.load("visuals/mobs/train_rev_walk1.png").convert_alpha(),
            pygame.image.load("visuals/mobs/train_rev_walk2.png").convert_alpha()
        ]

    def load_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile in self.platform_tiles:
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.platforms.append({
                        "rect": rect,
                        "type": tile
                    })

                elif tile == "P":
                    # store spawn X at tile center
                    self.revisor_spawns.append(x + TILE_SIZE // 2)


    def scroll(self, player):
        # Scroll right
        if player.rect.x > CAMERA_RIGHT_THRESHOLD:
            shift = player.rect.x - CAMERA_RIGHT_THRESHOLD

            if self.world_shift + shift > self.level_width - SCREEN_WIDTH:
                shift = self.level_width - SCREEN_WIDTH - self.world_shift

            if shift > 0:
                player.rect.x -= shift
                self.world_shift += shift

                for platform in self.platforms:
                    platform["rect"].x -= shift
                for monster in self.sleep_monsters:
                    monster["base_x"] -= shift
                # for hole in self.floor_holes:
                #     hole.x -= shift
                for revisor in self.revisors:
                    revisor["base_x"] -= shift
                for sign in self.background_signs:
                    sign["x"] -= shift
                # for image in self.background_images:
                #     image["x"] -= shift
                for text in self.background_texts:
                    text["x"] -= shift
                # self.floor.x -= shift
                self.exit_train_rect.x -= shift   
                self.intro_text["x"] -= shift




        # Scroll left
        elif player.rect.x < CAMERA_LEFT_THRESHOLD:
            shift = CAMERA_LEFT_THRESHOLD - player.rect.x

            if self.world_shift - shift < 0:
                shift = self.world_shift

            if shift > 0:
                player.rect.x += shift
                self.world_shift -= shift

                for platform in self.platforms:
                    platform["rect"].x += shift
                for monster in self.sleep_monsters:
                    monster["base_x"] += shift
                # for hole in self.floor_holes:
                #     hole.x += shift
                for revisor in self.revisors:
                    revisor["base_x"] += shift
                for sign in self.background_signs:
                    sign["x"] += shift
                for text in self.background_texts:
                    text["x"] += shift
                # for image in self.background_images:
                #     image["x"] += shift
                # self.floor.x += shift
                self.exit_train_rect.x += shift   
                self.intro_text["x"] += shift


    
    def get_colliders(self, player=None):
        return [p["rect"] for p in self.platforms]

    def draw_platforms(self, screen):
        for platform in self.platforms:
            rect = platform["rect"]
            tile = self.platform_tiles[platform["type"]]

            y = rect.top - (tile.get_height() - rect.height)

            screen.blit(tile, (rect.x, y))


    def draw_train(self, screen):
        img_w = self.train_tile.get_width()
        img_h = self.train_tile.get_height()

        # Anchor train to the ground using the rect
        x = self.train_rect.centerx - img_w // 2
        y = self.train_rect.bottom - img_h

        screen.blit(self.train_tile, (x, y))

    def draw_exit_train(self, screen):
        img_w = self.train_tile.get_width()
        img_h = self.train_tile.get_height()

        # Anchor train to the ground using the rect
        x = self.exit_train_rect.centerx - img_w // 2
        y = self.exit_train_rect.bottom - img_h

        screen.blit(self.exit_train_tile, (x, y))

    def draw_background_signs(self, screen):
        for sign in self.background_signs:
            image = self.sign_images[sign["name"]]

            screen.blit(
                image,
                (
                    sign["x"],
                    sign["y"]
                )
            )
    
    def draw_background_images(self, screen):
        for bg in self.background_images:
            draw_x = bg["x"] - self.world_shift * bg["parallax"]

            screen.blit(
                bg["img"],
                (draw_x, bg["y"])
            )



    def draw_background_texts(self, screen):
        for t in self.background_texts:
            draw_text(
                screen,
                t["text"],
                t["size"],
                t["x"],
                t["y"],
                t["color"]
            )

    def draw_text_block(self, surface, text, x, y, width, font, color, line_spacing=4):
        words = []
        for line in text.split("\n"):
            words.append(line.split(" "))
            words.append(["\n"])
        words.pop()  # remove last extra newline

        x_start = x
        y_offset = 0
        line = ""

        for word_group in words:
            if word_group == ["\n"]:
                rendered = font.render(line, True, color)
                surface.blit(rendered, (x_start, y + y_offset))
                y_offset += font.get_height() + line_spacing
                line = ""
                continue

            for word in word_group:
                test_line = line + word + " "
                if font.size(test_line)[0] <= width:
                    line = test_line
                else:
                    rendered = font.render(line, True, color)
                    surface.blit(rendered, (x_start, y + y_offset))
                    y_offset += font.get_height() + line_spacing
                    line = word + " "

        if line:
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x_start, y + y_offset))



    def draw(self, screen, player):
        # draw floor
        #pygame.draw.rect(screen, (50, 200, 50), self.floor)
        self.draw_background_images(screen)
        # self.draw_floor(screen)
        self.draw_platforms(screen)
        pygame.draw.rect(screen, (20,20,20), self.exit_train_rect)

        
        self.draw_background_signs(screen)
        self.draw_background_texts(screen)
        self.draw_text_block(
            screen,
            self.intro_text["text"],
            self.intro_text["x"],
            self.intro_text["y"],
            self.intro_text["width"],
            self.ui_font,
            self.intro_text["color"]
        )
        
        



        # draw platforms
        # for platform in self.platforms:
        #     pygame.draw.rect(screen, (60, 60, 60), platform)

        if self.state == "intro":
            draw_text(screen, "Arrival by train", 24, SCREEN_WIDTH // 2, 80)
            self.draw_train(screen)

        elif self.state == "exiting":
            draw_text(screen, "Next stop...", 24, SCREEN_WIDTH // 2, 80)

        self.draw_exit_train(screen)

        progress = min(
            player.distance_travelled / self.level_width,
            1.0
        )
        bar_width = 200
        bar_height = 10
        x = SCREEN_WIDTH - bar_width - 20
        y = 20

        pygame.draw.rect(
            screen,
            (180, 180, 180),
            (x, y, bar_width, bar_height)
        )

        fill_width = int(bar_width * progress)

        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (x, y, fill_width, bar_height)
        )
        for monster in self.sleep_monsters:
            if not monster["alive"]:
                continue

            rect = monster["rect"]
            screen.blit(
                self.sleep_monster_image,
                (
                    rect.centerx - self.sleep_monster_image.get_width() // 2,
                    rect.bottom - self.sleep_monster_image.get_height()
                )
            )


        for revisor in self.revisors:
            if not revisor["alive"]:
                continue

            image = self.revisor_frames[revisor["frame_index"]]

            if revisor["direction"] < 0:
                image = pygame.transform.flip(image, True, False)

            screen.blit(
                image,
                (
                    revisor["rect"].centerx - image.get_width() // 2,
                    revisor["rect"].bottom - image.get_height()
                )
            )

    def update_state(self, player):
        if self.state == "intro":
            if self.intro_start_x == None:
                self.intro_start_x = player.rect.x

            player.can_move = False
            player.scripted_velocity_x = 2  # walking right

            if player.rect.x >= self.intro_start_x + self.intro_walk_distance:
                player.scripted_velocity_x = 0
                player.can_move = True
                self.state = "playing"
        elif self.state == "exiting":
            player.scripted_velocity_x = 2

            if player.rect.left > self.exit_train_rect.right:
                player.scripted_velocity_x = 0
                print("LOAD NEXT LEVEL HERE")

    def respawn_player(self, player):
        player.rect.topleft = (self.spawn_x, self.spawn_y)
        player.velocity_y = 0

    def is_solid_at(self, x, y):
        for platform in self.platforms:
            if platform["rect"].collidepoint(x, y):
                return True
        return False


    def is_on_ground(self, rect):
        return self.is_solid_at(rect.centerx, rect.bottom + 1)

    
    def resolve_monster_horizontal_collision(self, monster):
        for platform in self.platforms:
            if monster["rect"].colliderect(platform["rect"]):
                if monster["direction"] > 0:
                    # Moving right → hit left side of platform
                    monster["rect"].right = platform["rect"].left
                else:
                    # Moving left → hit right side of platform
                    monster["rect"].left = platform["rect"].right

                monster["base_x"] = monster["rect"].x
                monster["direction"] *= -1  # turn around

    # def find_ground_y(self, x):
    #         for platform in self.platforms:
    #             if platform["rect"].left <= x <= platform["rect"].right:
    #                 return platform["rect"].top
    #         return None
    
    def find_ground_y(self, x):
        ground_y = None

        for platform in self.platforms:
            rect = platform["rect"]
            if rect.left <= x <= rect.right:
                if ground_y is None or rect.top < ground_y:
                    ground_y = rect.top

        return ground_y


    def update(self, player):


        # --- Monster motion ---
        for monster in self.sleep_monsters:
            if not monster["alive"]:
                continue

            monster["phase"] += 0.05

            x_offset = math.sin(monster["phase"]) * 20
            y_offset = math.cos(monster["phase"] * 2) * 6

            monster["rect"].x = monster["base_x"] + int(x_offset)
            monster["rect"].y = monster["base_y"] + int(y_offset)

        # --- Hazard: falling into the void ---
        if player.rect.top > SCREEN_HEIGHT + 50:
            player.take_damage()
            self.respawn_player(player)

        # --- Monster collisions ---
        for monster in self.sleep_monsters:
            if not monster["alive"]:
                continue

            if player.rect.colliderect(monster["rect"]):
                player_bottom = player.rect.bottom
                monster_top = monster["rect"].top

                if player.velocity_y > 0 and player_bottom - monster_top < 12:
                    # STOMP!
                    monster["alive"] = False
                    player.velocity_y = -8
                else:
                    player.take_damage()

        for revisor in self.revisors:
            if not revisor["alive"]:
                continue

            # --- CHASE PLAYER ---
            dx = player.rect.centerx - revisor["rect"].centerx

            CHASE_DISTANCE = 600
            STOP_DISTANCE = 20

            if abs(dx) < CHASE_DISTANCE and abs(dx) > STOP_DISTANCE:
                revisor["direction"] = 1 if dx > 0 else -1
                revisor["base_x"] += revisor["direction"] * revisor["speed"]

            # --- APPLY X POSITION ---
            revisor["rect"].x = int(revisor["base_x"])
            self.resolve_monster_horizontal_collision(revisor)

            # --- HOLE DETECTION ---
            probe_x = revisor["rect"].centerx + revisor["direction"] * 16
            probe_y = revisor["rect"].bottom + 2

            on_ground = self.is_on_ground(revisor["rect"])

            floor_ahead = self.is_solid_at(probe_x, probe_y)

            if on_ground and not floor_ahead:
                revisor["velocity_y"] = -10
                revisor["base_x"] += revisor["direction"] * 20

            # --- GRAVITY ---
            revisor["velocity_y"] += 0.45
            revisor["rect"].y += revisor["velocity_y"]

            # --- VERTICAL COLLISION WITH TILES ---
            for platform in self.platforms:
                tile_rect = platform["rect"]
                if revisor["rect"].colliderect(tile_rect):
                    if revisor["velocity_y"] > 0:  # falling
                        revisor["rect"].bottom = tile_rect.top
                        revisor["velocity_y"] = 0
                    elif revisor["velocity_y"] < 0:  # jumping
                        revisor["rect"].top = tile_rect.bottom
                        revisor["velocity_y"] = 0

            # --- FLOOR COLLISION ---

            # --- WALK ANIMATION ---
            revisor["walk_timer"] += 1
            if revisor["walk_timer"] > 15:
                revisor["walk_timer"] = 0
                revisor["frame_index"] = (revisor["frame_index"] + 1) % 2



        

        for revisor in self.revisors:
            if not revisor["alive"]:
                continue

            if player.rect.colliderect(revisor["rect"]):
                # Revisor cannot be stomped
                player.take_damage()









    def check_exit(self, player):
        if self.state == "playing" and player.rect.colliderect(self.exit_train_rect):
            self.state = "exiting"
            player.can_move = False
            player.scripted_velocity_x = 2



