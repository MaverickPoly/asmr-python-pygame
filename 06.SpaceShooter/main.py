import os
from player import Player
from utils import *

os.chdir("6.SpaceShooter")


class Game:
    def __init__(self):
        # Initial setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space shooter")

        # assets
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))
        self.barrier = pygame.Rect(WIDTH / 2 - BARRIER_WIDTH / 2, 0, BARRIER_WIDTH, HEIGHT)
        self.left_image = scale_image(pygame.image.load(os.path.join("assets", "ship_yellow.png")), 0.8)
        self.right_image = pygame.transform.rotate(
            scale_image(pygame.image.load(os.path.join("assets", "ship_red.png")), 0.8),
            180)
        self.main_font = pygame.font.SysFont("comicsans", 40)
        self.shoot_sound = pygame.mixer.Sound(os.path.join("assets", "laser.wav"))
        self.shoot_sound.set_volume(0.7)
        self.game_music = pygame.mixer.Sound(os.path.join("assets", "music.wav"))
        self.game_music.play(-1)
        self.hit_music = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))

        # players
        self.player_width = self.left_image.get_width()
        self.player_height = self.left_image.get_height()
        self.left_player = Player(self.left_image, WIDTH / 4 - self.left_image.get_width() / 2, HEIGHT / 2 - self.left_image.get_height() / 2)
        self.right_player = Player(self.right_image, WIDTH * 3 / 4 - self.right_image.get_width() / 2, HEIGHT / 2 - self.right_image.get_height() / 2)
        self.left_health = PLAYER_HEALTH
        self.right_health = PLAYER_HEALTH

        # Game loop setup
        self.running = True
        self.clock = pygame.time.Clock()

    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.left_player.x - SHIP_SPEED > 0:  # LEFT
            self.left_player.x -= SHIP_SPEED
        if (keys_pressed[pygame.K_d] and self.left_player.x + SHIP_SPEED + self.player_width <
                WIDTH / 2 - BARRIER_WIDTH / 2):  # RIGHT
            self.left_player.x += SHIP_SPEED
        if keys_pressed[pygame.K_w] and self.left_player.y - SHIP_SPEED > 0:  # UP
            self.left_player.y -= SHIP_SPEED
        if keys_pressed[pygame.K_s] and self.left_player.y + SHIP_SPEED + self.player_height < HEIGHT:  # DOWN
            self.left_player.y += SHIP_SPEED

        if keys_pressed[pygame.K_LEFT] and self.right_player.x - SHIP_SPEED > WIDTH / 2 + BARRIER_WIDTH / 2:  # LEFT
            self.right_player.x -= SHIP_SPEED
        if keys_pressed[pygame.K_RIGHT] and self.right_player.x + SHIP_SPEED + self.player_width < WIDTH:  # RIGHT
            self.right_player.x += SHIP_SPEED
        if keys_pressed[pygame.K_UP] and self.right_player.y - SHIP_SPEED > 0:  # UP
            self.right_player.y -= SHIP_SPEED
        if keys_pressed[pygame.K_DOWN] and self.right_player.y + SHIP_SPEED + self.player_height < HEIGHT:  # DOWN
            self.right_player.y += SHIP_SPEED

    def display_end_text(self, text):
        msg = self.main_font.render(text, True, WHITE)
        self.screen.blit(msg, (WIDTH / 2 - msg.get_width() / 2, HEIGHT / 2 - msg.get_height()))
        pygame.display.flip()
        pygame.time.delay(4000)
        self.running = False

    def handle_player_hit(self):
        self.hit_music.play()
        if self.left_health == 0:
            self.display_end_text(f"Red player won!")
        if self.right_health == 0:
            self.display_end_text(f"Yellow player won!")

    def handle_bullets(self):
        # Move bullets
        for bullet in self.left_player.bullets:
            bullet.x += BULLET_SPEED

        for bullet in self.right_player.bullets:
            bullet.x -= BULLET_SPEED

        # Removing bullets: Out of screen or hit a player
        for bullet in self.left_player.bullets[:]:
            if bullet.x > WIDTH:
                self.left_player.bullets.remove(bullet)
            if bullet.colliderect(self.right_player.rect):
                self.left_player.bullets.remove(bullet)
                self.right_health -= 1
                self.handle_player_hit()

        for bullet in self.right_player.bullets[:]:
            if bullet.x + BULLET_WIDTH < 0:
                self.right_player.bullets.remove(bullet)
            if bullet.colliderect(self.left_player.rect):
                self.right_player.bullets.remove(bullet)
                self.left_health -= 1
                self.handle_player_hit()

    def draw_text(self):
        left_health = self.main_font.render(f"Health: {self.left_health}", True, WHITE)
        right_health = self.main_font.render(f"Health: {self.right_health}", True, WHITE)
        self.screen.blit(left_health, (10, 10))
        self.screen.blit(right_health, (WIDTH - 10 - right_health.get_width(), 10))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, WHITE, self.barrier)

        self.handle_bullets()
        self.left_player.draw(self.screen)
        self.right_player.draw(self.screen)
        self.draw_text()

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        self.left_player.shoot(self.left_player.x + self.player_width, self.left_player.y + self.left_player.rect.height / 2)
                        self.shoot_sound.play()
                    if event.key == pygame.K_RCTRL:
                        self.right_player.shoot(self.right_player.x - BULLET_WIDTH, self.right_player.y + self.right_player.rect.height / 2)
                        self.shoot_sound.play()

            self.movement()
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
