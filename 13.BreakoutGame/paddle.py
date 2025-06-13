import pygame
from settings import *



class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_W, PADDLE_H))
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 30

        self.speed = 0

    def update(self):
        self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def move_right(self):
        self.speed = PADDLE_SPEED
    
    def move_left(self):
        self.speed = -PADDLE_SPEED
    
    def stop(self):
        self.speed = 0
