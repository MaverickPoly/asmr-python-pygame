import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH - ENEMY_PADDING, ENEMY_HEIGHT - ENEMY_PADDING))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

