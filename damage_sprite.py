import pygame.sprite


class DamageSprite(pygame.sprite.Sprite):

    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.get_init()
        self.image = pygame.font.SysFont('Times New Roman', 23).render(f'{damage}', True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1

        if self.counter > 30:
            self.kill()
