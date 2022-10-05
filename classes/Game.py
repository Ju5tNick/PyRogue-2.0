import sys
import time
import pygame
import schedule
from random import randrange, choice

from classes.MainHero import MainHero
from classes.Object import Object
from classes.Slime import Slime
from classes.Tile import AvailableTile, UnavailableTile
from classes.Trader import Trader
from classes.Weapon import Weapon
from helpers.config import FIELD_SIZE_Y, FIELD_SIZE_X, TILE_WIDTH, TILES_COUNT_X, TILES_COUNT_Y, TILE_HEIGHT
from helpers.images import OTHER_OBJECTS, load_image, POTIONS


class Game:
    screen = pygame.display.set_mode((TILES_COUNT_X * TILE_WIDTH, TILES_COUNT_Y * TILE_HEIGHT))

    field = [[None for _ in range(FIELD_SIZE_X)] for _ in range(FIELD_SIZE_Y)]
    cur_x = 2
    cur_y = 2
    is_trader_active = False
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

    def __init__(self):
        pygame.init()
        pygame.font.Font(None, 25)
        pygame.mouse.set_visible(True)
        pygame.display.set_caption('PyRogue')
        pygame.display.set_icon(OTHER_OBJECTS["logo"])

        self.is_weapon_active = False
        self.hero = MainHero([10, 10], 'MainHero', 200, money=200)
        self.weapons.add(self.hero.get_weapon())
        self.mainhero.add(self.hero)
        self.nearest_trader = Trader()
        self.trader.add(self.nearest_trader)
        self.up = self.down = self.left = self.right = False

        self.background.add(Object(
            OTHER_OBJECTS["background"][0], [0, 0], [TILES_COUNT_X * TILE_WIDTH, TILES_COUNT_Y * TILE_HEIGHT],
            False
        ))

        for potion in self.nearest_trader.get_trades():
            self.shop.add(potion)

        self.shop.add(
            Object(OTHER_OBJECTS["merchant"][0], [254, 276], [101, 107], True, info=OTHER_OBJECTS["merchant"][1])
        )

        self.chunk, self.other_obj = self.generate(no_water=True)
        self.available_tile, self.unavailable_tile = self.render_map(self.chunk)

    def render_map(self, chunk):
        cant_go = pygame.sprite.Group()
        can_go = pygame.sprite.Group()
        for rrow in range(TILES_COUNT_Y):
            for rcol in range(TILES_COUNT_X):
                flag = False
                if chunk[rrow][rcol] in range(6):
                    tile = AvailableTile(f"assets/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png", rcol, rrow)
                elif chunk[rrow][rcol] in range(6, 9):
                    tile, flag = UnavailableTile(f"assets/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png", rcol, rrow), True
                elif chunk[rrow][rcol] in range(9, 12):
                    tile = AvailableTile(f"assets/images/tiles/sand/sand{chunk[rrow][rcol] - 8}.png", rcol, rrow)

                if flag:
                    cant_go.add(tile)
                else:
                    can_go.add(tile)
        return can_go, cant_go

    def generate(self, no_water=False):
        other_object = pygame.sprite.Group()
        chunk, flag = [], False
        for i in range(TILES_COUNT_Y):
            intermediate = []
            for j in range(TILES_COUNT_X):

                if randrange(300) in range(100) and flag == False and not no_water:
                    if 2 < i < TILES_COUNT_Y - 12:
                        r_lenght, r_width, flag = randrange(2, 4), randrange(7, 14), True
                        r_lenght_2, loc_x, r_width_2 = r_lenght, randrange(13, TILES_COUNT_X - 15), r_width

                if flag and r_lenght_2 != 0 and sum([intermediate.count(i) for i in range(6)]) == loc_x:
                    intermediate.append(randrange(6, 9))
                    if randrange(100) in range(5):
                        tile = pygame.sprite.Sprite()
                        image = pygame.transform.rotate(OTHER_OBJECTS["water_lily"], randrange(1, 361))
                        tile.image = image
                        tile.rect = image.get_rect()
                        tile.rect.x, tile.rect.y = j * TILE_WIDTH + randrange(10), i * TILE_WIDTH + randrange(10)
                        other_object.add(tile)
                    r_lenght_2 -= 1

                elif len(intermediate) != TILES_COUNT_X:
                    intermediate.append(randrange(6))
                    if randrange(100) in range(50):
                        tile = pygame.sprite.Sprite()
                        image = OTHER_OBJECTS["tall_grass"]
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
            for i in range(TILES_COUNT_Y):
                for j in range(TILES_COUNT_X):
                    if i < TILES_COUNT_Y - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i + 1][j] in list(
                            range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        chunk[i - 1][j] = randrange(9, 12) if i < TILES_COUNT_Y - 2 else 1
                        chunk[i][j - 1] = randrange(9, 12) if j != TILES_COUNT_X - 2 else 1
                        flag = True

                    if i - 1 != 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i - 1][j] in list(
                            range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        if i + 1 < TILES_COUNT_Y:
                            chunk[i + 1][j] = randrange(9, 12)
                        chunk[i][j - 1] = randrange(9, 12) if j - 2 > 0 else 1
                        flag = True

                    if j < TILES_COUNT_X - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j + 1] in list(
                            range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        chunk[i][j - 1] = randrange(9, 12) if j < TILES_COUNT_X - 2 else 1
                        flag = True

                    if j - 1 > 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j - 1] in list(
                            range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        chunk[i][j + 1] = randrange(9, 12) if j - 2 > 0 else 1

                    if i < TILES_COUNT_Y - 2 and j < TILES_COUNT_X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i + 1][j + 1] in list(
                            range(6)):
                        chunk[i + 1][j + 1] = randrange(9, 12)
                        flag = True
                    if i - 2 != 0 and j < TILES_COUNT_X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i - 1][j + 1] in list(
                            range(6)):
                        chunk[i - 1][j + 1] = randrange(9, 12)
                        flag = True

                    if chunk[i][j] in range(9, 12):
                        if randrange(100) in range(20):
                            tile = pygame.sprite.Sprite()
                            image = load_image(f"assets/images/objects/rock{choice([1, 2])}.png")
                            tile.image = image
                            tile.rect = image.get_rect()
                            tile.rect.x, tile.rect.y = (j - 0.5) * 26 + randrange(-5, 6), (i - 0.5) * 26 + randrange(-5,
                                                                                                                     6)
                            other_object.add(tile)

        return chunk, other_object

    def enemy_move(self):
        [schedule.every(3).to(5).seconds.do(elem.set_flag) for elem in self.enemies]

    def draw_interface(self):
        # hp_bar
        pygame.draw.rect(self.screen, (0, 0, 0), (TILES_COUNT_X * TILE_WIDTH - 195, 5, 190, 17))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (TILES_COUNT_X * TILE_WIDTH - 194, 6, (self.hero.get_hp() / self.hero.get_max_hp() * 190 - 2), 15))

        self.screen.blit(pygame.font.Font(None, 21).render(str(self.hero.get_hp()).rjust(3, '0'), True, (255, 255, 255)),
                    (TILES_COUNT_X * TILE_WIDTH - 100, 7))
        self.screen.blit(OTHER_OBJECTS["heart"], (TILES_COUNT_X * TILE_WIDTH - 115, 6))

        # experience_bar
        pygame.draw.rect(self.screen, (0, 0, 0), (TILES_COUNT_X * TILE_WIDTH - 95, 24, 90, 17))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (TILES_COUNT_X * TILE_WIDTH - 94, 25, (self.hero.get_ex()[0] / self.hero.get_ex()[1] * 90 - 1), 15))
        self.screen.blit(
            pygame.font.Font(None, 14).render(f"lvl: {self.hero.get_ex()[-1]} exp: {self.hero.get_ex()[0]} / {self.hero.get_ex()[1]}",
                                              True, (120, 120, 120)), (TILES_COUNT_X * TILE_WIDTH - 90, 28))
        # money_bar
        self.screen.blit(pygame.font.Font(None, 25).render(str(self.hero.get_balance()).rjust(5, '0'), True, (254, 226, 66)),
                    (TILES_COUNT_X * TILE_WIDTH - 70, 44))
        self.screen.blit(OTHER_OBJECTS["coin"], (TILES_COUNT_X * TILE_WIDTH - 21, 42))

        # stamina
        pygame.draw.rect(self.screen, (0, 0, 0), (TILES_COUNT_X * TILE_WIDTH - 195, 24, 95, 17))
        pygame.draw.rect(self.screen, (64, 105, 194), (TILES_COUNT_X * TILE_WIDTH - 194, 25, (self.hero.get_stamina()[1] 
                        / self.hero.get_stamina()[0] * 95 - 2), 15))

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def start_screen(self):
        image, running = OTHER_OBJECTS["begin"], True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 772 <= event.pos[0] <= 832 and 249 <= event.pos[1] <= 271:
                        running = False

                    if 787 <= event.pos[0] <= 832 and 276 <= event.pos[1] <= 293:
                        self.terminate()
                self.screen.blit(image, (0, 0))
                pygame.display.flip()

    def game_over(self):
        self.is_first_session = False
        image, running = OTHER_OBJECTS["game_over"], True
        time.sleep(0.1)
        self.music("assets/sounds/game_over.mp3")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_screen(self)
                self.screen.blit(image, (0, 0))
                pygame.display.flip()

    @staticmethod
    def music(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    @staticmethod
    def sound(filename):
        pygame.mixer.Sound(filename).play()

    def obj_move(self):
        for elem in self.shop:
            elem.move()

    def loop(self):
        available_tile, unavailable_tile = self.render_map(self.chunk)
        available_tile.draw(self.screen)
        unavailable_tile.draw(self.screen)
        self.field[self.cur_y][self.cur_x] = available_tile, unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, self.trader, self.clots, self.chunk
        self.trader.draw(self.screen)
        self.clots.draw(self.screen)
        self.mainhero.draw(self.screen)
        self.weapons.draw(self.screen)
        self.draw_interface()
        self.is_chosen = [False, ""]
        self.is_running = False

        schedule.every(2).to(5).seconds.do(self.enemy_move)
        schedule.every(0.5).seconds.do(self.obj_move)

        self.start_screen()

        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    keys, flag = pygame.key.get_pressed(), True

                    if keys[pygame.K_m] and self.nearest_trader.check(self.mainhero):
                        self.is_trader_active = False if self.is_trader_active else True
                        if self.is_trader_active:
                            self.music("assets/sounds/morshu.wav")
                        self.up = self.down = self.right = self.left = False

                    if keys[pygame.K_w] and not self.is_trader_active:
                        self.up, self.down = True, False
                    if keys[pygame.K_a] and not self.is_trader_active:
                        self.left, self.right = True, False
                    if keys[pygame.K_s] and not self.is_trader_active:
                        self.down, self.up = True, False
                    if keys[pygame.K_d] and not self.is_trader_active:
                        self.right, self.left = True, False

                    if keys[pygame.K_y] and self.is_trader_active and self.is_chosen[0]:
                        self.nearest_trader.sell(self.hero, self.is_chosen[1], self.sound)

                    if keys[pygame.K_n] and self.is_trader_active and self.is_chosen[0]:
                        self.is_chosen = [False, ""]

                    if self.hero.get_stamina()[1] <= 20:
                        
                        self.is_running = False                        

                    else:
                        if (keys[pygame.K_LSHIFT] and not self.is_trader_active and 
                            (self.up or self.down or self.left or self.right)):
                            self.is_running = True


                if event.type == pygame.KEYUP and not self.is_trader_active:
                    if keys[pygame.K_LSHIFT]:
                        self.is_running = False

                    if keys[pygame.K_w]:
                        self.up = False
                        self.hero.move(self.chunk, "up", stop=True)
                    if keys[pygame.K_a]:
                        self.left = False
                        self.hero.move(self.chunk, "left", stop=True)
                    if keys[pygame.K_s]:
                        self.down = False
                        self.hero.move(self.chunk, "down", stop=True)
                    if keys[pygame.K_d]:
                        self.right = False
                        self.hero.move(self.chunk, "right", stop=True)

                if self.is_trader_active and self.nearest_trader.check(self.mainhero):
                    self.nearest_trader.draw_interface(Game)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for elem in self.shop:
                            if elem.check(event.pos):
                                self.is_chosen = [True, elem]
                                self.nearest_trader.say(self.screen, obj=elem)
                                break
                            else:
                                self.is_chosen = [False, elem]
                else:
                    self.is_chosen = [False, ""]

                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():

                    if self.hero.check(event.pos) and not self.is_trader_active:
                        self.is_weapon_active = True
                        pygame.mouse.set_visible(False)
                    else:
                        self.is_weapon_active = False
                        pygame.mouse.set_visible(True)

                    if self.is_weapon_active:
                        for elem in self.weapons:
                            self.is_weapon_active = elem.move(*event.pos, *event.rel, self.hero, self.enemies, self.is_weapon_active)

            if self.up:
                self.hero.move(self.chunk, "up")
            elif self.down:
                self.hero.move(self.chunk, "down")
            elif self.left:
                self.hero.move(self.chunk, "left")
            elif self.right:
                self.hero.move(self.chunk, "right")

            x, y = self.hero.get_coords()[0], self.hero.get_coords()[1]

            if TILES_COUNT_X * TILE_WIDTH <= x or x <= 0 or TILES_COUNT_Y * TILE_HEIGHT <= y or y <= 0:

                if TILES_COUNT_X * TILE_WIDTH <= x:
                    self.cur_x += 1
                if x <= 0:
                    self.cur_x -= 1
                if TILES_COUNT_Y * TILE_HEIGHT <= y:
                    self.cur_y += 1
                if y <= 0:
                    self.cur_y -= 1

                cur_x = FIELD_SIZE_X - 1 if self.cur_x < 0 else self.cur_x
                cur_y = FIELD_SIZE_Y - 1 if self.cur_y < 0 else self.cur_y
                cur_x = 0 if cur_x >= FIELD_SIZE_X else cur_x
                cur_y = 0 if cur_y >= FIELD_SIZE_Y else cur_y

                if self.field[cur_y][cur_x] is None:
                    self.chunk, self.other_obj = self.generate()
                    self.available_tile, self.unavailable_tile = self.render_map(self.chunk)
                    self.enemy_visions = pygame.sprite.Group()
                    self.enemies = pygame.sprite.Group()
                    self.trader = pygame.sprite.Group()
                    self.clots = pygame.sprite.Group()
                    for _ in range(randrange(5, 10)):
                        params = {
                            "hero": self.hero,
                            "chunk": self.chunk,
                            "available_tile": self.available_tile,
                            "enemy_visions": self.enemy_visions,
                            "sound": self.sound,
                            "music": self.music,
                            "clots": self.clots,
                        }
                        self.enemies.add(Slime("name", 10, 100, 2, 5, randrange(5, 15), randrange(10, 21), params))
                    self.field[cur_y][cur_x] = self.available_tile, self.unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, self.trader, self.clots, self.chunk
                else:
                    self.available_tile, self.unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, self.trader, self.clots, self.chunk = self.field[cur_y][cur_x]

            if TILES_COUNT_X * TILE_WIDTH <= self.hero.get_coords()[0]:
                self.hero.set_coords(1, self.hero.get_coords()[1])

            elif self.hero.get_coords()[0] <= 0:
                self.hero.set_coords(TILES_COUNT_X * TILE_WIDTH, self.hero.get_coords()[1])

            if TILES_COUNT_Y * TILE_HEIGHT <= self.hero.get_coords()[1]:
                self.hero.set_coords(self.hero.get_coords()[0], 1)

            elif self.hero.get_coords()[1] <= 0:
                self.hero.set_coords(self.hero.get_coords()[0], TILES_COUNT_Y * TILE_HEIGHT)

            schedule.run_pending()
            self.hero.heal()
            self.hero.running(self.is_running)

            if not self.is_trader_active:
                [elem.update() for elem in self.enemy_visions]
                [clot.move(self.hero, self.mainhero, self.weapons, Game) for clot in self.clots]
                [elem.move(self.hero.get_coords(), self.mainhero) for elem in self.enemies]
                self.available_tile.draw(self.screen)
                self.unavailable_tile.draw(self.screen)
                self.other_obj.draw(self.screen)
                self.trader.draw(self.screen)
                self.enemy_visions.draw(self.screen)
                self.enemies.draw(self.screen)
                self.clots.draw(self.screen)
                pygame.draw.circle(self.screen, (70, 79, 21), (self.hero.get_coords()[0] + 19 / 2, self.hero.get_coords()[1] + 31 / 2),
                                   self.hero.get_range(), 1)
                self.mainhero.draw(self.screen)
                if self.is_weapon_active:
                    self.weapons.draw(self.screen)
            else:
                self.nearest_trader.draw_interface(Game)

            self.draw_interface()

            if self.is_chosen[0]:
                self.nearest_trader.say(self.screen, obj=elem)

            pygame.display.flip()
            self.clock.tick(30)
