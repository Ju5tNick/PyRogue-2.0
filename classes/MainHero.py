import pygame
from pygame.math import Vector2
from itertools import cycle

from classes.Sound import Sound
from classes.Weapon import Weapon
from helpers.config import HERO_RUNNING_SPEED, HERO_BASE_SPEED, ON_CHANGE_TILE
from helpers.images import HERO_SETS
from helpers.sounds import SOUNDS


class MainHero(pygame.sprite.Sprite):

    hero_sets = HERO_SETS
    image = HERO_SETS["image"]
    cur_frame = 0

    def __init__(self, coords, name, hp, money=0):
        super().__init__(pygame.sprite.Group())
        self.coords, self.hp, self.name = coords, hp, name
        self.size = [19, 31]
        self.rect, self.animation_counter = pygame.Rect(coords[0], coords[1], self.size[0], self.size[1]), 0
        self.balance, self.xp_progress = money, 1
        self.required_xp, self.level, self.max_hp, self.heal_counter, self.range = 10, 1, hp, 0, 100
        self.is_running = False
        self.last_tile = "land"

        self.weapon = Weapon(10, [20, 10], 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(coords[0], coords[1])
        self.stamina = self.current_stamina = 200
        self.index = cycle([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        self.pos = Vector2(coords)
        self.vel = Vector2(0, 0)
        self.speed = HERO_BASE_SPEED

        self.with_crown = False

    def move(self, event):
        self.handling(event)

        postfix = "-in-water" if self.last_tile == "water" else ""
        force = event.type == ON_CHANGE_TILE
        if self.get_move():
            if self.get_running():
                Sound.play(SOUNDS["HERO"][f"run{postfix}"], force)
            else:
                Sound.play(SOUNDS["HERO"][f"step{postfix}"], force)
        if not self.get_move():
            Sound.stop("movement")

    def handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.vel.x = self.speed
            elif event.key == pygame.K_a:
                self.vel.x = -self.speed
            elif event.key == pygame.K_w:
                self.vel.y = -self.speed
            elif event.key == pygame.K_s:
                self.vel.y = self.speed

        if self.is_running:
            if self.vel.x > 0:
                self.vel.x = HERO_RUNNING_SPEED
            elif self.vel.x < 0:
                self.vel.x = -HERO_RUNNING_SPEED
            if self.vel.y > 0:
                self.vel.y = HERO_RUNNING_SPEED
            elif self.vel.y < 0:
                self.vel.y = -HERO_RUNNING_SPEED
        else:
            if self.vel.x > 0:
                self.vel.x = HERO_BASE_SPEED
            elif self.vel.x < 0:
                self.vel.x = -HERO_BASE_SPEED
            if self.vel.y > 0:
                self.vel.y = HERO_BASE_SPEED
            elif self.vel.y < 0:
                self.vel.y = -HERO_BASE_SPEED

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.vel.x > 0:
                self.vel.x = 0

            elif event.key == pygame.K_a and self.vel.x < 0:
                self.vel.x = 0

            elif event.key == pygame.K_w and self.vel.y < 0:
                self.vel.y = 0

            elif event.key == pygame.K_s and self.vel.y > 0:
                self.vel.y = 0

    def stop(self):
        self.vel.x = 0
        self.vel.y = 0
        Sound.stop("movement")

    def set_flag(self, flag):
        self.is_running = flag

    def set_last_tile(self, tile):
        self.last_tile = tile

    def animation(self, event):
        ind = int(next(self.index))

        if self.vel.x > 0:
            self.image = self.hero_sets["move"]["right"][ind]
        elif self.vel.x < 0:
            self.image = self.hero_sets["move"]["left"][ind]
        elif self.vel.y < 0:
            self.image = self.hero_sets["move"]["up"][ind]
        elif self.vel.y > 0:
            self.image = self.hero_sets["move"]["down"][ind]

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.image = HERO_SETS["still"]["right"]
            elif event.key == pygame.K_a:
                self.image = HERO_SETS["still"]["left"]
            elif event.key == pygame.K_w:
                self.image = HERO_SETS["still"]["up"]
            elif event.key == pygame.K_s:
                self.image = HERO_SETS["still"]["down"]

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def get_move(self):
        return self.vel.x != 0 or self.vel.y != 0

    def get_running(self):
        return self.is_running

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
            Sound.stop_all_channels()
            game.game_over(game)

    def add_hp(self, hp):
        self.max_hp += hp

    def buy(self, price):
        if self.balance - price >= 0:
            self.balance -= price

    def is_alive(self):
        return True if self.hp > 0 else False

    def heal(self):
        if self.hp <= self.max_hp - 1:
            if self.heal_counter == 5:
                self.hp += 1
                self.heal_counter = 0
            self.heal_counter += 1

        if self.current_stamina < self.stamina:
            self.current_stamina += 1

    def set_coords(self, new_x, new_y):
        self.pos = new_x, new_y
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

    def check(self, mouse_coords):
        if (abs(self.rect.x - mouse_coords[0]) ** 2 + abs(
                self.rect.y - mouse_coords[1]) ** 2) ** 0.5 <= self.range + 15:
            return True
        return False

    def add_damage(self, value):
        self.weapon.add_damage(value)

    def get_stamina(self):
        return self.stamina, self.current_stamina

    def add_stamina(self, value):
        self.stamina += value

    def pay(self, value):
        Sound.play(SOUNDS["HERO"]["pick-coins"])
        self.balance += value

    def get_with_crown(self):
        return self.with_crown
