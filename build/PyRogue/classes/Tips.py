import pygame

from helpers.config import MAX_TIP_LENGTH

pygame.init()


class Tip(pygame.sprite.Sprite):

	def __init__(self, text):
		super().__init__(pygame.sprite.Group())
		current_width = current_index = 0
		self.tip = [[]]
		self.size = [0, 0]

		for word in text.split():
			message = pygame.font.Font(None, 20).render(word, True, (0, 0, 0))
			if current_width + message.get_width() <= MAX_TIP_LENGTH:
				current_width += message.get_width()
				self.tip[current_index].append(word)
			else:
				current_index += 1
				current_width = 0
				self.tip.append([word])

		self.size[0] = pygame.font.Font(None, 20).render(max([' '.join(string) for string in self.tip], key=len), True, (0, 0, 0)).get_width() + 4
		_list = [string[0][0] for string in self.tip]
		self.size[1] = sum([pygame.font.Font(None, 20).render(elem, True, (0, 0, 0)).get_height() for elem in _list]) + 4
		self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		self.image.fill((252, 215, 142, 180))
		screen.blit(self.image, (5, 5))
		for i, string in enumerate(self.tip):
			string = " ".join(string)
			screen.blit(pygame.font.Font(None, 20).render(string, True, (0, 0, 0)), (7, 7 + i * ((self.size[1]) // len(self.tip))))
