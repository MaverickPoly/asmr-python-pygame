import pygame
from settings import *
import random


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        pygame.draw.circle(self.image, ORANGE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
        self.reset()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1

        if self.rect.top > HEIGHT:
            return True
        return False

    def bounce(self):
        self.speed_y *= -1

    def reset(self):
        self.rect.centerx = WIDTH / 2
        self.rect.centery = WIDTH / 2
        self.speed_x = random.choice([BALL_SPEED, -BALL_SPEED])
        self.speed_y = -BALL_SPEED

