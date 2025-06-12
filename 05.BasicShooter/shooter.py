import pygame

from settings import *


class Shooter(pygame.sprite.Sprite):
    def __init__(self, image, x, y, screen):
        super().__init__()

        self.image = image
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.bullets = []
        self.max_bullets = 4

    def update(self):
        for bullet in self.bullets:
            bullet.y -= BULLET_SPEED

        for bullet in self.bullets[:]:
            if bullet.y + bullet.height < 0:
                self.bullets.remove(bullet)

    def draw(self):
        self.update()

        for bullet in self.bullets:
            pygame.draw.rect(self.screen, WHITE, bullet)

        self.screen.blit(self.image, self.rect)

    def shoot(self):
        if len(self.bullets) < self.max_bullets:
            new_bullet = pygame.Rect(self.rect.centerx - BULLET_WIDTH / 2, self.rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
            self.bullets.append(new_bullet)
