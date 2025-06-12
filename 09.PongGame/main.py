import pygame
from settings import *
from player import Player
from ball import Ball


class Game:
    def __init__(self):
        # Setup
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        # Game Loop
        self.running = True
        self.clock = pygame.time.Clock()

        # Assets
        self.font = pygame.font.SysFont("comicsans", 32)

        # Events
        self.right_player_add_score = pygame.event.Event(pygame.USEREVENT, attr="right_player_add_score")
        self.left_player_add_score = pygame.event.Event(pygame.USEREVENT, attr="left_player_add_score")

        # Players
        self.left_player = Player(
            (PADDLE_MARGIN, HEIGHT / 2), pygame.K_w, pygame.K_s
        )
        self.right_player = Player(
            (WIDTH - PADDLE_MARGIN, HEIGHT / 2), pygame.K_UP, pygame.K_DOWN
        )
        self.players_group = pygame.sprite.Group(self.left_player, self.right_player)
        self.right_score = 0
        self.left_score = 0

        # Ball
        self.ball = pygame.sprite.GroupSingle(
            Ball((WIDTH / 2, HEIGHT / 2), RED)
        )

        # Decorations
        self.center_line = pygame.Rect(
            WIDTH / 2 - RECT_WIDTH / 2, 0,
            RECT_WIDTH, RECT_HEIGHT
        )

    def draw_text(self):
        right_score_text = self.font.render(f"Score {self.right_score}", True, WHITE)
        left_score_text = self.font.render(f"Score {self.left_score}", True, WHITE)

        self.display.blit(left_score_text, (0, 0))
        self.display.blit(right_score_text, (WIDTH - right_score_text.get_width(), 0))

    def draw(self):
        self.display.fill(BLACK)

        self.draw_text()

        self.players_group.update()
        self.players_group.draw(self.display)

        pygame.draw.rect(self.display, LIGHT_GRAY, self.center_line)

        self.ball.update(self.players_group, (self.right_player_add_score, self.left_player_add_score))
        self.ball.draw(self.display)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event == self.right_player_add_score:
                    self.right_score += 1
                    print("right score")
                if event == self.left_player_add_score:
                    self.left_score += 1
                    print("left score")
            
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
