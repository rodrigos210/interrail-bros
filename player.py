# player.py

import pygame
from settings import (
    SCREEN_HEIGHT,
    GRAVITY,
    PLAYER_SPEED,
    JUMP_FORCE
)

class Player:
    def __init__(self):
        self.width = 24
        self.height = 44

        self.rect = pygame.Rect(100, 100, self.width, self.height)

        self.max_lives = 3
        self.lives = self.max_lives

        self.invulnerable = False
        

        self.inv_start_time = 0
        self.inv_duration = 1500 #ms

        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.was_on_ground = True
        self.can_move = True
        self.scripted_velocity_x = 0
        self.distance_travelled = 0
        self.prev_x = self.rect.x
        self.idle_img = pygame.image.load(
            "visuals/avatar/idle1.png"
        ).convert_alpha()

        self.walk_frames = [
            pygame.image.load("visuals/avatar/walk1.png").convert_alpha(),
            pygame.image.load("visuals/avatar/walk2.png").convert_alpha()
        ]

        self.jump_img = pygame.image.load("visuals/avatar/jump1.png").convert_alpha()

        self.fall_img = pygame.image.load("visuals/avatar/fall1.png").convert_alpha()

        self.land_img = pygame.image.load("visuals/avatar/land1.png").convert_alpha()
        self.crouch_img = pygame.image.load("visuals/avatar/land1.png").convert_alpha()

        self.facing_right = True
        self.crouching = False

        self.animations = {
            "idle": [self.idle_img],
            "walk": [self.walk_frames[0], self.walk_frames[1]],
            "jump": [self.jump_img],
            "fall": [self.fall_img],
            "land": [self.land_img],
            "crouch": [self.crouch_img],
        }

        self.state = "idle"
        self.walk_index = 0
        self.animation_timer = 0
        self.animation_speed = 120  # ms per frame
        self.landing_timer = 0
        self.landing_duration = 120
        self.last_update = pygame.time.get_ticks()
        self.current_image = self.idle_img



    def handle_input(self):
        if not self.can_move:
            self.velocity_x=self.scripted_velocity_x
            return
        
        self.velocity_x = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

        if keys[pygame.K_DOWN] and self.on_ground:
            self.crouching = True
            self.velocity_x = 0
        else:
            self.crouching = False


    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def move_horizontal(self, platforms):
        self.rect.x += self.velocity_x

        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_x > 0:  # moving right
                    self.rect.right = platform.left
                elif self.velocity_x < 0:  # moving left
                    self.rect.left = platform.right
        if self.velocity_x > 0:
            self.facing_right = True
        elif self.velocity_x < 0:
            self.facing_right = False
        
    def update_state(self):
        now = pygame.time.get_ticks()

        # Landing has top priority
        if self.on_ground and (now - self.landing_timer < self.landing_duration):
            self.state = "land"
            return

        if self.crouching and self.on_ground:
            self.state = "crouch"

        elif not self.on_ground:
            if self.velocity_y < 0:
                self.state = "jump"
            else:
                self.state = "fall"

        elif self.velocity_x != 0:
            self.state = "walk"

        else:
            self.state = "idle"


    # def check_vertical_collisions(self, platforms):
    #     self.on_ground = False

    #     for platform in platforms:
    #         if self.rect.colliderect(platform):
    #             if self.velocity_y > 0:  # falling
    #                 self.rect.bottom = platform.top
    #                 self.velocity_y = 0
    #                 self.on_ground = True
    #             elif self.velocity_y < 0:  # jumping up
    #                 self.rect.top = platform.bottom
    #                 self.velocity_y = 0
    
    def check_vertical_collisions(self, platforms):
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:  # falling
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # jumping up
                    self.rect.top = platform.bottom
                    self.velocity_y = 0


    def update_animation(self):
        if self.state == "idle":
            self.current_image = self.idle_img
        
        now = pygame.time.get_ticks()

        if self.state == "walk":
            if now - self.last_update > self.animation_speed:
                self.walk_index = (self.walk_index + 1) % len(self.walk_frames)
                self.last_update = now
            self.current_image = self.walk_frames[self.walk_index]

        elif self.state == "jump":
            self.current_image = self.jump_img

        elif self.state == "fall":
            self.current_image = self.fall_img

        elif self.state == "crouch":
            self.current_image = self.crouch_img

        elif self.state == "land":
            self.current_image = self.land_img



    def update(self, platforms):
        self.handle_input()
            
        self.move_horizontal(platforms)
        dx = self.rect.x - self.prev_x
        self.distance_travelled += abs(dx)
        self.prev_x = self.rect.x

        self.apply_gravity()
        self.check_vertical_collisions(platforms)

        if self.rect.left < 0:
            self.rect.left = 0


        if not self.was_on_ground and self.on_ground:
            self.landing_timer = pygame.time.get_ticks()

        self.was_on_ground = self.on_ground
        # NEW — animation logic layer
        self.update_state()
        self.update_animation()

        if self.invulnerable:
            if pygame.time.get_ticks() - self.inv_start_time > self.inv_duration:
                self.invulnerable = False

        


    def draw(self, screen):
        # Blink effect: skip drawing every other interval
        if self.invulnerable:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return

        image = self.current_image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        screen.blit(
            image,
            (
                self.rect.centerx - image.get_width() // 2,
                self.rect.bottom - image.get_height()
            )
        )

        

    def take_damage(self):
        if self.invulnerable:
            return
        
        self.lives -= 1
        self.invulnerable = True
        self.inv_start_time = pygame.time.get_ticks()

        #small knockback
        self.velocity_x = -6
        self.velocity_y = -6


