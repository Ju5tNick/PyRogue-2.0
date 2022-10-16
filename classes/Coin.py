import pygame

from random import randrange
from helpers.images import COINS


class Coin(pygame.sprite.Sprite):

    def __init__(self, coords, denomination):
        super().__init__(pygame.sprite.Group())
        self.rect = pygame.Rect(coords[0] + randrange(-5, 6), coords[1] + randrange(-10, 11), 7, 9)
        self.denomination = denomination
        self.image = COINS[self.denomination]
        self.mask = pygame.mask.from_surface(self.image)

    def drop(self, mainhero):
    	
    	if pygame.sprite.spritecollideany(self, mainhero):
    		for hero in mainhero:
    			hero.pay(self.denomination)
    		self.kill()
        