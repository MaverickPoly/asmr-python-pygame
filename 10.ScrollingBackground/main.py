from PIL import Image
import pygame


img = Image.open("image.png")

WIDTH, HEIGHT = img.width, img.height
FPS = 60
SPEED = 2

# Window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Background")

image = pygame.image.load("image.png")
rect1 = image.get_rect(topleft=(0, 0))
rect2 = image.get_rect(topleft=(WIDTH, 0))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    screen.fill("black")

    screen.blit(image, rect1)
    screen.blit(image, rect2)

    rect1.x -= SPEED
    rect2.x -= SPEED

    if rect1.right <= 0:
        rect1.left = WIDTH
    if rect2.right <= 0:
        rect2.left = WIDTH
    

    pygame.display.update()
    clock.tick(FPS)
