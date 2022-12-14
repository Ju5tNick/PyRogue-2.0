from classes.Sound import Sound
from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_Y, TILES_COUNT_X
from classes.Slime import Slime
from helpers.images import EXP_SLIME_SETS
from helpers.sounds import SOUNDS


class ExpSlime(Slime):

    def __init__(self, name, sltype, base_damage, base_health, base_speed, gold_drops, xp_drops, game_params, coords=[]):
        super().__init__(name, sltype, base_damage, base_health, base_speed, gold_drops, xp_drops, game_params, coords=coords)
        self.game = game_params

        self.name, self.damage, self.health, self.speed = name, base_damage, base_health, base_speed
        self.exp_flag, self.max_health = False, base_health

        self.get_angry = False
        self.animation_counter, self.required_quantity = 0, 5

        self.slime_sets = EXP_SLIME_SETS

        self.cur_frame, self.frames = 0, []
        self.die_flag = False

        self.game["enemy_visions"].add(self.vision)
        self.gold_drops, self.get_angry = gold_drops, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True
        self.coins = []
        self.coords = [self.rect.x, self.rect.y]

    def move(self, *qwargs):
        flag = True
        hero_coords = self.game["hero"].get_coords()
        if self.frames == self.slime_sets["explosive"]:
            self.can_move = False

        if self.vision.check(self.game["hero_group"]) and not self.angry and not self.exp_flag:
            self.vision.set_flag()
            self.get_angry = True

        if self.angry:
            if self.can_move:
                move = [self.speed, 0, -self.speed]

                diff_y, diff_x = abs(hero_coords[0] - self.rect.x), abs(hero_coords[1] - self.rect.y)
                del_x, del_y = 0, 0

                if abs(hero_coords[0]) - abs(self.rect.x) != 1:
                    for elem in move:
                        if abs(hero_coords[0] - (self.rect.x + elem)) < diff_y:
                            del_y, flag = elem, False

                if abs(hero_coords[1]) - abs(self.rect.y) != 1:
                    for elem in move:
                        if abs(hero_coords[1] - (self.rect.y + elem)) < diff_x:
                            del_x, flag = elem, False

                self.vision.move(del_y, del_x)
                self.rect = self.rect.move(del_y, del_x)

            if (abs(self.game["hero"].get_coords()[0] - self.rect.x) <= 10 and abs(
                    self.game["hero"].get_coords()[1] - self.rect.y) <= 10 and not self.exp_flag and self.angry and 
                    not self.die_flag):
                self.exp_flag = True
                self.can_move = False
                self.vision.exp_vision()

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
            if not self.exp_flag and not self.die_flag:

                if self.get_angry:
                    self.frames, self.can_move, self.required_quantity = self.slime_sets["gets_angry"], False, 7

                    if self.cur_frame == 3:
                        self.angry, self.get_angry, self.required_quantity = True, False, 5

                elif self.angry and not self.get_angry:
                    self.frames, self.speed, self.can_move = self.slime_sets["angry_move"], 5.9, True
                    self.get_angry = False

                else:
                    self.frames = self.slime_sets["still"] if stop else self.slime_sets["move"]

            elif self.exp_flag:
                if self.image == self.slime_sets["explosive"][-1]:
                    if self.vision.check(self.game["hero_group"]):
                        self.game["hero"].get_damage(40, self.game["game"])
                    Sound.play(SOUNDS["ENEMY"]["exp-death"])
                    self.vision.kill()
                    self.kill()

                self.frames = self.slime_sets["explosive"]

            if self.die_flag:
                if self.image == self.slime_sets["die_animation"][-1]:
                    Sound.play(SOUNDS["ENEMY"]["death"])
                    self.die()
                    self.kill()

                self.frames = self.slime_sets["die_animation"]

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_counter = 0

        self.animation_counter += 1

    def get_damage(self, damage):
        if self.health > 0 and not self.exp_flag:
            Sound.play(SOUNDS["ENEMY"]["hit"])
            self.health -= damage

        if self.health <= 0:
            self.die_flag = True
            self.can_move = False
            self.vision.kill()

        if not self.angry:
            self.get_angry = True

    def die(self):
        if self.health <= 0:

            self.game["hero"].xp_progress += self.xp_drops
            self.game["hero"].check_level()

            self.vision.kill()
