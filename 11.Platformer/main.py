import pygame
from settings import *
from player import Player
from obstacle import Obstacle


class Platformer:
    def __init__(self):
        # Window
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        obstacle_positions = [
            (300, 550, 180, 25),
            (100, 450, 200, 20),
            (400, 400, 200, 20),
            (200, 300, 200, 20),
            (500, 250, 200, 20),
        ]
        for obs in obstacle_positions:
            o = Obstacle(*obs)
            self.all_sprites.add(o)
            self.obstacle_sprites.add(o)

        # Game Loop
        self.running = True
        self.clock = pygame.time.Clock()

    def update(self):
        self.display.fill(BLACK)

        self.player.update(self.obstacle_sprites)
        self.all_sprites.draw(self.display)

        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            self.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    platformer = Platformer()
    platformer.run()
