import os
import sys
import pygame
import schedule
import time

from classes import *
from image_sets import *

X, Y, FIELD_X, FIELD_Y = 40, 20, 5, 5
TILE_WIDTH, TILE_HEIGT = 25, 25

#  timecode: 0:34 -- 1:10

#  +-------TILES------+
#  | 0 - 5   -- grass |
#  | 6 - 8   -- water |
#  | 9 - 11  -- sand  |
#  +------------------+


class MainHero(pygame.sprite.Sprite):

    def __init__(self, coords, name, hp, money=0):
        super().__init__(all_sprites)
        self.coords, self.hp, self.name, self.weapon, self.weapons = coords, hp, name, None, []
        self.rect, self.animation_counter, self.balance, self.xp_progress = pygame.Rect(coords[0], coords[1], 19, 31), 0, money, 1
        self.required_xp, self.level, self.max_hp, self.heal_counter, self.range = 10, 1, hp, 0, 100
        self.walk_on_water, self.stamina, self.current_stamina = False, 100, 100
        self.speed = 4

        self.moves = {
            "up": [0, -self.speed], "down": [0, self.speed],
            "left": [-self.speed, 0], "right": [self.speed, 0]
            }

        self.still = hero_sets["still"]
        self.directions = hero_sets["directions"]
        self.image = hero_sets["hero_image"]

        self.cur_frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(coords[0], coords[1])

    def move(self, direction, stop=False):
        direct = self.moves[direction].copy()

        if (5 <= self.rect.x <= X * TILE_WIDTH - 5 and 5 <= self.rect.y <= Y * TILE_HEIGT - 5 and not self.walk_on_water and
            5 <= self.rect.x + 21 <= X * TILE_WIDTH - 5 and 5 <= self.rect.y + 24 <= Y * TILE_HEIGT - 5 and not self.walk_on_water):
            if (chunk[int(self.rect.y / TILE_HEIGT)][int((self.rect.x + direct[0]) / TILE_WIDTH)] in range(6, 9) or 
                chunk[int(self.rect.y / TILE_HEIGT)][int((self.rect.x + 21 + direct[0]) / TILE_WIDTH)] in range(6, 9)):
                direct[0] = 0; stop = True
            else:
                direct[0] = direct[0]
            
            if (chunk[int((self.rect.y + direct[1]) / TILE_HEIGT)][int(self.rect.x / TILE_WIDTH)] in range(6, 9) or 
                chunk[int((self.rect.y + 24 + direct[1]) / TILE_HEIGT)][int(self.rect.x / TILE_WIDTH)] in range(6, 9)):
                direct[1] = 0; stop = True
            else:
                direct[1] = direct[1]


        self.rect = self.rect.move(*direct)

        if stop:
            self.image = self.still[direction]
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.update(direction)

    def get_hp(self):
        return self.hp

    def get_range(self):
        return self.range

    def get_max_hp(self):
        return self.max_hp

    def get_damage(self, damage):
        sound("data/sounds/mh_hit.mp3")
        self.hp -= damage
        if self.hp <= 0:
            sound("data/sounds/death_mh.mp3")
            game_over()
            

    def add_hp(self, hp):
        self.max_hp += hp

    def buy(self, price):
        if self.balance - price >= 0:
            self.balance -= price

    def check_water(self):
        return pygame.sprite.spritecollideany(self, cant_go_tiles)

    def update(self, direction):
        if self.animation_counter == 5:
            self.frames = self.directions[direction]
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
                self.hp += 1; self.heal_counter = 0
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
            weapons.add(weapon)

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
        if (abs(self.rect.x - mouse_coords[0]) ** 2 + abs(self.rect.y - mouse_coords[1]) ** 2) ** 0.5 <= self.range + 15:
            return True
        return False

    def get_stamina(self):
        return (self.stamina, self.current_stamina)

    def add_stamin(self, value):
        self.stamina += value

    def running(self):
        pass


