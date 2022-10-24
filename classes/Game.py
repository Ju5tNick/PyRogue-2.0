import pygame.display
import schedule

from random import randrange, choice
from itertools import cycle

from classes.Animator import Animator
from classes.Image import Image
from classes.MainHero import MainHero
from classes.Object import Object
from classes.Slime import Slime
from classes.ExpSlime import ExpSlime
from classes.Sound import Sound
from classes.Tile import AvailableTile, UnavailableTile
from classes.Trader import Trader
from classes.Boss import Boss
from helpers.common import terminate
from helpers.config import *
from helpers.images import OTHER_OBJECTS, load_image, MERCHANT_PHRASES
from helpers.sounds import SOUNDS
from helpers.tips import TIPS
from helpers.trader_speech import *


class Game:
    screen = pygame.display.set_mode((TILES_COUNT_X * TILE_WIDTH, TILES_COUNT_Y * TILE_HEIGHT))

    def __init__(self):
        pygame.init()
        pygame.font.Font(None, 25)
        pygame.mouse.set_visible(True)
        pygame.display.set_caption('PyRogue')
        pygame.display.set_icon(OTHER_OBJECTS["logo"])

        self.enemies = pygame.sprite.Group()
        self.enemy_visions = pygame.sprite.Group()
        self.mainhero = pygame.sprite.Group()
        self.trader = pygame.sprite.Group()
        self.shop = pygame.sprite.Group()
        self.clots = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.tips = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.cracks = pygame.sprite.Group()
        self.eggs = pygame.sprite.Group()

        self.field = [[None for _ in range(FIELD_SIZE_X)] for _ in range(FIELD_SIZE_Y)]
        self.cur_x = self.cur_y = 2
        self.new_x = self.new_y = cycle([2, 3, 4, 0, 1])
        self.is_trader_active = False
        self.is_chosen = [False, ""]
        self.clock = pygame.time.Clock()
        self.now_playing = None
        self.is_someone_angry = False
        self.tip_counter = 1

        self.is_weapon_active = False
        self.is_first_time_at_merchant = True
        self.hero = MainHero([50, 50], 'MainHero', HERO_HP, money=HERO_MONEY)
        self.weapons.add(self.hero.get_weapon())
        self.mainhero.add(self.hero)
        self.nearest_trader = Trader()
        self.trader.add(self.nearest_trader)
        self.tips.add(TIPS[0])
        self.is_game_win = False

        self.background.add(Object(
            OTHER_OBJECTS["background"][0], [0, 0], [TILES_COUNT_X * TILE_WIDTH, TILES_COUNT_Y * TILE_HEIGHT],
            False
        ))

        for potion in self.nearest_trader.get_trades():
            self.shop.add(potion)

        self.shop.add(
            Object(OTHER_OBJECTS["merchant"], [254, 276], [101, 107], True, info=MERCHANT_PHRASES["irritaion"])
        )

        self.chunk, self.other_obj = self.generate(no_water=True)
        self.available_tile, self.unavailable_tile = self.render_map(self.chunk)

        self.params = {
            "hero": self.hero,
            "chunk": self.chunk,
            "hero_group": self.mainhero,
            "available_tile": self.available_tile,
            "enemy_visions": self.enemy_visions,
            "clots": self.clots,
            "screen": self.screen,
            "game": Game,
            "egg_group": self.eggs,
            "crack_group": self.cracks
        }

    def render_map(self, chunk):
        cant_go = pygame.sprite.Group()
        can_go = pygame.sprite.Group()
        for rrow in range(TILES_COUNT_Y):
            for rcol in range(TILES_COUNT_X):
                flag = False
                if chunk[rrow][rcol] in range(6):
                    tile = AvailableTile(f"assets/images/tiles/grass/grass{chunk[rrow][rcol] + 1}.png", rcol, rrow)
                elif chunk[rrow][rcol] in range(6, 9):
                    tile, flag = UnavailableTile(f"assets/images/tiles/water/water3{chunk[rrow][rcol] - 5}.png", rcol,
                                                 rrow), True
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
                    if i < TILES_COUNT_Y - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i + 1][
                        j] in list(
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

                    if j < TILES_COUNT_X - 1 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][
                        j + 1] in list(
                        range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        chunk[i][j - 1] = randrange(9, 12) if j < TILES_COUNT_X - 2 else 1
                        flag = True

                    if j - 1 > 0 and chunk[i][j] in list(range(6)) + list(range(9, 12)) and chunk[i][j - 1] in list(
                            range(6, 9)):
                        chunk[i][j] = randrange(9, 12)
                        chunk[i][j + 1] = randrange(9, 12) if j - 2 > 0 else 1

                    if i < TILES_COUNT_Y - 2 and j < TILES_COUNT_X - 2 and chunk[i][j] in list(range(6, 9)) and \
                            chunk[i + 1][j + 1] in list(
                        range(6)):
                        chunk[i + 1][j + 1] = randrange(9, 12)
                        flag = True
                    if i - 2 != 0 and j < TILES_COUNT_X - 2 and chunk[i][j] in list(range(6, 9)) and chunk[i - 1][
                        j + 1] in list(
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
                         (TILES_COUNT_X * TILE_WIDTH - 194, 6, (self.hero.get_hp() / self.hero.get_max_hp() * 190 - 2),
                          15))

        self.screen.blit(
            pygame.font.Font(None, 21).render(str(self.hero.get_hp()).rjust(3, '0'), True, (255, 255, 255)),
            (TILES_COUNT_X * TILE_WIDTH - 100, 7))
        self.screen.blit(OTHER_OBJECTS["heart"], (TILES_COUNT_X * TILE_WIDTH - 115, 6))

        # experience_bar
        pygame.draw.rect(self.screen, (0, 0, 0), (TILES_COUNT_X * TILE_WIDTH - 95, 24, 90, 17))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (TILES_COUNT_X * TILE_WIDTH - 94, 25, (self.hero.get_ex()[0] / self.hero.get_ex()[1] * 90 - 1),
                          15))
        self.screen.blit(
            pygame.font.Font(None, 14).render(
                f"lvl: {self.hero.get_ex()[-1]} exp: {self.hero.get_ex()[0]} / {self.hero.get_ex()[1]}",
                True, (120, 120, 120)), (TILES_COUNT_X * TILE_WIDTH - 90, 28))
        # money_bar
        self.screen.blit(
            pygame.font.Font(None, 25).render(str(self.hero.get_balance()).rjust(5, '0'), True, (254, 226, 66)),
            (TILES_COUNT_X * TILE_WIDTH - 70, 44))
        self.screen.blit(OTHER_OBJECTS["coin"], (TILES_COUNT_X * TILE_WIDTH - 21, 42))

        # stamina
        pygame.draw.rect(self.screen, (0, 0, 0), (TILES_COUNT_X * TILE_WIDTH - 195, 24, 95, 17))
        pygame.draw.rect(self.screen, (64, 105, 194), (TILES_COUNT_X * TILE_WIDTH - 194, 25, (self.hero.get_stamina()[1]
                                                                                              / self.hero.get_stamina()[
                                                                                                  0] * 95 - 2), 15))

    def draw_sprites(self, auto_update=True, without_hero=False):
        if not self.is_trader_active:
            [clot.move(self.hero, self.mainhero, self.weapons, Game, randrange(1, 7)) for clot in self.clots]
            [enemy.move() for enemy in self.enemies]
            [[self.coins.add(coin) for coin in enemy.get_coins()] for enemy in self.enemies]
            [coin.drop(self.mainhero) for coin in self.coins]
            self.available_tile.draw(self.screen)
            self.unavailable_tile.draw(self.screen)
            self.other_obj.draw(self.screen)
            self.trader.draw(self.screen)
            [elem.update(self.screen) for elem in self.enemy_visions]
            self.enemy_visions.draw(self.screen)
            self.enemies.draw(self.screen)
            self.clots.draw(self.screen)
            self.coins.draw(self.screen)
            [boss.move(self.hero, self.mainhero, self.params) for boss in self.boss]
            [egg.move(0, 0) for egg in self.eggs]
            [crack.update() for crack in self.cracks]

            if all([boss.is_die() for boss in self.boss]):
                [self.other_obj.add(boss.drop_crown()) for boss in self.boss]

            self.cracks.draw(self.screen)
            self.boss.draw(self.screen)
            self.eggs.draw(self.screen)

            if not without_hero:
                self.mainhero.draw(self.screen)
                pygame.draw.circle(self.screen, (101, 101, 101), (self.hero.get_coords()[0] + 19 / 2,
                                                                  self.hero.get_coords()[1] + 31 / 2),
                                   self.hero.get_range(), 1)
            [tip.draw(self.screen) for tip in self.tips]
            [boss.draw_hp_bar(self.screen) for boss in self.boss]

            for obj in self.other_obj:
                if obj.image == OTHER_OBJECTS["crown"]:
                    obj.is_crossing(self.hero, self.mainhero)

            if self.is_weapon_active:
                self.weapons.draw(self.screen)
        else:
            self.nearest_trader.draw_interface(self)

        self.draw_interface()

        if self.is_chosen[0]:
            self.nearest_trader.say(self.screen)

        if auto_update:
            pygame.display.flip()

    def start_screen(self):
        image, running = OTHER_OBJECTS["begin"], True
        Sound.play(SOUNDS["SOUNDTRACKS"]["start-menu"])
        Image.grow(self.screen, self.clock, image)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 772 <= event.pos[0] <= 832 and 249 <= event.pos[1] <= 271:
                        running = False
                    if 787 <= event.pos[0] <= 832 and 276 <= event.pos[1] <= 293:
                        terminate()

                self.screen.blit(image, (0, 0))
                pygame.display.flip()

            if not Sound.is_busy("bg-music"):
                Sound.play(SOUNDS["SOUNDTRACKS"]["start-menu"])

        Sound.stop("bg-music", 3000)
        Image.fade(self.screen, self.clock, image)

    def game_over(self):
        image, running = OTHER_OBJECTS["game_over"], True
        Sound.play(SOUNDS["GAME"]["game-over"])
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    Sound.stop("main", 1000)
                self.screen.blit(image, (0, 0))
                pygame.display.flip()

    def game_win(self):
        image, running = OTHER_OBJECTS["game_win"], True
        Image.grow(self.screen, self.clock, image)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    Sound.stop("main", 1000)
                self.screen.blit(image, (0, 0))
                pygame.display.flip()

        self.is_game_win = True

    def obj_move(self):
        for elem in self.shop:
            elem.move()

    def erase_cracks(self):
        [crack.kill() for crack in self.cracks]

    def change_tip(self):
        if self.tip_counter <= len(TIPS) - 1:
            self.tips = pygame.sprite.Group()
            self.tips.add(TIPS[self.tip_counter])
            self.tip_counter += 1
        else:
            self.tips = pygame.sprite.Group()

    def check_tile(self):
        av = un = tr = False
        if pygame.sprite.spritecollideany(self.hero, self.trader):
            tr = True
        elif pygame.sprite.spritecollideany(self.hero, self.available_tile):
            av = True
        elif pygame.sprite.spritecollideany(self.hero, self.unavailable_tile):
            un = True

        if tr and self.hero.last_tile != "trader":
            self.hero.set_last_tile("trader")
            pygame.event.post(pygame.event.Event(ON_CHANGE_TILE))
        elif av and self.hero.last_tile != "land":
            self.hero.set_last_tile("land")
            pygame.event.post(pygame.event.Event(ON_CHANGE_TILE))
        elif un and self.hero.last_tile != "water":
            self.hero.set_last_tile("water")
            pygame.event.post(pygame.event.Event(ON_CHANGE_TILE))

    def handle_sounds(self):
        is_not_gameplay_or_trader = self.now_playing not in ["gameplay", "trader"]
        is_not_trader = self.now_playing == "trader" and not self.is_trader_active
        is_not_enemies = not self.enemies and not self.boss

        if is_not_enemies and is_not_gameplay_or_trader or is_not_trader or self.now_playing is None:
            if Sound.overlay(SOUNDS["SOUNDTRACKS"]["gameplay"]):
                self.now_playing = "gameplay"
        if self.boss and self.now_playing != "boss-fight":
            if Sound.overlay(SOUNDS["SOUNDTRACKS"]["boss-fight"]):
                self.now_playing = "boss-fight"
        if self.enemies and not self.boss and self.now_playing != "fight":
            if Sound.overlay(SOUNDS["SOUNDTRACKS"]["fight"]):
                self.now_playing = "fight"
        if self.is_trader_active and self.now_playing != "trader":
            track = SOUNDS["SOUNDTRACKS"]["trader"]
            if self.hero.get_with_crown():
                track = SOUNDS["SOUNDTRACKS"]["happy-end"]
            if Sound.overlay(track):
                self.now_playing = "trader"

        if not Sound.is_busy("bg-music"):
            self.now_playing = None

        return self.now_playing

    def start(self):
        self.run_schedule_actions()
        while True:
            self.start_screen()
            self.loop()
            self.__init__()

    def run_schedule_actions(self):
        schedule.every(2).to(5).seconds.do(self.enemy_move)
        schedule.every(0.5).seconds.do(self.obj_move)
        schedule.every(15).seconds.do(self.change_tip)
        schedule.every(5).seconds.do(self.erase_cracks)

    def loop(self):
        group = self.available_tile, self.unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, \
                self.trader, self.clots, self.chunk, self.coins, self.boss, self.eggs, self.cracks
        self.field[self.cur_y][self.cur_x] = group

        first_start = True
        event = None

        while self.hero.is_alive() and not self.is_game_win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                keys = pygame.key.get_pressed()

                if event.type == ON_CHANGE_TILE and self.hero.last_tile == "trader":
                    Animator.hut_entrance(self.hero, self.draw_sprites, self.nearest_trader)
                    self.is_trader_active = True

                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE] and self.is_trader_active:
                        self.is_trader_active = False

                    if keys[pygame.K_e] and self.is_trader_active and self.is_chosen[0]:
                        self.nearest_trader.sell(self.hero, self.is_chosen[-1])

                    if keys[pygame.K_LSHIFT]:
                        if not self.is_trader_active and self.hero.get_move() and self.hero.get_stamina()[1] > 20:
                            self.hero.set_flag(True)
                            pygame.event.post(pygame.event.Event(ON_CHANGE_HERO_SPEED))
                        else:
                            self.hero.set_flag(False)
                            pygame.event.post(pygame.event.Event(ON_CHANGE_HERO_SPEED))

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.hero.set_flag(False)
                        pygame.event.post(pygame.event.Event(ON_CHANGE_HERO_SPEED))

                if not self.is_trader_active:
                    self.hero.move(event)

                if self.is_trader_active:
                    self.nearest_trader.draw_interface(self)

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if self.nearest_trader.get_text() == FINAL_SPEECH[-1] and self.hero.get_with_crown():
                            self.hero.with_crown = False
                            self.game_win()

                        elif self.nearest_trader.get_text() == SPEECH[-1] and self.is_first_time_at_merchant:
                            self.is_first_time_at_merchant = False
                            self.is_trader_active = False
                            self.nearest_trader.speech_counter = 0

                        elif self.is_trader_active:

                            for elem in self.shop:
                                if elem.check(event.pos):
                                    self.nearest_trader.set_text(obj=elem, first_time=self.is_first_time_at_merchant,
                                                                 last_time=self.hero.get_with_crown())
                                    self.is_chosen = [True, self.nearest_trader.get_text(), elem]
                                    self.nearest_trader.say(self.screen)
                                    break
                                else:
                                    self.is_chosen = [False, self.nearest_trader.get_text(), elem]
                            self.nearest_trader.reset_flag(False)
                    else:
                        self.nearest_trader.reset_flag(True)
                else:
                    self.is_chosen = [False, self.nearest_trader.get_text(), None]

                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    if self.hero.check(event.pos) and not self.is_trader_active:
                        self.is_weapon_active = True
                        pygame.mouse.set_visible(False)
                    else:
                        self.is_weapon_active = False
                        pygame.mouse.set_visible(True)

                    if self.is_weapon_active:
                        for elem in self.weapons:
                            self.is_weapon_active = elem.move(*event.pos, *event.rel, self.hero, self.enemies,
                                                              self.boss,
                                                              self.is_weapon_active)
                        for elem in self.weapons:
                            self.is_weapon_active = elem.move(*event.pos, *event.rel, self.hero, self.eggs, self.boss,
                                                              self.is_weapon_active)

            if self.hero.current_stamina > 5 and self.hero.get_running():
                self.hero.current_stamina -= 5
            if self.hero.current_stamina < 5 and self.hero.get_running():
                self.hero.set_flag(False)
                pygame.event.post(pygame.event.Event(ON_CHANGE_HERO_SPEED))

            self.check_tile()
            self.handle_sounds()

            self.is_someone_angry = any([enemy.is_angry() for enemy in self.enemies])
            self.is_boss_angry = any([boss.get_angry() for boss in self.boss])

            if event:
                self.hero.animation(event)

            x, y = self.hero.get_coords()

            if ((TILES_COUNT_X * TILE_WIDTH - 5 <= x or x <= 5 or TILES_COUNT_Y * TILE_HEIGHT - 5 <= y or y <= 5)
                    and not self.is_someone_angry and not self.is_boss_angry and not self.is_first_time_at_merchant):

                if TILES_COUNT_X * TILE_WIDTH - 5 <= x:
                    self.cur_x += 1

                if x <= 5:
                    self.cur_x -= 1

                if TILES_COUNT_Y * TILE_HEIGHT - 5 <= y:
                    self.cur_y += 1

                if y <= 5:
                    self.cur_y -= 1

                self.cur_x = FIELD_SIZE_X - 1 if self.cur_x < 0 else self.cur_x
                self.cur_y = FIELD_SIZE_Y - 1 if self.cur_y < 0 else self.cur_y
                self.cur_x = 0 if self.cur_x >= FIELD_SIZE_X else self.cur_x
                self.cur_y = 0 if self.cur_y >= FIELD_SIZE_Y else self.cur_y

                if self.field[self.cur_y][self.cur_x] is None:
                    self.chunk, self.other_obj = self.generate()
                    self.available_tile, self.unavailable_tile = self.render_map(self.chunk)
                    self.enemy_visions = pygame.sprite.Group()
                    self.enemies = pygame.sprite.Group()
                    self.trader = pygame.sprite.Group()
                    self.clots = pygame.sprite.Group()
                    self.coins = pygame.sprite.Group()
                    self.cracks = pygame.sprite.Group()
                    self.eggs = pygame.sprite.Group()

                    self.params = {
                        "hero": self.hero,
                        "chunk": self.chunk,
                        "hero_group": self.mainhero,
                        "available_tile": self.available_tile,
                        "enemy_visions": self.enemy_visions,
                        "clots": self.clots,
                        "screen": self.screen,
                        "game": Game,
                        "egg_group": self.eggs,
                        "crack_group": self.cracks
                    }

                    if self.cur_y == 0 and self.cur_x == 0 and self.boss != pygame.sprite.Group():
                        self.boss.add(Boss([300, 300], self.params))
                    else:
                        self.boss = pygame.sprite.Group()

                    for _ in range(randrange(10, 15)):
                        self.enemies.add(
                            Slime("name", "regular", 10, 200, 2, randrange(1, 11), randrange(10, 21), self.params))

                    for _ in range(randrange(10, 15)):
                        self.params["game"] = Game
                        self.enemies.add(
                            ExpSlime("name", "explosion", 40, 100, 10, randrange(15, 26), randrange(20, 31),
                                     self.params))

                    self.field[self.cur_y][
                        self.cur_x] = self.available_tile, self.unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, self.trader, self.clots, self.chunk, self.coins, self.boss, self.eggs, self.cracks
                else:
                    if self.cur_y != 0 and self.cur_x != 0:
                        self.boss = pygame.sprite.Group()

                    self.available_tile, self.unavailable_tile, self.other_obj, self.enemies, self.enemy_visions, self.trader, self.clots, self.chunk, self.coins, self.boss, self.eggs, self.cracks = \
                        self.field[self.cur_y][self.cur_x]

            if TILES_COUNT_X * TILE_WIDTH - 5 <= self.hero.get_coords()[0]:
                self.hero.set_coords(5, self.hero.get_coords()[1])

            elif self.hero.get_coords()[0] <= 5:
                self.hero.set_coords(TILES_COUNT_X * TILE_WIDTH - 5, self.hero.get_coords()[1])

            if TILES_COUNT_Y * TILE_HEIGHT - 5 <= self.hero.get_coords()[1]:
                self.hero.set_coords(self.hero.get_coords()[0], 5)

            elif self.hero.get_coords()[1] <= 5:
                self.hero.set_coords(self.hero.get_coords()[0], TILES_COUNT_Y * TILE_HEIGHT - 5)

            schedule.run_pending()
            self.hero.heal()

            if not first_start:
                self.draw_sprites()

            self.mainhero.update()

            if self.hero.get_stamina()[1] <= 0:
                self.hero.set_flag(False)
                pygame.event.post(pygame.event.Event(ON_CHANGE_HERO_SPEED))

            if first_start:
                Image.alt_fade(self.screen, self.clock, self.draw_sprites)
                first_start = False

            self.clock.tick(30)
