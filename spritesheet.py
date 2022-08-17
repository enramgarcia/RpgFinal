import pygame


class SpriteSheet:
    background = (0, 255, 247)

    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, flip=False):
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(self.background)
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.flip(image, flip, False)
        image.set_colorkey(self.background)
        return image
