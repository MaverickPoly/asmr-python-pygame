import pygame
from settings import * 


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], up_key, down_key):
        super().__init__()

        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(GRAY)
        
        self.rect = self.image.get_rect(center=pos)

        self.up_key = up_key
        self.down_key = down_key

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.up_key]:
            self.rect.y -= PADDLE_SPEED
        if keys[self.down_key]:
            self.rect.y += PADDLE_SPEED

    def check_constraints(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + PADDLE_HEIGHT >= HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT

    def update(self):
        self.get_input()
        self.check_constraints()
