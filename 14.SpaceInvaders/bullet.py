import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy):
        super().__init__()
        self.enemy = enemy

        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        color = ENEMY_BULLET_COLOR if enemy else BULLET_COLOR
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = -ENEMY_BULLET_SPEED if enemy else BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom <= 0:
            self.kill()
        if self.enemy and self.rect.top >= HEIGHT:
            self.kill()
