from random import choice

import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, image, coords, size, can_move, effect="", info="", cost=0, ef_value=0):
        super().__init__(pygame.sprite.Group())
        self.image, self.coords, self.size, self.info = image, coords, size, info
        self.cost, self.effect = cost, effect
        self.can_move, self.counter = can_move, choice([1, -1])
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.ef_value = ef_value

    def move(self):
        if self.can_move:
            if self.counter == 1:
                self.rect = self.rect.move(0, 2)
            else:
                self.rect = self.rect.move(0, -2)
            self.counter = self.counter * (-1)

    def check(self, event_coords):
        if (
                self.coords[0] <= event_coords[0] <= self.coords[0] + self.size[0] and
                self.coords[1] <= event_coords[1] <= self.coords[1] + self.size[1]
        ):
            return True
        return False

    def get_info(self):
        return self.info

    def get_cost(self):
        return self.cost

    def get_effect(self):
        return self.effect

    def get_ef_value(self):
        return self.ef_value
