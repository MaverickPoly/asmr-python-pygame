import pygame
from pygame import Vector2
from settings import *
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        # Window
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.snake = Snake()
        self.score = 0
        self.fruits: list[Fruit] = [Fruit()]

        # Timers
        self.UPDATE_SNAKE_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.UPDATE_SNAKE_EVENT, UPDATE_SNAKE_EVENT_TIME)
        self.SPAWN_FRUIT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_FRUIT_EVENT, UPDATE_FRUIT_EVENT_TIME)

        # Game Loop
        self.running = True
        self.clock = pygame.time.Clock()

    def handle_collision(self):
        # Out of window
        head = self.snake.body[0]
        if head.x < 0 or head.x > TILES_X or head.y < 0 or head.y > TILES_Y:
            self.running = False
        
        # Eat Fruit
        new_fruits = []
        for fruit in self.fruits:
            if head.x == fruit.row and head.y == fruit.col:
                self.snake.grow()
            else:
                new_fruits.append(fruit)
        self.fruits = new_fruits

        # Collide with itself
        for part in self.snake.body[1:]:
            if part == head:
                self.running = False
                break

    def draw_bg(self):
        for row in range(TILES_X):
            for col in range(TILES_Y):
                x = TILE_SIZE * row
                y = TILE_SIZE * col

                count = row + col

                color = LIGHT_GREEN if count % 2 == 0 else DARK_GREEN

                surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surface.fill(color)
                self.display.blit(surface, (x, y))

    def draw_fruits(self):
        for fruit in self.fruits:
            fruit.draw(self.display)

    def draw_snake(self):
        self.snake.update()
        self.handle_collision()
        self.snake.draw(self.display)

    def update(self):       
        self.draw_bg() 
        self.draw_fruits()
        self.draw_snake()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != Vector2(0, 1):
                        self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and self.snake.direction != Vector2(0, -1):
                        self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and self.snake.direction != Vector2(1, 0):
                        self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and self.snake.direction != Vector2(-1, 0):
                        self.snake.direction = Vector2(1, 0)
                if event.type == self.UPDATE_SNAKE_EVENT:
                    self.update()
                if event.type == self.SPAWN_FRUIT_EVENT:
                    self.fruits.append(Fruit())

            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()

