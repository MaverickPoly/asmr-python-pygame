import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((PLAYER_W, PLAYER_H))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(bottom=HEIGHT, centerx=WIDTH / 2 - PLAYER_W / 2)

        self.y_velocity = 0
        self.on_ground = False

    def update(self, obstacles: pygame.sprite.Group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED

        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # UP
                if self.y_velocity > 0 and self.rect.bottom > obstacle.rect.top and self.rect.top < obstacle.rect.top:
                    self.y_velocity = 0
                    self.on_ground = True
                    self.rect.bottom = obstacle.rect.top
                    break

                # DOWN
                if self.y_velocity < 0 and self.rect.top < obstacle.rect.bottom and self.rect.bottom > obstacle.rect.bottom:
                    self.y_velocity = 0
                    self.rect.top = obstacle.rect.bottom
                    break

                # RIGHT
                if self.rect.left < obstacle.rect.right and self.rect.right > obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    break

                # LEFT
                if self.rect.right > obstacle.rect.left and self.rect.left < obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    break


        if self.rect.left <= 0: # LEFT
            self.rect.left = 0
        if self.rect.right >= WIDTH: # RIGHT
            self.rect.right = WIDTH
        if self.rect.bottom >= HEIGHT: # DOWN
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.y_velocity = 0


    def jump(self):
        if self.on_ground:
            self.y_velocity = -JUMP_FORCE
            self.on_ground = False
