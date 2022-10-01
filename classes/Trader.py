import pygame

from random import randint

from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_X, TILES_COUNT_Y
from helpers.images import TRADER_SETS


class Trader(pygame.sprite.Sprite):
    image = TRADER_SETS["image"]

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.trader_sets = TRADER_SETS
        self.rect = pygame.Rect(TILES_COUNT_X * TILE_WIDTH / 2 - 200, TILES_COUNT_Y * TILE_HEIGHT / 2 - 150, 400, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.trades = []  # (price, eff_type, eff_value, stock)
        for i in range(20):
            price = randint(10, 100)
            eff_type = randint(0, 1)
            eff_value = int(price / 5 / (eff_type + 1))
            stock = int(30 / (eff_type + 1) / eff_value)
            self.trades.append([price, eff_type, eff_value, stock])

    def sell(self, mainhero, obj, sound):
        if mainhero.get_balance() - obj.get_cost() >= 0 and obj.get_cost() != 0:
            sound("assets/sounds/buy.wav")
            mainhero.buy(obj.get_cost())

    def get_trades(self):
        return self.trades

    def check(self, mainhero):
        return pygame.sprite.spritecollideany(self, mainhero)  # возвращает булевый тип(пересеклись ли спрайты)

    def draw_interface(self, game):
        pygame.mouse.set_visible(True)
        game.background.draw(game.screen)
        game.shop.draw(game.screen)

    def say(self, obj, screen):
        screen.blit(pygame.font.Font(None, 25).render(obj.get_info(), True, (255, 255, 255)), (50, 44))
