import pygame
from levels.level_data import (
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5,
    LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9
)

LEVEL_DATA = [
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5,
    LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9
]

class LevelManager:
    def __init__(self):
        self.levels = [
            {"name": "POL", "rect": pygame.Rect(70, 215, 58, 32).inflate(-6, -6)},
            {"name": "AUS", "rect": pygame.Rect(200, 215, 52, 28).inflate(-6, -6)},
            {"name": "SVK", "rect": pygame.Rect(300, 250, 52, 28).inflate(-6, -6)},
            {"name": "HUN", "rect": pygame.Rect(400, 270, 52, 28).inflate(-6, -6)},
            {"name": "SER", "rect": pygame.Rect(550, 290, 52, 28).inflate(-6, -6)},
            {"name": "MON", "rect": pygame.Rect(650, 320, 52, 28).inflate(-6, -6)},
            {"name": "BHZ", "rect": pygame.Rect(430, 320, 52, 28).inflate(-6, -6)},
            {"name": "CRO", "rect": pygame.Rect(380, 295, 52, 28).inflate(-6, -6)},
            {"name": "SVN", "rect": pygame.Rect(340, 265, 52, 28).inflate(-6, -6)},
        ]

        self.current_index = 0      # progress
        self.selected_index = 0     # cursor

    def move_selection(self, direction):
        self.selected_index += direction
        self.selected_index = max(0, min(self.selected_index, len(self.levels) - 1))

    def get_selected_level(self):
        return self.levels[self.selected_index]

    def get_selected_layout(self):
        """Return the tile layout for the currently selected level."""
        return LEVEL_DATA[self.selected_index]

    def advance(self):
        """Mark current level complete and move on. Returns True if more levels remain."""
        self.current_index = self.selected_index + 1
        if self.current_index < len(self.levels):
            self.selected_index = self.current_index
            return True
        return False

    def reset_progress(self):
        self.current_index = 0
        self.selected_index = 0
