import pygame
import random
import os
import time

from settings import *
from player import Player
from obstacle import Obstacle


class Game:
    def __init__(self):
        # Initialization
        pygame.init()

        # Setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simple Runner Game")

        # Assets
        self.sky = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sky.png")), (WIDTH, HEIGHT))
        self.ground = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ground.png")), (1200, 150))
        self.jump_audio = pygame.mixer.Sound(os.path.join("assets", "audio_jump.mp3"))
        self.music = pygame.mixer.Sound(os.path.join("assets", "music.wav"))
        self.music.play(-1)
        self.main_font = pygame.font.SysFont("comicsans", 40)

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.jump_audio))
        self.player_stand = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "stand.png")))

        # Obstacles
        self.obstacles = pygame.sprite.Group()

        # Game setup
        self.running = True
        self.game_on = True
        self.clock = pygame.time.Clock()
        self.required_time = 3000
        self.elapsed_obstacle_time = 0
        self.start_time = time.time()
        self.end_time = 0

    def draw_text(self):
        score_text = self.main_font.render(f"Score: {int((time.time() - self.start_time) * 10)}", True, GRAY)
        self.screen.blit(score_text, (10, 10))

    def handle_collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, False):
            return True
        return False

    def handle_end_screen(self, event):
        self.screen.fill(LIGHT_BLUE)
        self.screen.blit(self.player_stand, (
            WIDTH / 2 - self.player_stand.get_width() / 2, HEIGHT / 2 - self.player_stand.get_height() / 2))
        end_text = self.main_font.render(f"You Lost!! Score: {int((self.end_time - self.start_time) * 10)}. "
                                         f"Press Space to restart!", True, WHITE)
        self.screen.blit(end_text, (WIDTH / 2 - end_text.get_width() / 2, HEIGHT / 2 + 200))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_on = True
            self.start_time = time.time()
            self.obstacles.empty()
            self.required_time = 3000
        pygame.display.update()

    def draw(self):
        self.screen.blit(self.sky, (0, 0))
        self.screen.blit(self.ground, (0, HEIGHT - GRASS_HEIGHT))

        self.player.update()
        self.player.draw(self.screen)

        self.obstacles.update()
        self.obstacles.draw(self.screen)

        self.draw_text()

        pygame.display.update()

    def run(self):
        while self.running:
            self.elapsed_obstacle_time += self.clock.tick(FPS)
            if self.elapsed_obstacle_time > self.required_time:
                self.obstacles.add(Obstacle(random.choice(["snail", "snail", "fly"])))
                self.required_time = max(self.required_time - 20, 200)
                self.elapsed_obstacle_time = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.game_on:
                    self.handle_end_screen(event)

            self.game_on = not self.handle_collision()

            if self.game_on:
                self.end_time = time.time()
                self.draw()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
