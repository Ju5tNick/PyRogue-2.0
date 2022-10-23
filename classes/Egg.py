import pygame

from random import randrange
from classes.Slime import Slime
from classes.ExpSlime import ExpSlime
from helpers.images import OTHER_OBJECTS
from helpers.config import TILES_COUNT_X, TILES_COUNT_Y, TILE_WIDTH, TILE_HEIGHT


class Egg(pygame.sprite.Sprite):
	size = [20, 20]

	def __init__(self, egg_type, coords, game_params):
		super().__init__(pygame.sprite.Group())

		if egg_type == "regular" :
			self.image = OTHER_OBJECTS["egg"]
		elif egg_type == "exp":
			self.image = OTHER_OBJECTS["exp_egg"]

		self.rect = pygame.Rect(coords[0], coords[1], self.size[0], self.size[1])
		self.mask = pygame.mask.from_surface(self.image)
		self.speed = 20
		self.up_speed = 12
		self.current_health = self.health = 200
		self.self_group = game_params["egg_group"]
		self.game_params = game_params
		self.egg_type = egg_type

		self.is_fall = False
		self.hero_coords = []

	def move(self, *qwargs):
		if self.rect.y > 0 and not self.is_fall:
			self.rect = self.rect.move(0, -self.up_speed)
			if self.rect.y < 0:
				self.rect = self.rect.move(0, -self.up_speed)
				self.is_fall = True 
		else:
			move = [self.speed, 0, -self.speed]

			if self.hero_coords == []:
				self.hero_coords = self.game_params["hero"].get_coords()

			diff_y, diff_x = abs(self.hero_coords[0] - self.rect.x), abs(self.hero_coords[1] - self.rect.y)
			del_x, del_y = 0, 0

			if abs(self.hero_coords[0]) - abs(self.rect.x) != 0:
				for elem in move:
					if abs(self.hero_coords[0] - (self.rect.x + elem)) < diff_y:
						del_y = elem

			if abs(self.hero_coords[1]) - abs(self.rect.y) != 0:
				for elem in move:
					if abs(self.hero_coords[1] - (self.rect.y + elem)) < diff_x:
						del_x = elem

			self.rect = self.rect.move(del_y, del_x)
		
			if self.rect == self.rect.move(del_y, del_x):

				if pygame.sprite.spritecollideany(self, self.game_params["hero_group"]):
					self.game_params["hero"].get_damage(20, self.game_params["game"])

				if self.egg_type == "regular":
					minion = Slime("name", "regular", 10, 350, 2, randrange(1, 11), 
						randrange(10, 21), self.game_params, coords=[self.rect.x, self.rect.y])

					self.self_group.add(minion)
					minion.angry = True

				elif self.egg_type == "exp":
					minion = ExpSlime("name", "explosion", 40, 150, 10, randrange(15, 26), 
						randrange(20, 31), self.game_params, coords=[self.rect.x, self.rect.y])

					self.self_group.add(minion)
					minion.angry = True

				self.die()

	def get_damage(self, damage):
		pass

	def die(self):
		self.kill()

	