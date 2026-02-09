import pygame
import random

class Monster:
    def __init__(self, rect):
        self.rect = rect

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (120, 0, 120), self.rect)

class SleepMonster:
    def __init__(self, x, y):
        super().__init__(pygame.Rect(x, y, 32, 32))
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * 1
        if random.random() < 0.01:
            self.direction *= 1
    