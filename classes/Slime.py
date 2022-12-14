import pygame

from random import randrange, choice

from classes.Enemy import EnemyVision, EnemyClot
from classes.Coin import Coin
from classes.Sound import Sound
from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_Y, TILES_COUNT_X
from helpers.sounds import SOUNDS
from helpers.images import SLIME_SETS, EXP_SLIME_SETS


class Slime(pygame.sprite.Sprite):
    
    def __init__(self, name, sltype, base_damage, base_health, base_speed, gold_drops, xp_drops, game_params, coords=[]):
        super().__init__(pygame.sprite.Group())

        if sltype == "regular":
            self.slime_sets = SLIME_SETS
            self.image = SLIME_SETS["image"]
        elif sltype == "explosion":
            self.slime_sets = EXP_SLIME_SETS
            self.image = EXP_SLIME_SETS["image"]

        self.game = game_params

        self.name, self.damage, self.health, self.speed = name, base_damage, base_health, base_speed
        self.die_flag, self.max_health = False, base_health

        if coords == []:
            self.rect = pygame.Rect(
                *[randrange(100, TILES_COUNT_X * TILE_WIDTH - 100), randrange(50, TILES_COUNT_Y * TILE_HEIGHT - 100)], 21, 24)

            while not pygame.sprite.spritecollideany(self, self.game["available_tile"]):
                self.rect = pygame.Rect(
                    *[randrange(100, TILES_COUNT_X * TILE_WIDTH - 100), randrange(100, TILES_COUNT_Y * TILE_HEIGHT - 100)], 21,
                    24)
        else:
            self.rect = pygame.Rect(*coords, 21, 24)

        self.get_angry, self.attack = False, False
        self.animation_counter, self.required_quantity = 0, 5

        self.cur_frame, self.frames = 0, []

        self.vision = EnemyVision(100, (self.rect.x, self.rect.y), self, "slime")
        self.game["enemy_visions"].add(self.vision)
        self.gold_drops, self.get_angry, self.angry = gold_drops, False, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True
        self.coins = []
        self.coords = [self.rect.x, self.rect.y]

    def move(self, *qwargs):
        flag = True
        hero_coords = self.game["hero"].get_coords()
        if self.frames == self.slime_sets["die_animation"]:
            self.can_move = False

        if self.vision.check(self.game["hero_group"]) and not self.angry:
            self.vision.set_flag()
            self.get_angry = True

        if self.angry:
            if self.can_move:
                move = [self.speed, 0, -self.speed]

                diff_y, diff_x = abs(hero_coords[0] - self.rect.x), abs(hero_coords[1] - self.rect.y)
                del_x, del_y = 0, 0

                if abs(hero_coords[0]) - abs(self.rect.x) != 20:
                    for elem in move:
                        if abs(hero_coords[0] - (self.rect.x + elem)) < diff_y:
                            del_y, flag = elem, False

                if abs(hero_coords[1]) - abs(self.rect.y) != 20:
                    for elem in move:
                        if abs(hero_coords[1] - (self.rect.y + elem)) < diff_x:
                            del_x, flag = elem, False

                self.vision.move(del_y, del_x)
                self.rect = self.rect.move(del_y, del_x)

            if abs(self.game["hero"].get_coords()[0] - self.rect.x) <= 200 and abs(
                    self.game["hero"].get_coords()[1] - self.rect.y) <= 200 and not self.die_flag and self.angry:
                self.attack = True

            if abs(self.game["hero"].get_coords()[0] - self.rect.x) >= 220 and abs(
                    self.game["hero"].get_coords()[1] - self.rect.y) >= 220 and not self.die_flag and self.angry:
                self.angry = self.get_angry = False
                
        else:
            
            if self.flag == 1 and not self.angry and not self.get_angry and self.direction != [0, 0] and self.can_move:
                flag = False
                if self.rect.x + 1 >= TILES_COUNT_X * TILE_WIDTH - 50 or \
                        self.game["chunk"][int(self.rect.y / TILE_HEIGHT)][
                            int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[0] = -1
                elif self.rect.x - 1 <= 50 or self.game["chunk"][int(self.rect.y / TILE_HEIGHT)][
                    int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[0] = 1
                if self.rect.y + 1 >= TILES_COUNT_Y * TILE_HEIGHT - 50 or \
                        self.game["chunk"][int((self.rect.y + 1) / TILE_HEIGHT)][
                            int(self.rect.x / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1
                elif self.rect.y - 1 <= 50 or self.game["chunk"][int((self.rect.y - 1) / TILE_HEIGHT)][
                    int(self.rect.x / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1

                self.rect = self.rect.move(self.direction[0], self.direction[1])
                self.vision.move(self.direction[0], self.direction[1])

        self.update(stop=flag)
        self.coords = [self.rect.x, self.rect.y] 

    def update(self, stop=False):
        if self.animation_counter == self.required_quantity:
            if not self.die_flag:
                
                if self.get_angry:
                    self.frames, self.can_move, self.required_quantity = self.slime_sets["gets_angry"], False, 7

                    if self.cur_frame == 3:
                        self.angry, self.get_angry, self.required_quantity = True, False, 5

                elif self.angry and not self.get_angry:
                    self.frames, self.speed, self.can_move = self.slime_sets["angry_move"], 5.9, True
                    self.get_angry = False

                else:
                    self.frames = self.slime_sets["still"] if stop else self.slime_sets["move"]

                if self.attack and not self.get_angry:
                    for _ in range(randrange(1, 4)):
                        self.frames, self.can_move, self.required_quantity = self.slime_sets["attack_animation"], False, 3

                        if self.cur_frame == 6:
                            self.clot = EnemyClot((self.rect.x, self.rect.y))                    
                            self.game["clots"].add(self.clot)
                            self.attack, self.can_move = False, True

            else:
                if self.image == self.slime_sets["die_animation"][-1]:
                    self.kill()
                self.frames = self.slime_sets["die_animation"]

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0
            if self.health <= self.max_health:
                self.health += 1

        self.animation_counter += 1

    def set_flag(self):
        self.direction = [choice([1, 0, -1]), choice([1, 0, -1])]
        self.flag = -self.flag

    def get_damage(self, damage):
        if not self.die_flag:
            Sound.play(SOUNDS["ENEMY"]["hit"])
        self.health -= damage
        if not self.angry:
            self.get_angry = True
        if self.health <= 0 and not self.die_flag:
            self.die()

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_coins(self):
        return self.coins

    def die(self):
        if self.health <= 0:

            for _ in range(self.gold_drops // 10):
                self.coins.append(Coin(self.coords, 10))

            for _ in range((self.gold_drops % 10) // 5):
                self.coins.append(Coin(self.coords, 5))

            for _ in range((self.gold_drops % 10) % 5):
                self.coins.append(Coin(self.coords, 1))

            Sound.play(SOUNDS["ENEMY"]["death"])

            self.game["hero"].xp_progress += self.xp_drops
            self.game["hero"].check_level()

            self.vision.kill()
            self.cur_frame, self.die_flag = 0, True

    def get_stats(self):
        return self.name, self.damage, self.health, self.speed, self.range

    def is_angry(self):
        return self.angry
