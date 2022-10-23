import pygame

from helpers.images import OTHER_OBJECTS


class Crack(pygame.sprite.Sprite):
	size = [20, 20]
	image = OTHER_OBJECTS["crack"]

	def __init__(self, coords, damage, game_params):
		super().__init__(pygame.sprite.Group())

		self.coords = coords
		self.damage = damage
		self.self_group = game_params["crack_group"]
		self.rect = pygame.Rect(coords[0], coords[1], self.size[0], self.size[1])
		self.mask = pygame.mask.from_surface(self.image)
		self.game_params = game_params
		self.self_group.add(self)

	def update(self):
		if pygame.sprite.spritecollideany(self, self.game_params["hero_group"]):
			self.game_params["hero"].get_damage(10, self.game_params["game"])
			self.kill()