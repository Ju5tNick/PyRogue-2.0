import pygame

from random import randint

from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_X, TILES_COUNT_Y
from helpers.images import TRADER_SETS, POTIONS
from classes.Object import Object


class Trader(pygame.sprite.Sprite):
    image = TRADER_SETS["image"]
    getters = {}

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.trader_sets = TRADER_SETS
        self.rect = pygame.Rect(TILES_COUNT_X * TILE_WIDTH / 2 - 200, TILES_COUNT_Y * TILE_HEIGHT / 2 - 150, 400, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.trades = []  # (price, eff_type, eff_value, stock)
        for i, potion in enumerate(POTIONS):
            self.trades.append(
                Object(
                POTIONS[potion][0], [650 + i * 22, 278], [21, 21], True, effect=POTIONS[potion][-2], 
                info=POTIONS[potion][1], cost=POTIONS[potion][-3], ef_value=POTIONS[potion][-1]
                ))

    def sell(self, mainhero, obj, sound):
        effects = {"damage": mainhero.add_damage, "stamina": mainhero.add_stamina, "health": mainhero.add_hp}
        if mainhero.get_balance() - obj.get_cost() >= 0 and obj.get_cost() != 0:
            sound("assets/sounds/buy.wav")
            effects[obj.get_effect()](obj.get_ef_value())
            mainhero.buy(obj.get_cost())

    def get_trades(self):
        return self.trades

    def check(self, mainhero):
        return pygame.sprite.spritecollideany(self, mainhero)  # возвращает булевый тип(пересеклись ли спрайты)

    def draw_interface(self, game):
        pygame.mouse.set_visible(True)
        game.background.draw(game.screen)
        game.shop.draw(game.screen)

    def say(self, screen, text="", obj=None):
        text = str(obj.get_info()) if text == "" else text 
        screen.blit(pygame.font.Font(None, 25).render(text, True, (255, 255, 255)), (50, 44))
