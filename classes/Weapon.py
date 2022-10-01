import pygame

from helpers.images import WEAPON_SETS


class Weapon(pygame.sprite.Sprite):
    image = WEAPON_SETS["sword"]

    def __init__(self, damage, coords, range):
        super().__init__(pygame.sprite.Group())
        self.weapon_sets = WEAPON_SETS
        self.default_weapon = self.weapon_sets["sword"]
        self.mask, self.range, self.damage = pygame.mask.from_surface(self.image), range, damage
        self.rect, self.crossing = self.image.get_rect(), True

        self.flips = {
            "++": -90, "=+": -135, "-+": -180, "-=": 135, "": -1, "--": 90, "=-": 45, "+-": 0, "+=": -45, "==": -1
        }

    def move(self, x, y, del_x, del_y, hero, enemies):
        global weapon_activated
        if hero.check((x, y)):
            pygame.mouse.set_visible(False)
            weapon_activated = True
            if self.flips[''.join(self.check(del_x, del_y))] != -1:
                self.image = pygame.transform.rotate(self.default_weapon, self.flips[''.join(self.check(del_x, del_y))])
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x, self.rect.y = x, y
            hurt_enemies = pygame.sprite.spritecollide(self, enemies, False)
            if self.crossing:
                for enemy in hurt_enemies:
                    hero.attack(enemy)
            self.crossing = True if not pygame.sprite.spritecollide(self, enemies, False) else False
        else:
            weapon_activated = False
            pygame.mouse.set_visible(True)
            self.rect.x, self.rect.y = hero.get_coords()[0], hero.get_coords()[1]

    def get_range(self):
        return self.range

    def get_damage(self):
        return self.damage

    def add_damage(self, damage):
        self.damage += damage

    def check(self, x, y):
        result = ["", ""]
        result[0] = "+" if x > 0 else "-"
        result[1] = "+" if y > 0 else "-"
        result[0] = "=" if x in range(-3, 4) else result[0]
        result[1] = "=" if y in range(-3, 4) else result[1]
        return result
