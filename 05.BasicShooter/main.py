import os
import random
import time

from shooter import Shooter
from obstacle import *

for i in range(5):
    print(5)
    
def scale_image(image, scale_factor):
    size = (image.get_width() * scale_factor, image.get_height() * scale_factor)
    return pygame.transform.scale(image, size)


class Game:
    def __init__(self):
        # Initial setup
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Basic Shooter")

        # Assets
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))
        self.shooter_image = scale_image(pygame.image.load(os.path.join("assets", "shooter.png")), 0.35)
        self.obstacle_image = scale_image(pygame.image.load(os.path.join("assets", "meteor.png")), 0.6)
        self.main_font = pygame.font.SysFont("comicsans", 40)

        # Music
        self.game_music = pygame.mixer.Sound(os.path.join("assets", "music.wav"))
        self.explosion_music = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
        self.laser_music = pygame.mixer.Sound(os.path.join("assets", "laser.wav"))
        self.game_music.play(-1)

        # Player
        self.shooter = Shooter(self.shooter_image, WIDTH / 2 - self.shooter_image.get_width() / 2, HEIGHT - 50 - self.shooter_image.get_height(), self.screen)

        # Obstacles
        self.obstacle_groups = pygame.sprite.Group()

        # Utils
        self.running = True
        self.clock = pygame.time.Clock()
        self.obstacle_add_increment = 2000
        self.obstacle_count = 0
        self.start_time = time.time()
        self.score = 0
        self.health = 5

    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and self.shooter.rect.y - SHOOTER_SPEED > 0:  # UP
            self.shooter.rect.y -= SHOOTER_SPEED
        if keys_pressed[pygame.K_DOWN] and self.shooter.rect.y + SHOOTER_SPEED + self.shooter.rect.height < HEIGHT:  # DOWN
            self.shooter.rect.y += SHOOTER_SPEED
        if keys_pressed[pygame.K_LEFT] and self.shooter.rect.x - SHOOTER_SPEED > 0:  # LEFT
            self.shooter.rect.x -= SHOOTER_SPEED
        if keys_pressed[pygame.K_RIGHT] and self.shooter.rect.x + SHOOTER_SPEED + self.shooter.rect.width < WIDTH:  # RIGHT
            self.shooter.rect.x += SHOOTER_SPEED

    def handle_collision(self):
        if pygame.sprite.spritecollide(self.shooter, self.obstacle_groups, True):
            self.health -= 1
            self.explosion_music.play()

        check = [False] * len(self.shooter.bullets)
        for i, bullet in enumerate(self.shooter.bullets):
            for obstacle in self.obstacle_groups:
                if bullet.colliderect(obstacle.rect):
                    obstacle.kill()
                    check[i] = True
                    self.explosion_music.play()

        for i in range(len(self.shooter.bullets)):
            if check[i]:
                self.shooter.bullets.pop(i)


    def draw_texts(self):
        if self.health <= 0:
            end_text = self.main_font.render(f"You Lost! Your score: {self.score}", True, WHITE)
            self.screen.blit(end_text, (WIDTH / 2 - end_text.get_width() / 2, HEIGHT / 2 - end_text.get_height() / 2))
            pygame.display.flip()
            pygame.time.delay(4000)
            self.running = False
        else:
            health_text = self.main_font.render(f"Health: {self.health}", True, WHITE)
            self.screen.blit(health_text, (10, 10))

            self.score = int((time.time() - self.start_time) * 10)
            time_text = self.main_font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    def generate_obstacles(self):
        for _ in range(2):
            x_pos = random.randint(30, WIDTH - 30 - self.obstacle_image.get_width())
            y_pos = -random.randint(50, 150)
            speed = random.choice([2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6])
            rotation_amount = random.randint(0, 180)
            obstacle_image = pygame.transform.rotate(self.obstacle_image, rotation_amount)
            new_obstacle = Obstacle(obstacle_image, x_pos, y_pos, speed, self.screen)
            self.obstacle_groups.add(new_obstacle)
        self.obstacle_count = 0
        self.obstacle_add_increment = max(10, self.obstacle_add_increment - 50)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for obstacle in self.obstacle_groups:
            obstacle.draw()
        self.draw_texts()
        self.handle_collision()
        self.shooter.draw()
        pygame.display.update()

    def run(self):
        while self.running:
            self.obstacle_count += self.clock.tick(FPS)
            if self.obstacle_count > self.obstacle_add_increment:
                self.generate_obstacles()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shooter.shoot()
                        self.laser_music.play()
            self.movement()
            self.draw()
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()
