import pygame
from random import randrange, choice, randint
from image_sets import load_image
from image_sets import hero_sets, weapon_sets, enemy_sets, trader_sets, other_objects

all_sprites = pygame.sprite.Group()
X, Y, FIELD_X, FIELD_Y = 40, 20, 5, 5
TILE_WIDTH, TILE_HEIGT = 25, 25


class Tile_can_go(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(all_sprites)
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGT


class Tile_cant_go(pygame.sprite.Sprite):

    def __init__(self, way, x, y):
        super().__init__(all_sprites)
        self.image = load_image(way)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGT


