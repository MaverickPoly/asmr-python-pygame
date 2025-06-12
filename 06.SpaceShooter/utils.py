from settings import *


def scale_image(image: pygame.Surface, scale_factor):
    size = image.get_width() * scale_factor, image.get_height() * scale_factor
    return pygame.transform.scale(image, size)
