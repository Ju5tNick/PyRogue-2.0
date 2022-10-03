import pygame

from random import randrange, choice

from classes.Enemy import EnemyVision, EnemyClot
from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_Y, TILES_COUNT_X
from helpers.images import SLIME_SETS


class Slime(pygame.sprite.Sprite):
    image = SLIME_SETS["image"]

    def __init__(self, name, base_damage, base_health, base_speed, range, gold_drops, xp_drops, game_params):
        super().__init__(pygame.sprite.Group())

        self.game = game_params

        self.name, self.damage, self.health, self.speed = name, base_damage, base_health, base_speed
        self.range, self.die_flag, self.max_health = range, False, base_health
        self.rect = pygame.Rect(
            *[randrange(50, TILES_COUNT_X * TILE_WIDTH - 50), randrange(50, TILES_COUNT_Y * TILE_HEIGHT - 50)], 21, 24)
        while not pygame.sprite.spritecollideany(self, self.game["available_tile"]):
            self.rect = pygame.Rect(
                *[randrange(50, TILES_COUNT_X * TILE_WIDTH - 50), randrange(50, TILES_COUNT_Y * TILE_HEIGHT - 50)], 21,
                24)

        self.get_angry, self.attack = False, False
        self.animation_counter, self.required_quantity = 0, 5

        self.slime_sets = SLIME_SETS

        self.cur_frame, self.frames = 0, []

        self.vision = EnemyVision(100, (self.rect.x, self.rect.y), self)
        self.game["enemy_visions"].add(self.vision)
        self.gold_drops, self.get_angry, self.angry = gold_drops, False, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True

    def move(self, hero_coords, mainhero):
        flag = True
        if self.frames == self.slime_sets["die_animation"]:
            self.can_move = False
        if self.vision.check(mainhero) or self.angry:
            if self.can_move:
                self.get_angry = True
                move = [self.speed, 0, -self.speed]

                diff_y, diff_x = abs(hero_coords[0] - self.rect.x), abs(hero_coords[1] - self.rect.y)
                del_x, del_y = 0, 0

                if abs(hero_coords[0]) - abs(self.rect.x) != 10:
                    for elem in move:
                        if abs(hero_coords[0] - (self.rect.x + elem)) < diff_y:
                            del_y, flag = elem, False

                if abs(hero_coords[1]) - abs(self.rect.y) != 10:
                    for elem in move:
                        if abs(hero_coords[1] - (self.rect.y + elem)) < diff_x:
                            del_x, flag = elem, False

                self.vision.move(del_y, del_x)
                self.rect = self.rect.move(del_y, del_x)

            if not self.game["hero"].check_water(self.game["available_tile"]):
                self.can_move, self.attack = False, True

            if abs(self.game["hero"].get_coords()[0] - self.rect.x) <= 10 and abs(
                    self.game["hero"].get_coords()[1] - self.rect.y) <= 10 and not self.die_flag:
                self.attack = True
        else:
            self.attack = False

            if self.angry and self.get_angry:
                self.angry, self.get_angry = False, False

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

                if self.game["chunk"][int((self.rect.y - 1) / TILE_HEIGHT)][
                    int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1
                    self.direction[0] = 1
                elif self.game["chunk"][int((self.rect.y + 1) / TILE_HEIGHT)][
                    int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1
                    self.direction[0] = 1
                elif self.game["chunk"][int((self.rect.y - 1) / TILE_HEIGHT)][
                    int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1
                    self.direction[0] = -1
                elif self.game["chunk"][int((self.rect.y + 1) / TILE_HEIGHT)][
                    int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1
                    self.direction[0] = -1

                self.rect = self.rect.move(self.direction[0], self.direction[1])
                self.vision.move(self.direction[0], self.direction[1])

        self.update(stop=flag)

    def update(self, stop=False):
        if self.animation_counter == self.required_quantity:
            if not self.die_flag:
                if self.angry:
                    self.frames, self.speed, self.can_move = self.slime_sets["angry_move"], 5.9, True
                    # self.angry = False if not self.vision.check() else True
                elif self.get_angry:
                    self.frames, self.can_move, self.required_quantity = self.slime_sets["gets_angry"], False, 7
                    if self.cur_frame == 3:
                        self.game["sound"]("assets/sounds/get_angry_e.wav")
                        self.angry, self.get_angry, self.required_quantity = True, False, 5
                else:
                    self.speed = 2
                    self.frames = self.slime_sets["still"] if stop else self.slime_sets["move"]
                if self.attack:
                    self.frames, self.can_move, self.required_quantity = self.slime_sets["attack_animation"], False, 3
                    if self.cur_frame == 6 and not self.game["hero"].check_water(self.game["available_tile"]):
                        self.clot = EnemyClot((self.rect.x, self.rect.y))
                        self.game["clots"].add(self.clot)
                    elif self.cur_frame == 6 and self.game["hero"].check_water(self.game["available_tile"]):
                        self.attack, self.can_move, self.required_quantity = False, True, 5
                        self.clot = EnemyClot((self.rect.x, self.rect.y))
                        self.game["clots"].add(self.clot)
                elif not self.attack and not self.angry and not self.get_angry:
                    self.speed, self.can_move, self.required_quantity = 2, True, 5
                    self.frames = self.slime_sets["still"] if stop else self.slime_sets["move"]
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
            self.game["sound"]("assets/sounds/enemy_hit.mp3")
        self.health -= damage
        self.get_angry = True
        if self.health <= 0 and not self.die_flag:
            self.die(self.game["hero"])

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def die(self, hero):
        if self.health <= 0:
            self.game["music"]("assets/sounds/death_enemy.mp3")
            hero.balance += self.gold_drops
            hero.xp_progress += self.xp_drops
            hero.check_level()
            self.vision.kill()
            self.cur_frame, self.die_flag = 0, True

    def get_stats(self):
        return self.name, self.damage, self.health, self.speed, self.range
