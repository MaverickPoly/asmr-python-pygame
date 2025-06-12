import pygame
from pygame import Vector2
from settings import *


class Snake:
    def __init__(self):
        self.body = [Vector2(10, 11), Vector2(10, 10), Vector2(10, 9)]
        self.direction = Vector2(1, 0)

    def grow(self):
        vector = self.body[-1] - self.direction
        self.body.append(vector)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy[:]

    def update(self):
        self.move()

    def draw(self, display: pygame.Surface):
        for part in self.body:
            dest = part.x * TILE_SIZE, part.y * TILE_SIZE
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surface.fill(SNAKE_COLOR)
            display.blit(surface, dest)
