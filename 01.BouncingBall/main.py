import pygame
import os
import random

pygame.init()
WIDTH, HEIGHT = 1050, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

hit_music = pygame.mixer.Sound(os.path.join("hit_sound.mp3"))
hit_music.set_volume(10)
background = pygame.transform.scale(pygame.image.load(os.path.join("bg.png")), (WIDTH, HEIGHT))
ball_vectors = [pygame.Vector2(5, 5)]
ball_positions = [pygame.Vector2(WIDTH / 2, HEIGHT / 2)]

colors = [(0, 0, 0)]


def hit():
    for i in range(len(colors)):
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        colors[i] = red, green, blue
    hit_music.play()


def handle_collision():
    for ball_pos, ball_vector in zip(ball_positions, ball_vectors):
        ball_pos += ball_vector
        if ball_pos.x >= WIDTH:
            ball_vector.x *= -1
            hit()
        if ball_pos.x <= 0:
            ball_vector.x *= -1
            hit()
        if ball_pos.y >= HEIGHT:
            ball_vector.y *= -1
            hit()
        if ball_pos.y <= 0:
            ball_vector.y *= -1
            hit()


def draw():
    screen.blit(background, (0, 0))
    for i in range(len(ball_positions)):
        pygame.draw.circle(screen, colors[i], ball_positions[i], 15)
    handle_collision()

    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    running = True
    required_time = 2000
    elapsed = 0
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed += dt
        if elapsed > required_time:
            colors.append((0, 0, 0))
            pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            speed = random.randint(3, 6), random.randint(3, 6)
            ball_positions.append(pygame.Vector2(pos))
            ball_vectors.append(pygame.Vector2(speed))
            elapsed = 0

        draw()
    pygame.quit()


if __name__ == "__main__":
    main()
