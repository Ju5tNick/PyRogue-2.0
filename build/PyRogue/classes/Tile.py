import pygame

from helpers.config import TILE_WIDTH, TILE_HEIGHT
from helpers.images import load_image


class AvailableTile(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(pygame.sprite.Group())
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGHT


class UnavailableTile(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(pygame.sprite.Group())
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGHT
