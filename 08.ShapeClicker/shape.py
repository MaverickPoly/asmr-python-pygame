import pygame
from settings import *
import time


class Shape:
    def __init__(self, x, y, color, width, height):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.created_time = time.time()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=BORDER_RADIUS)


