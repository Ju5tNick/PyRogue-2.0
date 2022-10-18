import pygame

from classes.Sound import Sound
from classes.Weapon import Weapon
from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_Y, TILES_COUNT_X
from helpers.images import HERO_SETS
from helpers.sounds import SOUNDS


class MainHero(pygame.sprite.Sprite):

    hero_sets = HERO_SETS
    image = HERO_SETS["image"]
    cur_frame = 0
    speed = 4

    def __init__(self, coords, name, hp, money=0):
        super().__init__(pygame.sprite.Group())
        self.set_speed()
        self.coords, self.hp, self.name = coords, hp, name
        self.size = [19, 31]
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], self.size[0], self.size[1]), 0
        self.balance, self.xp_progress = money, 1
        self.required_xp, self.level, self.max_hp, self.heal_counter, self.range = 10, 1, hp, 0, 100

        self.weapon = Weapon(10, [20, 10], 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(coords[0], coords[1])
        self.stamina = self.current_stamina = 200
        

    def move(self, chunk, direction, stop=False):
        direct = self.moves[direction].copy()

        if (
                5 <= self.rect.x <= TILES_COUNT_X * TILE_WIDTH - 5 and 5 <= self.rect.y <= TILES_COUNT_Y * TILE_HEIGHT - 5
                and 5 <= self.rect.x + 21 <= TILES_COUNT_X * TILE_WIDTH - 5 and
                5 <= self.rect.y + 24 <= TILES_COUNT_Y * TILE_HEIGHT - 5
        ):

            if (
                    chunk[self.rect.y // TILE_HEIGHT][self.rect.x // TILE_WIDTH] in range(6, 9) or
                    chunk[(self.rect.y + self.size[1]) // TILE_HEIGHT][(self.rect.x + self.size[0]) // TILE_WIDTH] in range(6, 9)
            ):
                self.speed = 2
            else:
                self.speed = 4

            self.set_speed()

            if (
                    chunk[self.rect.y // TILE_HEIGHT][self.rect.x // TILE_WIDTH] in range(6, 9) or
                    chunk[(self.rect.y + self.size[1]) // TILE_HEIGHT][(self.rect.x + self.size[0]) // TILE_WIDTH] in range(6, 9)
            ):
                self.speed = 2
            else:
                self.speed = 4

            self.set_speed()

        self.rect = self.rect.move(*direct)

        if stop:
            self.image = HERO_SETS["still"][direction]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.update(direction)

    def set_speed(self):
        self.moves = {"up": [0, -self.speed], "down": [0, self.speed], "left": [-self.speed, 0], "right": [self.speed, 0]}

    def get_hp(self):
        return self.hp

    def get_range(self):
        return self.range

    def get_max_hp(self):
        return self.max_hp

    def get_damage(self, damage, game):
        Sound.play(SOUNDS["HERO"]["hit"])
        self.hp -= damage
        if self.hp <= 0:
            Sound.play(SOUNDS["HERO"]["death"])
            game.game_over(game)

    def add_hp(self, hp):
        self.max_hp += hp

    def buy(self, price):
        if self.balance - price >= 0:
            self.balance -= price

    def check_water(self, tile):
        return pygame.sprite.spritecollideany(self, tile)

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

    def get_weapon(self):
        return self.weapon

    def get_balance(self):
        return self.balance

    def get_ex(self):
        return self.xp_progress, self.required_xp, self.level

    def attack(self, enemy):
        enemy.get_damage(self.weapon.get_damage())

    def check_level(self):
        while self.xp_progress >= self.required_xp:
            self.level += 1
            self.xp_progress -= self.required_xp
            self.required_xp = round(self.required_xp * 1.8)
        self.walk_on_water = True if self.level >= 15 else False

    def check(self, mouse_coords):
        if (abs(self.rect.x - mouse_coords[0]) ** 2 + abs(
                self.rect.y - mouse_coords[1]) ** 2) ** 0.5 <= self.range + 15:
            return True
        return False

    def add_damage(self, value):
        self.weapon.add_damage(value)

    def get_stamina(self):
        return (self.stamina, self.current_stamina)

    def add_stamina(self, value):
        self.stamina += value

    def pay(self, value):
        self.balance += value

    def running(self, flag):
        self.speed = self.speed * 2 if flag and self.current_stamina >= 20 else self.speed

        self.set_speed()

        if flag and self.current_stamina > 5:
            self.current_stamina -= 5
        elif self.current_stamina < self.stamina:
            self.current_stamina += 1