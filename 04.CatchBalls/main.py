import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 1050, 750
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
WHITE = (255, 255, 255)
ORANGE = (255, 175, 0)
SPEED = 8
FPS = 60
BALL_AMOUNT = 1
BALL_RADIUS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Balls")

background = pygame.transform.scale(pygame.image.load(os.path.join("bg.png")), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 40)
lives = 5
GAME_OVER = pygame.USEREVENT + 1
score = 0



def handle_movement(paddle):
    keys_pressed = pygame.key.get_pressed()
    # if keys_pressed[pygame.K_UP] and paddle.y - SPEED > 0:  # UP
    #     paddle.y -= SPEED
    # if keys_pressed[pygame.K_DOWN] and paddle.y + SPEED < HEIGHT:  # DOWN
    #     paddle.y += SPEED
    if keys_pressed[pygame.K_LEFT] and paddle.x - SPEED > 0:  # LEFT
        paddle.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and paddle.x + SPEED + paddle.width < WIDTH:  # RIGHT
        paddle.x += SPEED


def generate_balls(balls_list):
    for i in range(BALL_AMOUNT):
        pos = pygame.Vector2(random.randint(0, WIDTH - BALL_RADIUS // 2), 0)
        speed = pygame.Vector2(random.randint(3, 6), random.randint(3, 6))
        color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        balls_list.append((pos, speed, color))


def check_collision(ball_pos, paddle):
    closest_x = max(paddle.left, min(ball_pos.x, paddle.right))
    closest_y = max(paddle.top, min(ball_pos.y, paddle.bottom))

    distance = pygame.Vector2(closest_x, closest_y).distance_to(ball_pos)
    return distance <= BALL_RADIUS


def handle_hit():
    global lives
    if lives <= 0:
        pygame.event.post(pygame.event.Event(GAME_OVER))
    else:
        lives -= 1


def handle_balls(balls_list: list[tuple[pygame.Vector2, pygame.Vector2, tuple]], paddle: pygame.Rect):
    global score
    for pos, speed, color in balls_list[:]:
        pos += speed

        if pos.x + BALL_RADIUS >= WIDTH:  # RIGHT
            speed.x *= -1
        if pos.x <= 0:  # LEFT
            speed.x *= -1
        if check_collision(pos, paddle):
            score += 1
            balls_list.remove((pos, speed, color))
        if pos.y >= HEIGHT:
            handle_hit()
            balls_list.remove((pos, speed, color))



def draw(paddle, balls_list):
    screen.blit(background, (0, 0))
    for pos, speed, color in balls_list:
        pygame.draw.circle(screen, color, pos, BALL_RADIUS)
    lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.display.update()



def main():
    running = True
    clock = pygame.time.Clock()
    paddle = pygame.Rect(WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    needed_time = 2000
    elapsed = 0
    balls_list = []

    while running:
        dt = clock.tick(FPS)
        elapsed += dt
        if elapsed > needed_time:
            generate_balls(balls_list)
            elapsed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == GAME_OVER:
                print("GAME OVER!")
                text = FONT.render(f"You lost :( Score: {score}.", True, WHITE)
                screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height()))
                pygame.display.update()
                pygame.time.delay(4000)


        handle_movement(paddle)

        handle_balls(balls_list, paddle)
        draw(paddle, balls_list)
    pygame.quit()


if __name__ == '__main__':
    main()
