from settings import *
import pygame as pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, screen: pygame.Surface):
        super().__init__()

        self.image = image
        self.speed = speed
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)

