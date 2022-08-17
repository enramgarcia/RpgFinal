import pygame


class Scenario:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

        ground = pygame.image.load('assets/Background/ground.png').convert_alpha()
        self.ground = pygame.transform.scale(ground, (self.width, 55))

        squirrel = pygame.image.load('assets/Background/ardilla.png').convert_alpha()
        self.squirrel = pygame.transform.scale(squirrel, (30, 30))

        self.trees = []

        for i in range(1, 6):
            tree = pygame.image.load(f"assets/Background/plx-{i}.png").convert_alpha()
            tree = pygame.transform.scale(tree, (self.width, self.height))
            self.trees.append(tree)

    def draw(self):
        for i in range(len(self.trees)):
            self.window.blit(self.trees[i], (0, 0))

        ground_height = self.height - 55
        self.window.blit(self.ground, (0, ground_height))

        #self.window.blit(self.squirrel, (0, ground_height - 30))
