import pygame
from settings import *
from rocket import Rocket
from enemy import Enemy
from bullet import Bullet

import random


class Game:
    def __init__(self):
        # Display
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)

        # Assets
        self.font = pygame.font.Font(None, 42)
        self.bg_music = pygame.mixer.Sound("assets/bg_music.wav")
        self.bg_music.play(loops=-1)
        self.shoot_music = pygame.mixer.Sound("assets/shoot.wav")
        self.shoot_music.set_volume(0.2)
        self.explosion_music = pygame.mixer.Sound("assets/shipexplosion.wav")
        self.explosion_music.set_volume(0.2)

        # Events
        self.UPDATE_ENEMIES_EVENT = pygame.USEREVENT
        self.ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.UPDATE_ENEMIES_EVENT, ENEMY_UPDATE_TIME)
        pygame.time.set_timer(self.ENEMY_SHOOT_EVENT, ENEMY_SHOOT_EVENT_TIME)

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies: list[Enemy] = pygame.sprite.Group()
        self.bullets: list[Bullet] = pygame.sprite.Group()

        self.rocket = Rocket()
        self.all_sprites.add(self.rocket)

        self.create_enemies()

        self.enemy_speed = ENEMY_SPEED

        # Rocket
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3

        # Game Loop
        self.running = True
        self.game_over = False
        self.clock = pygame.time.Clock()    
    
    def create_enemies(self):
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy_y = row * ENEMY_HEIGHT + ENEMY_OFFSET_TOP
                enemy_x = col * ENEMY_WIDTH + ENEMY_PADDING
                enemy = Enemy(enemy_x, enemy_y)

                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

    def update_enemies(self):
        reached = False
        for enemy in self.enemies:
            enemy.rect.x += self.enemy_speed

            if enemy.rect.right >= WIDTH or enemy.rect.left <= 0:
                reached = True
        
        if reached:
            self.enemy_speed *= -1
            for enemy in self.enemies:
                enemy.rect.y += ENEMY_DROP

    def enemy_shoot(self):
        if len(self.enemies) > 0:
            l = list(self.enemies)
            random_enemy = random.choice(l)
            x, y = random_enemy.rect.centerx, random_enemy.rect.bottom
            bullet = Bullet(x, y, True)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.shoot_music.play()

    def update_rocket(self):
        self.rocket.update() 

        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and ticks - self.last_shoot >= RELOAD_SPEED:
            bullet = Bullet(self.rocket.rect.centerx, self.rocket.rect.top, False)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shoot = ticks
            self.shoot_music.play()

        if len(self.enemies) <= 0:
            self.game_over = True


    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

        for bullet in self.bullets:
            if not bullet.enemy and pygame.sprite.spritecollide(bullet, self.enemies, True):
                bullet.kill()
                self.explosion_music.play()

        if pygame.sprite.spritecollide(self.rocket, self.bullets, True):
            self.lives -= 1
            self.explosion_music.play()

            if self.lives == 0:
                self.game_over = True

    def draw_texts(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.display.blit(lives_text, (10, 10))

    def update(self):
        self.update_rocket()
        self.update_bullets()

        self.draw_texts()
        self.all_sprites.draw(self.display)

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.rocket = Rocket()
        self.all_sprites.add(self.rocket)

        self.create_enemies()
        self.enemy_speed = ENEMY_SPEED
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.game_over = False

    def run(self):
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.UPDATE_ENEMIES_EVENT:
                    self.update_enemies()
                if event.type == self.ENEMY_SHOOT_EVENT:
                    self.enemy_shoot()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset()
            
            self.display.fill(BLACK)

            if not self.game_over:
                self.update()
            else:
                if self.lives <= 0:
                    game_over_text = self.font.render("Game over! Press Spacebar to restart!", True, WHITE)
                else:
                    game_over_text = self.font.render(f"You won! You have {self.lives} lives left. Space to restart!", True, WHITE)
                self.display.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
                    
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
