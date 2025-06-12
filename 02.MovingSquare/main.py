import pygame

pygame.init()

WIDTH, HEIGHT = 1100, 700
RECT_SIZE = 50
GREY = (60, 60, 60)
SQUARE_COLOR = (40, 120, 130)
SPEED = 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")


def draw(square):
    screen.fill(GREY)
    pygame.draw.rect(screen, SQUARE_COLOR, square, border_radius=20)
    pygame.display.update()



def main():
    running = True
    clock = pygame.time.Clock()
    square = pygame.Rect(WIDTH / 2 - RECT_SIZE / 2, HEIGHT - 2 * RECT_SIZE, RECT_SIZE, RECT_SIZE)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and square.y - SPEED > 0:  # UP
            square.y -= SPEED
        if keys_pressed[pygame.K_DOWN] and square.y + SPEED + RECT_SIZE < HEIGHT:  # DOWN
            square.y += SPEED
        if keys_pressed[pygame.K_RIGHT] and square.x + SPEED + RECT_SIZE < WIDTH:  # RIGHT
            square.x += SPEED
        if keys_pressed[pygame.K_LEFT] and square.x - SPEED > 0:  # LEFT
            square.x -= SPEED


        draw(square)
    pygame.quit()


if __name__ == "__main__":
    main()

