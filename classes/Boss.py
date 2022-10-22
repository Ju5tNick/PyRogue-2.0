import pygame

from random import choice
from itertools import cycle
from classes.Enemy import EnemyVision
from helpers.images import BOSS_SETS


class Boss(pygame.sprite.Sprite):
	image = BOSS_SETS["image"]
	required_counter = 4
	iter_counter = 0
	frames = []
	speed = 3

	def __init__(self, coords):
		super().__init__(pygame.sprite.Group())
		self.rect = pygame.Rect(coords[0], coords[1], 64, 64)
		self.mask = pygame.mask.from_surface(self.image)
		self.vision = EnemyVision(200, (self.rect.x, self.rect.y), self, "boss")

		self.die_flag = False
		self.attack = False
		self.angry = False
		self.is_changed = False
		self.spawn = False
		self.frames = BOSS_SETS["idle"]
		self.can_move = True
		self.frame_counter = cycle(range(self.required_counter))

		self.health = self.current_health = 500

	def move(self, hero, hero_group):
		if self.vision.check(hero_group):
			self.angry = True

		if self.angry and self.can_move:
			move = [self.speed, 0, -self.speed]

			hero_coords = hero.get_coords()
			diff_y, diff_x = abs(hero_coords[0] - self.rect.x), abs(hero_coords[1] - self.rect.y)
			del_x, del_y = 0, 0

			if abs(hero_coords[0]) - abs(self.rect.x) != 100:
				for elem in move:
					if abs(hero_coords[0] - (self.rect.x + elem)) < diff_y:
						del_y = elem

			if abs(hero_coords[1]) - abs(self.rect.y) != 100:
				for elem in move:
					if abs(hero_coords[1] - (self.rect.y + elem)) < diff_x:
						del_x = elem

			self.vision.move(del_y, del_x)
			self.rect = self.rect.move(del_y, del_x)

			if abs(hero.get_coords()[0] - self.rect.x) <= 100 and abs(
					hero.get_coords()[1] - self.rect.y) <= 100 and not self.die_flag and self.angry and not self.attack and not self.spawn:
				if choice([False, False, False, True]):
					self.attack = True
					self.frame_counter = cycle(range(len(BOSS_SETS["attack"]) + 1))
				else:
					self.spawn = True
					self.frame_counter = cycle(range(len(BOSS_SETS["spawn_minion"]) + 1))

		self.update()

	def update(self):
		if self.iter_counter == self.required_counter:
			ind = int(next(self.frame_counter))

			if self.die_flag:
				self.frames = BOSS_SETS["die"]
				self.can_move = False
				self.attack = False
				self.image = self.frames[ind]

				if self.frames[ind] == self.frames[-1]:
					self.vision.kill()
					self.drop_crown()
					self.kill()

			if self.attack:
				self.frames = BOSS_SETS["attack"]
				self.can_move = False
				self.image = self.frames[ind]

				if self.frames[ind] == self.frames[-1]:
					self.frames = BOSS_SETS["idle"]
					self.required_counter = 4
					self.frame_counter = cycle(range(self.required_counter))
					ind = int(next(self.frame_counter))
					self.can_move, self.attack = True, False

			elif self.spawn:
				self.frames = BOSS_SETS["spawn_minion"]
				self.can_move = False
				self.image = self.frames[ind]

				if self.frames[ind] == self.frames[-1]:
					self.frames = BOSS_SETS["idle"]
					self.required_counter = 4
					self.frame_counter = cycle(range(self.required_counter))
					ind = int(next(self.frame_counter))
					self.can_move, self.spawn = True, False

			else:
				self.image = self.frames[ind]

			self.iter_counter = 0

		self.iter_counter += 1

	def draw_hp_bar(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), (10, 470, 980, 25))
		pygame.draw.rect(screen, (70, 117, 93), (11, 471, (self.current_health / self.health) * 980 - 2, 23))
		screen.blit(
            pygame.font.Font(None, 21).render("boss", True, (255, 255, 255)),
            (430, 475))

	def drop_crown(self):
		pass

	def get_damage(self, damage):
		if self.current_health > 0:
			self.current_health -= damage
		if self.current_health <= 0:
			self.die_flag = True
			self.frame_counter = cycle(range(len(BOSS_SETS["die"])))
		