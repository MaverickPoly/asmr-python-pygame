import pygame
from settings import *
from random import choice

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], color):
        super().__init__()
        self.pos = pos

        self.image = pygame.Surface((RADIUS, RADIUS), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (RADIUS / 2, RADIUS / 2), RADIUS / 2)
        self.rect = self.image.get_rect(center=pos)

        self.vector = pygame.Vector2(choice([-1, 1]), choice([-1, 1]))

    def move(self):
        self.rect.center += self.vector * CIRCLE_SPEED        

    def reset(self):
        self.vector = pygame.Vector2(choice([-1, 1]), choice([-1, 1]))
        self.rect = self.image.get_rect(center=self.pos)

    def handle_collision(self, players_group, events):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vector.y *= -1
        if self.rect.left <= 0:
            self.reset()
            pygame.event.post(events[0])

        if self.rect.right >= WIDTH:
            self.reset()
            pygame.event.post(events[1])

        if pygame.sprite.spritecollide(self, players_group, False):
            self.vector.x *= -1

    def update(self, players_group, events: tuple | list):
        self.move()
        self.handle_collision(players_group, events)