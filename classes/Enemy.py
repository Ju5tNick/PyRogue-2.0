from random import randrange

import pygame

from helpers.images import SLIME_SETS


class EnemyVision(pygame.sprite.Sprite):

    def __init__(self, range, coords, enemy):
        super().__init__(pygame.sprite.Group())
        self.host, self.range = enemy, range
        self.image = pygame.Surface((3 * self.range, 3 * self.range), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        self.rect = pygame.Rect(coords[0] - self.range + 10.5, coords[1] - self.range + 12, 1.85 * self.range, 1.85 * self.range)
        self.is_noticed = False

    def update(self, screen):
        pygame.draw.rect(self.image, (0, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 9, self.range - 15, (self.host.get_health() / self.host.get_max_health() * 22 - 2), 3))

    def move(self, del_x, del_y):
        self.rect = self.rect.move(del_x, del_y)

    def check(self, mainhero):
        return pygame.sprite.spritecollideany(self, mainhero)

    def set_flag(self):
        self.is_noticed = True


class EnemyClot(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(pygame.sprite.Group())
        self.image = SLIME_SETS["clot"]
        self.rect = pygame.Rect(coords[0], coords[1], 10, 10)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = []
        self.speed, self.damage = 8, 10
        self.counter = 0

    def move(self, hero, mainhero, weapons, game, iterations=1):
        if pygame.sprite.spritecollide(self, weapons, False):
            self.kill()

        if self.counter <= iterations:
            move = [self.speed * 2, 0, -self.speed * 2]
            diff_y, diff_x = abs(hero.get_coords()[0] - self.rect.x), abs(hero.get_coords()[1] - self.rect.y)
            del_x, del_y = 0, 0

            if abs(hero.get_coords()[0]) - abs(self.rect.x) != 1:
                for elem in move:
                    if abs(hero.get_coords()[0] - (self.rect.x + elem)) < diff_y:
                        del_y, flag = elem, False

            if abs(hero.get_coords()[1]) - abs(self.rect.y) != 1:
                for elem in move:
                    if abs(hero.get_coords()[1] - (self.rect.y + elem)) < diff_x:
                        del_x, flag = elem, False

            y = del_y if del_y == 0 else diff_y / del_y
            x = del_x if del_x == 0 else diff_x / del_x

            self.direction = [y, x]
            self.counter += 1

        self.rect = self.rect.move(*self.direction)

        if pygame.sprite.spritecollide(self, mainhero, False):
            hero.get_damage(self.damage, game)
            self.kill()
