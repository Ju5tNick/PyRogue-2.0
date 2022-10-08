import pygame

from random import randint

from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_X, TILES_COUNT_Y
from helpers.images import TRADER_SETS, POTIONS
from classes.Object import Object
from classes.Dialog import Dialog


class Trader(pygame.sprite.Sprite):
    image = TRADER_SETS["image"]

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.trader_sets = TRADER_SETS
        self.rect = pygame.Rect(TILES_COUNT_X * TILE_WIDTH / 2 - 200, TILES_COUNT_Y * TILE_HEIGHT / 2 - 150, 400, 300)
        self.mask = pygame.mask.from_surface(self.image)
        self.trades = []
        self.is_said = True
        self.dialog = Dialog()
        for i, potion in enumerate(POTIONS):
            if i <= 1:
                self.trades.append(
                    Object(
                    POTIONS[potion]["image"], [650 + i * 22, 278], [21, 21], True, effect=POTIONS[potion]["effect"], 
                    info=POTIONS[potion]["info"], cost=POTIONS[potion]["cost"], ef_value=POTIONS[potion]["ef_value"]
                    ))
            else:
                self.trades.append(
                    Object(
                    POTIONS[potion]["image"], [520 + i * 20, 215], [21, 21], True, effect=POTIONS[potion]["effect"], 
                    info=POTIONS[potion]["info"], cost=POTIONS[potion]["cost"], ef_value=POTIONS[potion]["ef_value"]
                    ))

    def sell(self, mainhero, obj, sound, screen):
        effects = {"damage": mainhero.add_damage, "stamina": mainhero.add_stamina, "health": mainhero.add_hp}
        if type(obj) == str:
            self.say(screen, text="Маловато у тебя деньжат. Возвращайся, как поднакопишь больше")
        elif mainhero.get_balance() - obj.get_cost() >= 0 and obj.get_cost() != 0:
            sound("assets/sounds/buy.wav")
            effects[obj.get_effect()](obj.get_ef_value())
            mainhero.buy(obj.get_cost())
            

    def reset_flag(self, value):
        self.is_said = value

    def get_trades(self):
        return self.trades

    def check(self, mainhero):
        return pygame.sprite.spritecollideany(self, mainhero)  # возвращает булевый тип(пересеклись ли спрайты)

    def draw_interface(self, game):
        pygame.mouse.set_visible(True)
        game.background.draw(game.screen)
        game.shop.draw(game.screen)

    def say(self, screen, text="", obj=None):
        if obj == None:
            text = text
        else:
            text = obj.get_info()
            
        if self.is_said:
            self.dialog.dialog(screen, text, False)
        else:
            self.dialog.dialog(screen, text, True)
            self.is_said = True
        return (True, text)
