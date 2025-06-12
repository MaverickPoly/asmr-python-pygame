import pygame
from settings import *



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(OBSTACLE_COLOR)

        self.rect = self.image.get_rect(topleft=(x, y))