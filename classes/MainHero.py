import pygame

from classes import Weapon
from helpers.config import TILE_WIDTH, TILE_HEIGHT, FIELD_SIZE_X, FIELD_SIZE_Y
from helpers.images import HERO_SETS


class MainHero(pygame.sprite.Sprite):

    walk_on_water = False
    weapon = None
    weapons = []
    hero_sets = HERO_SETS
    image = HERO_SETS["image"]
    cur_frame = 0
    moves = {"up": [0, -4], "down": [0, 4], "left": [-4, 0], "right": [4, 0]}

    def __init__(self, coords, name, hp, money=0):
        super().__init__(pygame.sprite.Group())
        self.coords, self.hp, self.name = coords, hp, name
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], 19, 31), 0
        self.balance, self.xp_progress = money, 1
        self.required_xp, self.level, self.max_hp, self.heal_counter, self.range = 10, 1, hp, 0, 100

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(coords[0], coords[1])

    def move(self, chunk, direction, stop=False):
        direct = self.moves[direction].copy()

        if (
                5 <= self.rect.x <= FIELD_SIZE_X * TILE_WIDTH - 5 and 5 <= self.rect.y <= FIELD_SIZE_Y * TILE_HEIGHT - 5
                and not self.walk_on_water and 5 <= self.rect.x + 21 <= FIELD_SIZE_X * TILE_WIDTH - 5 and
                5 <= self.rect.y + 24 <= FIELD_SIZE_Y * TILE_HEIGHT - 5 and not self.walk_on_water
        ):
            if (
                    chunk[int(self.rect.y / TILE_HEIGHT)][int((self.rect.x + direct[0]) / TILE_WIDTH)] in range(6, 9) or
                    chunk[int(self.rect.y / TILE_HEIGHT)][int((self.rect.x + 21 + direct[0]) / TILE_WIDTH)] in range(6,
                                                                                                                     9)
            ):
                direct[0] = 0
                stop = True
            else:
                direct[0] = direct[0]

            if (chunk[int((self.rect.y + direct[1]) / TILE_HEIGHT)][int(self.rect.x / TILE_WIDTH)] in range(6, 9) or
                    chunk[int((self.rect.y + 24 + direct[1]) / TILE_HEIGHT)][int(self.rect.x / TILE_WIDTH)] in range(6,
                                                                                                                     9)
            ):
                direct[1] = 0
                stop = True
            else:
                direct[1] = direct[1]

        self.rect = self.rect.move(*direct)

        if stop:
            self.image = self.hero_sets["still"][direction]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.update(direction)

    def get_hp(self):
        return self.hp

    def get_range(self):
        return self.range

    def get_max_hp(self):
        return self.max_hp

    def get_damage(self, damage, game):
        game.sound("assets/sounds/mh_hit.mp3")
        self.hp -= damage
        if self.hp <= 0:
            game.sound("assets/sounds/death_mh.mp3")
            game.game_over()

    def add_hp(self, hp):
        self.max_hp += hp

    def buy(self, price):
        if self.balance - price >= 0:
            self.balance -= price

    def check_water(self, available_tile):
        return pygame.sprite.spritecollideany(self, available_tile)

    def update(self, direction):
        if self.animation_counter == 5:
            self.frames = self.hero_sets["move"][direction]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            self.mask = pygame.mask.from_surface(self.image)
        self.animation_counter += 1

    def is_alive(self):
        return True if self.hp > 0 else False

    def heal(self):
        if self.hp <= self.max_hp - 1:
            if self.heal_counter == 5:
                self.hp += 1;
                self.heal_counter = 0
            self.heal_counter += 1

    def set_coords(self, new_x, new_y):
        self.rect.x, self.rect.y = new_x, new_y

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_balance(self):
        return self.balance

    def get_ex(self):
        return self.xp_progress, self.required_xp, self.level

    def add_weapon(self, weapon):
        if type(weapon) is Weapon:
            self.weapons.append(weapon)
            self.weapon = weapon

    def attack(self, enemy):
        enemy.get_damage(self.weapon.get_damage())

    def check_level(self):
        while self.xp_progress >= self.required_xp:
            self.level += 1
            self.xp_progress -= self.required_xp
            self.required_xp = round(self.required_xp * 1.8)
            self.max_hp += 5
        self.walk_on_water = True if self.level >= 15 else False

    def check(self, mouse_coords):
        if (abs(self.rect.x - mouse_coords[0]) ** 2 + abs(
                self.rect.y - mouse_coords[1]) ** 2) ** 0.5 <= self.range + 15:
            return True
        return False
