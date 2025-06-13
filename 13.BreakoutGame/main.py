import pygame
from settings import *
from paddle import Paddle
from brick import Brick
from ball import Ball

import sys


class Game:
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)

        # Assets
        self.font = pygame.font.Font(None, 38)

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()

        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)

        self.ball = Ball()
        self.all_sprites.add(self.ball)

        # Game Loop
        self.running = True
        self.game_over = False
        self.clock = pygame.time.Clock()

        self.lives = 3
        self.score = 0

        # Initializations
        self.create_bricks()

    def create_bricks(self):
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick_y = row * BRICK_HEIGHT + BRICK_OFFSET_TOP
                brick_x = col * BRICK_WIDTH + BRICK_PADDING
                color = COLORS[row % len(COLORS)]
                brick = Brick(brick_x, brick_y, color)
                
                self.bricks.add(brick)
                self.all_sprites.add(brick)

    def reset(self):
        self.game_over = False
        self.lives = 3
        self.score = 0

        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.create_bricks()
        self.paddle = Paddle()
        self.ball = Ball()
        self.all_sprites.add(self.paddle)
        self.all_sprites.add(self.ball)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.paddle.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.paddle.move_right()
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.game_over = False
                        self.reset()
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.paddle.stop()
            


            if not self.game_over:
                self.paddle.update()

                if self.ball.update():
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True
                    else:
                        self.ball.reset()

                if pygame.sprite.collide_rect(self.ball, self.paddle):
                    relative_x = (self.ball.rect.centerx - self.paddle.rect.centerx) / (PADDLE_W / 2)
                    self.ball.speed_x = relative_x * 7
                    self.ball.bounce()

                brick_hit = pygame.sprite.spritecollideany(self.ball, self.bricks)
                if brick_hit:
                    brick_hit.kill()
                    self.ball.bounce()
                    self.score += 10

                    if len(self.bricks) == 0:
                        self.game_over = True
            
            self.window.fill(BLACK)
            self.all_sprites.draw(self.window)

            # Texts
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            self.window.blit(score_text, (10, 10))
            self.window.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

            if self.game_over:
                if self.lives <= 0:
                    game_over_text = self.font.render("Game Over! Press Spacebar to restart!", True, WHITE)
                else:
                    game_over_text = self.font.render("You won! Press Spacebar to restart!", True, WHITE)
                self.window.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
