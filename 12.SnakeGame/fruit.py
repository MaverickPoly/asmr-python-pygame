import pygame
from settings import *
import random


class Fruit:
    def __init__(self):
        self.row, self.col = random.randint(0, TILES_X), random.randint(0, TILES_Y)
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surface.fill(FRUIT_COLOR)

    def draw(self, display: pygame.Surface):
        dest = self.row * TILE_SIZE, self.col * TILE_SIZE
        display.blit(self.surface, dest)
