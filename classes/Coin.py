import pygame

from helpers.images import OTHER_OBJECTS


class Coin(pygame.sprite.Sprite):
    image = OTHER_OBJECTS["coin"]

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.rect = pygame.Rect(20, 20, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)

    def drop(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
