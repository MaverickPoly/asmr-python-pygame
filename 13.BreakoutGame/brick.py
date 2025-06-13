import pygame
from settings import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH - BRICK_PADDING, BRICK_HEIGHT - BRICK_PADDING))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))