class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, base_damage, base_health, base_speed, range, gold_drops, xp_drops):
        super().__init__(all_sprites)
        self.name, self.damage, self.health, self.speed = name, base_damage, base_health, base_speed
        self.range, self.die_flag, self.max_health = range, False, base_health
        self.rect = pygame.Rect(*[randrange(50, X * TILE_WIDTH - 50), randrange(50, Y * TILE_HEIGT - 50)], 21, 24)
        while pygame.sprite.spritecollideany(self, cant_go_tiles):
            self.rect = pygame.Rect(*[randrange(50, X * TILE_WIDTH - 50), randrange(50, Y * TILE_HEIGT - 50)], 21, 24)
        
        self.get_angry, self.attack = False, False
        self.animation_counter, self.required_quantity = 0, 5

        self.still, self.moves = enemy_sets["still"], enemy_sets["moves"]
        self.angry_moves, self.gets_angry = enemy_sets["angry_moves"], enemy_sets["gets_angry"]
        self.die_ani, self.attack_ani = enemy_sets["die_animation"], enemy_sets["attack_animation"]

        self.image = enemy_sets["image"]
        self.cur_frame, self.frames = 0, []

        self.vision = Vision_for_enemy(100, (self.rect.x, self.rect.y), self)
        enemy_visions.add(self.vision)
        self.gold_drops, self.get_angry, self.angry = gold_drops, False, False
        self.xp_drops, self.flag, self.can_move = xp_drops, -1, True

    def move(self, hero_coords):
        flag = True
        if self.frames == self.die_ani:
            self.can_move = False
        if self.vision.check() or self.angry:
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

            if hero.check_water():
                self.can_move, self.attack = False, True  

            if abs(hero.get_coords()[0] - self.rect.x) <= 10 and abs(hero.get_coords()[1] - self.rect.y) <= 10 and not self.die_flag:
                self.attack = True
        else:
            self.attack = False
            
            if self.angry and self.get_angry:
                self.angry, self.get_angry = False, False

            if self.flag == 1 and not self.angry and not self.get_angry and self.direction != [0, 0] and self.can_move:
                flag = False
                if self.rect.x + 1 >= X * TILE_WIDTH - 50 or chunk[int(self.rect.y / TILE_HEIGT)][int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[0] = -1
                elif self.rect.x - 1 <= 50 or chunk[int(self.rect.y / TILE_HEIGT)][int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[0] = 1
                if self.rect.y + 1 >= Y * TILE_HEIGT - 50 or chunk[int((self.rect.y + 1) / TILE_HEIGT)][int(self.rect.x / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1
                elif self.rect.y - 1 <= 50 or chunk[int((self.rect.y - 1) / TILE_HEIGT)][int(self.rect.x / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1

                if chunk[int((self.rect.y - 1) / TILE_HEIGT)][int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1; self.direction[0] = 1
                elif chunk[int((self.rect.y + 1) / TILE_HEIGT)][int((self.rect.x - 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1; self.direction[0] = 1
                elif chunk[int((self.rect.y - 1) / TILE_HEIGT)][int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = 1; self.direction[0] = -1
                elif chunk[int((self.rect.y + 1) / TILE_HEIGT)][int((self.rect.x + 1) / TILE_WIDTH)] in range(6, 9):
                    self.direction[1] = -1; self.direction[0] = -1

                self.rect = self.rect.move(self.direction[0], self.direction[1])
                self.vision.move(self.direction[0], self.direction[1])

        self.update(stop=flag)

    def update(self, stop=False):
        if self.animation_counter == self.required_quantity:
            if not self.die_flag:
                if self.angry:
                    self.frames, self.speed, self.can_move = self.angry_moves, 5.9, True
                    # self.angry = False if not self.vision.check() else True
                elif self.get_angry:
                    self.frames, self.can_move, self.required_quantity = self.gets_angry, False, 7
                    if self.cur_frame == 3:
                        sound("data/sounds/get_angry_e.wav")
                        self.angry, self.get_angry, self.required_quantity = True, False, 5
                else:
                    self.speed = 2
                    self.frames = self.still if stop else self.moves
                if self.attack:
                    self.frames, self.can_move, self.required_quantity = self.attack_ani, False, 3
                    if self.cur_frame == 6 and hero.check_water():
                        self.clot = Enemies_clot((self.rect.x, self.rect.y)); clots.add(self.clot)
                    elif self.cur_frame == 6 and not hero.check_water():
                        self.attack, self.can_move, self.required_quantity = False, True, 5
                        self.clot = Enemies_clot((self.rect.x, self.rect.y)); clots.add(self.clot)
                elif not self.attack and not self.angry and not self.get_angry:
                    self.speed, self.can_move, self.required_quantity = 2, True, 5
                    self.frames = self.still if stop else self.moves
            else:
                if self.image == self.die_ani[-1]:
                    self.kill()
                self.frames = self.die_ani
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
            sound("data/sounds/enemy_hit.mp3")
        self.health -= damage
        self.get_angry = True
        if self.health <= 0 and not self.die_flag:
            self.die(hero)

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health
        
    def die(self, hero):
        if self.health <= 0:
            music("data/sounds/death_enemy.mp3")
            hero.balance += self.gold_drops
            hero.xp_progress += self.xp_drops
            hero.check_level()
            self.vision.kill()
            self.cur_frame, self.die_flag = 0, True
    
    def get_stats(self):
        return (self.name, self.damage, self.health, self.speed, self.range)


class Vision_for_enemy(pygame.sprite.Sprite):

    def __init__(self, range, coords, enemy):
        super().__init__(all_sprites)
        self.host, self.range = enemy, range
        self.image = pygame.Surface((3 * self.range, 3 * self.range), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (70, 79, 21), (self.range, self.range), self.range, 1)
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        self.rect = pygame.Rect(coords[0] - self.range + 10.5, coords[1] - self.range + 12, 1.85 * self.range, 1.85 * self.range)

    def update(self):
        pygame.draw.rect(self.image, (0, 0, 0), (self.range - 10, self.range - 16, 22, 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.range - 9, self.range - 15, (self.host.get_health() / self.host.get_max_health() * 22 - 2), 3))

    def move(self, del_x, del_y):
        self.rect = self.rect.move(del_x, del_y)

    def check(self):
        return pygame.sprite.spritecollideany(self, mainhero)


class Trader(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(all_sprites)
        self.image = trader_sets["image"]
        self.rect = pygame.Rect(X * TILE_WIDTH / 2 - 200, Y * TILE_HEIGT / 2 - 150, 400, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.trades = [] # (price, eff_type, eff_value, stock)
        for i in range(20):
            price = randint(10, 100)
            eff_type = randint(0, 1)
            eff_value = int(price / 5 / (eff_type + 1))
            stock = int(30 / (eff_type + 1) / eff_value)
            self.trades.append([price, eff_type, eff_value, stock])

    def sell(self, mainhero, obj):
        if hero.get_balance() - obj.get_cost() >= 0 and obj.get_cost() != 0:
            sound("data/sounds/buy.wav")
            hero.buy(obj.get_cost())

    def get_trades(self):
        return self.trades

    def check(self):
        return pygame.sprite.spritecollideany(self, mainhero)  # возвращает булевый тип(пересеклись ли спрайты)

    def draw_interface(self):
        pygame.mouse.set_visible(True)
        background.draw(screen)
        shop.draw(screen)
        

    def say(self, obj):
        screen.blit(pygame.font.Font(None, 25).render(obj.get_info(), True, (255, 255, 255)), (50, 44))


class Weapon(pygame.sprite.Sprite):

    def __init__(self, damage, coords, range):
        super().__init__(all_sprites)
        self.image, self.default_image = weapon_sets["image"], weapon_sets["default_image"]
        self.mask, self.range, self.damage = pygame.mask.from_surface(self.image), range, damage
        self.rect, self.crossing = self.image.get_rect(), True

        self.flips = {"++": -90, "=+": -135, "-+": -180, "-=": 135, "": -1,
                      "--": 90, "=-": 45, "+-": 0, "+=": -45, "==": -1}

    def move(self, x, y, del_x, del_y):
        global weapon_activated
        if hero.check((x, y)):
            pygame.mouse.set_visible(False)
            weapon_activated = True
            if self.flips[''.join(self.check(del_x, del_y))] != -1:
                self.image = pygame.transform.rotate(self.default_image, self.flips[''.join(self.check(del_x, del_y))])
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


class Enemies_clot(pygame.sprite.Sprite):

    def __init__(self, coords):
        super().__init__(all_sprites)
        self.image = enemy_sets["clot"]
        self.rect = pygame.Rect(coords[0], coords[1], 10, 10)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed, self.damage = 6.9, randrange(20, 45)

    def move(self, *trash):
        if pygame.sprite.spritecollide(self, weapons, False):
            self.kill()

        move = [self.speed, 0, -self.speed]   
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

        self.rect = self.rect.move(del_y, del_x)
        if pygame.sprite.spritecollide(self, mainhero, False):
            hero.get_damage(self.damage)
            self.kill()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, coords, size, can_move, info="", cost=0):
        super().__init__(all_sprites)
        self.image, self.coords, self.size, self.info = image, coords, size, info
        self.cost = cost
        self.can_move, self.counter = can_move, choice([1, -1])
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.can_move:
            if self.counter == 1:
                self.rect = self.rect.move(0, 2)
            else:
                self.rect = self.rect.move(0, -2)
            self.counter = self.counter * (-1)

    def check(self, event_coords):
        if (self.coords[0] <= event_coords[0] <= self.coords[0] + self.size[0] and
            self.coords[1] <= event_coords[1] <= self.coords[1] + self.size[1]):
            return True
        return False

    def get_info(self):
        return self.info

    def get_cost(self):
        return self.cost
        
def render_map(chunk: list):
    cant_go = pygame.sprite.Group()
    can_go = pygame.sprite.Group()
    for rrow in range(Y):
        for rcol in range(X):
            flag = False
            if chunk[rrow][rcol] in range(6):
                tile = Tile_can_go(f"data/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png", rcol, rrow)  
            elif chunk[rrow][rcol] in range(6, 9):
                tile, flag = Tile_cant_go(f"data/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png", rcol, rrow), True
            elif chunk[rrow][rcol] in range(9, 12):
                tile = Tile_can_go(f"data/images/tiles/sand/sand{chunk[rrow][rcol] - 8}.png", rcol, rrow)  

            if flag:
                cant_go.add(tile)
            else:
                can_go.add(tile)
    return can_go, cant_go


def generate(no_water=False):
    other_object = pygame.sprite.Group()
    chunk, flag = [], False
    for i in range(Y):
        intermediate = []
        for j in range(X): 
         
            if randrange(300) in range(100) and flag == False and not no_water:
                if 2 < i < Y - 12:
                    r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True
                    r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, X - 15), r_width 
         
            if flag and r_lenght_2 != 0 and sum([intermediate.count(i) for i in range(6)]) == loc_x:
                intermediate.append(randrange(6, 9))
                if randrange(100) in range(5):
                    tile = pygame.sprite.Sprite()
                    image = pygame.transform.rotate(other_objects["water_lily"], randrange(1, 361))  
                    tile.image = image
                    tile.rect = image.get_rect()
                    tile.rect.x, tile.rect.y = (j) * TILE_WIDTH + randrange(10), (i) * TILE_WIDTH + randrange(10)
                    other_object.add(tile)
                r_lenght_2 -= 1
            
            elif len(intermediate) != X:
                intermediate.append(randrange(6))
                if randrange(100) in range(50):
                    tile = pygame.sprite.Sprite()
                    image = other_objects["tall_grass"]
                    tile.image = image
                    tile.rect = image.get_rect()
                    tile.rect.x, tile.rect.y = (j - 0.5) * 26 + randrange(10), (i - 0.5) * 26 + randrange(10)
                    other_object.add(tile)
                
        if flag:
            if r_width - r_width_2 in range(0, int(r_width / 2)):
                r_lenght, loc_x = r_lenght + randrange(choice([1, 2]), 4), loc_x - randrange(1, 3)
            elif r_width - r_width_2 in range(int(r_width / 2) + 1, r_width):
                r_lenght, loc_x = r_lenght - randrange(choice([1, 2]), 4), loc_x + randrange(1, 3)

            r_width_2, r_lenght_2 = r_width_2 - 1, r_lenght
            flag = False if r_width_2 == 0 else True  

        chunk.append(intermediate)

    if choice([True, False, False]):
        for i in range(Y):
            for j in range(X):
                if i < Y - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i + 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i - 1][j] = randrange(9, 12) if i < Y - 2 else 1
                    chunk[i][j - 1] = randrange(9, 12) if j != X - 2 else 1
                    flag = True

                if i - 1 != 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i - 1][j] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    if i + 1 < Y:
                        chunk[i + 1][j] = randrange(9, 12) 
                    chunk[i][j - 1] = randrange(9, 12) if j - 2 > 0 else 1
                    flag = True     

                if j < X - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j + 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j - 1] = randrange(9, 12) if j < X - 2 else 1
                    flag = True

                if j - 1 > 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j - 1] in list(range(6, 9)):
                    chunk[i][j] = randrange(9, 12)
                    chunk[i][j + 1] = randrange(9, 12) if j - 2 > 0 else 1

                if i < Y - 2 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i + 1][j + 1] in list(range(6)):
                    chunk[i + 1][j + 1] = randrange(9, 12)
                    flag = True 
                if i - 2 != 0 and j < X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i - 1][j + 1] in list(range(6)):
                    chunk[i - 1][j + 1] = randrange(9, 12)
                    flag = True

                if chunk[i][j] in range(9, 12):
                    if randrange(100) in range(20):
                        tile = pygame.sprite.Sprite()
                        image = load_image(f"data/images/objects/rock{choice([1, 2])}.png")
                        tile.image = image
                        tile.rect = image.get_rect()
                        tile.rect.x, tile.rect.y = (j - 0.5) * 26 + randrange(-5, 6), (i - 0.5) * 26 + randrange(-5, 6)
                        other_object.add(tile) 

    return chunk, other_object


def save():
    pass


def enemy_move():
    global enemies
    [schedule.every(3).to(5).seconds.do(elem.set_flag) for elem in enemies]


def draw_interface():
    # hp_bar
    pygame.draw.rect(screen, (0, 0, 0), (X * TILE_WIDTH - 195, 5, 190, 17))
    pygame.draw.rect(screen, (255, 0, 0), (X * TILE_WIDTH - 194, 6, (hero.get_hp() / hero.get_max_hp() * 190 - 2), 15))

    screen.blit(pygame.font.Font(None, 21).render(str(hero.get_hp()).rjust(3, '0'), True, (255, 255, 255)), (X * TILE_WIDTH - 100, 7))
    screen.blit(other_objects["heart"], (X * TILE_WIDTH - 115, 6))

    # experience_bar
    pygame.draw.rect(screen, (0, 0, 0), (X * TILE_WIDTH - 95, 24, 90, 17))
    pygame.draw.rect(screen, (255, 255, 255), (X * TILE_WIDTH - 94, 25, (hero.get_ex()[0] / hero.get_ex()[1] * 90 - 1), 15))
    screen.blit(pygame.font.Font(None, 14).render(f"lvl: {hero.get_ex()[-1]} exp: {hero.get_ex()[0]} / {hero.get_ex()[1]}", True, (120, 120, 120)), (X * TILE_WIDTH - 90, 28))
    # money_bar
    screen.blit(pygame.font.Font(None, 25).render(str(hero.get_balance()).rjust(5, '0'), True, (254, 226, 66)), (X * TILE_WIDTH - 70, 44))
    screen.blit(other_objects["coin"], (X * TILE_WIDTH - 21, 42))
    # stamina
    pygame.draw.rect(screen, (0, 0, 0), (X * TILE_WIDTH - 195, 24, 95, 17))
    pygame.draw.rect(screen, (64, 105, 194), (X * TILE_WIDTH - 194, 25, (hero.get_stamina()[0] / hero.get_stamina()[1] * 95 - 2), 15))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    image, running = other_objects["begin"], True
    # music("data/sounds/begin.wav")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save()
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 772 <= event.pos[0] <= 832 and 249 <= event.pos[1] <= 271:
                    running = False
                if 787 <= event.pos[0] <= 832 and 276 <= event.pos[1] <= 293:
                    terminate()
            screen.blit(image, (0, 0))
            pygame.display.flip()


def game_over():
    image, running = other_objects["game_over"], True
    time.sleep(0.1)
    music("data/sounds/game_over.mp3")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
            screen.blit(image, (0, 0))
            pygame.display.flip()


def music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()


def sound(filename):
    pygame.mixer.Sound(filename).play()


def obj_move():
    for elem in shop:
        elem.move()
        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((X * TILE_WIDTH, Y * TILE_HEIGT))
    font = pygame.font.Font(None, 25)
    pygame.mouse.set_visible(True)
    pygame.display.set_caption('PyRogue')
    pygame.display.set_icon(other_objects["logo"])

    field = [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
    cur_x, cur_y = 2, 2
    is_trader, weapon_activated = False, False
    current_page, is_sold = 1, False
    is_chosen = [False, ""]
    clock = pygame.time.Clock()

    enemies = pygame.sprite.Group()
    f = pygame.sprite.Group()
    enemy_visions = pygame.sprite.Group()
    mainhero = pygame.sprite.Group()
    trader = pygame.sprite.Group()
    shop = pygame.sprite.Group()
    clots = pygame.sprite.Group()
    weapons = pygame.sprite.Group()
    background = pygame.sprite.Group()

    dishes = trader_sets["dishes"]
    weapons_logo = trader_sets["weapons_logo"]
    
    hero = MainHero([10, 10], 'MainHero', 200, money=200) 
    hero.add_weapon(Weapon(10, [20, 10], 100))
    nearest_trader = Trader()
    trader.add(nearest_trader)
    mainhero.add(hero)
    up, down, left, right = False, False, False, False 

    background.add(Object(other_objects["background"][0], [0, 0], [X * TILE_WIDTH, Y * TILE_HEIGT], False))

    for i, elem in enumerate(potions):
        shop.add(Object(potions[elem][0], [650 + i * 22 , 278], [21, 21], True, info=potions[elem][1], cost=potions[elem][-1]))

    shop.add(Object(other_objects["merchant"][0], [254, 276], [101, 107], True, info=other_objects["merchant"][1]))
    
    chunk, other_obj = generate(no_water=True)
    can_go_tiles, cant_go_tiles = render_map(chunk)
    can_go_tiles.draw(screen)
    cant_go_tiles.draw(screen)
    field[cur_y][cur_x] = (can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions, trader, clots, chunk)
    trader.draw(screen)
    clots.draw(screen)
    mainhero.draw(screen)
    weapons.draw(screen)
    draw_interface()

    schedule.every(2).to(5).seconds.do(enemy_move)
    schedule.every(0.5).seconds.do(obj_move)
    
    start_screen()

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save()
                terminate()

            if event.type == pygame.KEYDOWN:
                keys, flag = pygame.key.get_pressed(), True

                if keys[pygame.K_m] and nearest_trader.check():
                    is_trader = False if is_trader else True
                    if is_trader:
                        music("data/sounds/morshu.wav")
                    up, down, right, left = False, False, False, False

                if keys[pygame.K_w] and not is_trader:
                    up, down = True, False
                if keys[pygame.K_a] and not is_trader:
                    left, right = True, False
                if keys[pygame.K_s] and not is_trader:
                    down, up = True, False
                if keys[pygame.K_d] and not is_trader:
                    right, left = True, False

                if keys[pygame.K_y] and is_trader and is_chosen[0]:
                    nearest_trader.sell(hero, is_chosen[1])

                if keys[pygame.K_n] and is_trader and is_chosen[0]:
                    is_chosen = [False, ""]
                    
            if event.type == pygame.KEYUP and not is_trader:
                if keys[pygame.K_w]:
                    up = False
                    hero.move("up", stop=True) 
                if keys[pygame.K_a]:
                    left = False
                    hero.move("left", stop=True)
                if keys[pygame.K_s]:
                    down = False
                    hero.move("down", stop=True)
                if keys[pygame.K_d]:
                    right = False
                    hero.move("right", stop=True)

            if is_trader and nearest_trader.check():
                nearest_trader.draw_interface()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in shop:
                        if elem.check(event.pos):
                            is_chosen = [True, elem]
                            nearest_trader.say(elem)
                            break
                        else:
                            is_chosen = [False, elem]
            else:
                is_chosen = [False, elem]
                            

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                if hero.check(event.pos) and not is_trader:
                    weapon_activated = True
                    pygame.mouse.set_visible(False)
                else:
                    weapon_activated = False
                    pygame.mouse.set_visible(True)

                if weapon_activated:
                    [sword.move(*event.pos, *event.rel) for sword in weapons]

        if up:
            hero.move("up")
        elif down:
            hero.move("down")
        elif left:
            hero.move("left")
        elif right:
            hero.move("right")

        x, y = hero.get_coords()[0], hero.get_coords()[1]

        if X * TILE_WIDTH <= x or x <= 0 or Y * TILE_HEIGT <= y or y <= 0:

            if X * TILE_WIDTH <= x:
                cur_x += 1
            if x <= 0:
                cur_x -= 1
            if Y * TILE_HEIGT <= y:
                cur_y += 1
            if  y <= 0:
                cur_y -= 1

            cur_x = FIELD_X - 1 if cur_x < 0 else cur_x
            cur_y = FIELD_Y - 1 if cur_y < 0 else cur_y
            cur_x = 0 if cur_x >= FIELD_X else cur_x
            cur_y = 0 if cur_y >= FIELD_Y else cur_y

            if field[cur_y][cur_x] is None:
                chunk, other_obj = generate()
                can_go_tiles, cant_go_tiles = render_map(chunk)
                enemy_visions = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                trader = pygame.sprite.Group()
                clots = pygame.sprite.Group()
                for _ in range(randrange(10, 20)):
                    enemies.add(Enemy("name", 10, 100, 2, 5, randrange(5, 15), randrange(10, 21)))
                field[cur_y][cur_x] = (can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions, trader, clots, chunk)
            else:
                can_go_tiles, cant_go_tiles, other_obj, enemies, enemy_visions, trader, clots, chunk = field[cur_y][cur_x]

        if X * TILE_WIDTH <= hero.get_coords()[0]:
            hero.set_coords(1, hero.get_coords()[1])

        elif hero.get_coords()[0] <= 0:
            hero.set_coords(X * TILE_WIDTH, hero.get_coords()[1])

        if Y * TILE_HEIGT <= hero.get_coords()[1]:
            hero.set_coords(hero.get_coords()[0], 1)

        elif hero.get_coords()[1] <= 0:
            hero.set_coords(hero.get_coords()[0], Y * TILE_HEIGT)

        schedule.run_pending()
        hero.heal()

        if not is_trader:
            [elem.update() for elem in enemy_visions]
            [clot.move() for clot in clots]
            [elem.move(hero.get_coords()) for elem in enemies] 
            can_go_tiles.draw(screen)
            cant_go_tiles.draw(screen)
            other_obj.draw(screen)
            trader.draw(screen)
            enemy_visions.draw(screen)
            enemies.draw(screen)
            clots.draw(screen)
            pygame.draw.circle(screen, (70, 79, 21), (hero.get_coords()[0] + 19 / 2, hero.get_coords()[1] + 31 / 2), hero.get_range(), 1)
            mainhero.draw(screen)
            if weapon_activated:
                weapons.draw(screen)
        else:
            nearest_trader.draw_interface()

        draw_interface() 

        if is_chosen[0]:
            nearest_trader.say(elem)         

        pygame.display.flip()
        clock.tick(30)
