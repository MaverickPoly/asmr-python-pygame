import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 800
FPS = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple paint")
FONT = pygame.font.SysFont("lucidaconsole", 40)

colors = ["red", "black", "green", "orange", "yellow", "purple", "pink", "brown", "blue", "cyan", "grey"]
color_index = 0
radius = 10

print(pygame.font.get_fonts())


def draw():
    color_text = FONT.render(f"Color: {colors[color_index].title()}", True, (0, 0, 0))
    thickness_text = FONT.render(f"Thickness: {radius}", True, (0, 0, 0))
    utils_rect = pygame.Rect(0, 0, WIDTH, color_text.get_height() + 10)
    pygame.draw.rect(screen, (255, 255, 255), utils_rect)
    screen.blit(color_text, (10, 10))
    screen.blit(thickness_text, (WIDTH - thickness_text.get_width() - 10, 10))
    pygame.display.flip()


def main():
    global color_index, radius
    running = True
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    color_index = (color_index + 1) % len(colors)
                if event.key == pygame.K_RIGHT:
                    radius += 1
                if event.key == pygame.K_LEFT:
                    radius -= 1

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            coord = pygame.mouse.get_pos()
            pygame.draw.circle(screen, colors[color_index], coord, radius)
        draw()

    pygame.quit()


if __name__ == "__main__":
    main()
