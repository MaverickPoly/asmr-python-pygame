import pygame
from settings import *
from shape import Shape
import random
import time


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shape clicker")

        self.main_font = pygame.font.SysFont("comicsans", 40)

        self.shapes = []
        self.running = True
        self.clock = pygame.time.Clock()
        self.required_time = 800
        self.elapsed_time = 0
        self.score = 0
        self.start_time = time.time()

    def generate_shape(self):
        width = random.randint(40, 70)
        height = random.randint(40, 70)
        x_pos = random.randint(20, WIDTH - width - 20)
        y_pos = random.randint(20, HEIGHT - height - 20)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)
        new_shape = Shape(x_pos, y_pos, color, width, height)
        self.shapes.append(new_shape)

    def handle_hit(self, shape):
        self.shapes.remove(shape)
        self.score += 1

    def handle_collision(self):
        clicked_pos = pygame.mouse.get_pos()
        for shape in self.shapes:
            if shape.rect.collidepoint(clicked_pos):
                self.handle_hit(shape)
                break


    def draw_text(self):
        score_text = self.main_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        elapsed_time = int(time.time() - self.start_time)
        time_text = self.main_font.render(f"Time: {elapsed_time}", True, WHITE)
        self.screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    def handle_update_shapes(self):
        for shape in self.shapes:
            shape.draw(self.screen)

        for shape in self.shapes[:]:
            if time.time() - shape.created_time > LIVE_TIME:
                self.shapes.remove(shape)

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.handle_update_shapes()

        self.draw_text()

        pygame.display.update()

    def run(self):
        while self.running:
            self.elapsed_time += self.clock.tick(FPS)
            if self.elapsed_time > self.required_time:
                self.generate_shape()
                self.elapsed_time = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_collision()

            self.draw()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
