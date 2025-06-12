from settings import *


class Player:
    def __init__(self, image: pygame.Surface, x, y):
        self.image = image
        self.x = x
        self.y = y
        # self.rotation = rotation
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.max_bullets = 3
        self.bullets = []

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self, surface: pygame.Surface):
        self.update()
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(surface, WHITE, bullet)

    def shoot(self, x, y):
        if len(self.bullets) < self.max_bullets:
            new_bullet = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
            self.bullets.append(new_bullet)


