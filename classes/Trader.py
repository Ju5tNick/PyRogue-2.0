import pygame

from classes.Sound import Sound
from helpers.config import TILE_WIDTH, TILE_HEIGHT, TILES_COUNT_X, TILES_COUNT_Y
from helpers.images import TRADER_SETS, POTIONS, MERCHANT_PHRASES
from classes.Object import Object
from classes.Dialog import Dialog
from helpers.sounds import SOUNDS
from helpers.trader_speech import *


class Trader(pygame.sprite.Sprite):
    image = TRADER_SETS["image"]

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.trader_sets = TRADER_SETS
        self.rect = pygame.Rect(TILES_COUNT_X * TILE_WIDTH / 2 - 200, TILES_COUNT_Y * TILE_HEIGHT / 2 - 180, 160, 130)
        self.mask = pygame.mask.from_surface(self.image)
        self.trades = []
        self.is_said = True
        self.dialog = Dialog()
        self.text = ""
        self.speech_counter = 0
        for i, potion in enumerate(POTIONS):
            if i <= 1:
                self.trades.append(
                    Object(
                        POTIONS[potion]["image"], [650 + i * 22, 278], [21, 21], True, effect=POTIONS[potion]["effect"],
                        info=POTIONS[potion]["info"], cost=POTIONS[potion]["cost"],
                        ef_value=POTIONS[potion]["ef_value"],
                        required_lvl=POTIONS[potion]["required_lvl"]
                    ))
            else:
                self.trades.append(
                    Object(
                        POTIONS[potion]["image"], [520 + i * 20, 215], [21, 21], True, effect=POTIONS[potion]["effect"],
                        info=POTIONS[potion]["info"], cost=POTIONS[potion]["cost"],
                        ef_value=POTIONS[potion]["ef_value"],
                        required_lvl=POTIONS[potion]["required_lvl"]
                    ))

    def sell(self, mainhero, obj):
        effects = {"damage": mainhero.add_damage, "stamina": mainhero.add_stamina, "health": mainhero.add_hp}
        if (mainhero.get_balance() - obj.get_cost() >= 0 and obj.get_cost() != 0 and
                mainhero.get_ex()[2] >= obj.get_lvl()):
            Sound.play(SOUNDS["CONTEXT"]["allow"])
            effects[obj.get_effect()](obj.get_ef_value())
            mainhero.buy(obj.get_cost())

        elif mainhero.get_ex()[2] < obj.get_lvl():
            Sound.play(SOUNDS["CONTEXT"]["deny"])
            self.set_text(MERCHANT_PHRASES["dont_selling"])
            self.reset_flag(False)

        elif obj.get_info() != MERCHANT_PHRASES["irritaion"]:
            Sound.play(SOUNDS["CONTEXT"]["deny"])
            self.set_text(MERCHANT_PHRASES["no_money"])
            self.reset_flag(False)

    def reset_flag(self, value):
        self.is_said = value

    def set_text(self, text="", obj=None, first_time=False, last_time=False):
        if first_time:
            if self.speech_counter < len(SPEECH):
                self.text = SPEECH[self.speech_counter]
                self.speech_counter += 1

        elif last_time:
            if self.speech_counter < len(FINAL_SPEECH):
                self.text = FINAL_SPEECH[self.speech_counter]
                self.speech_counter += 1

        else:    
            if obj is not None:
                self.text = obj.get_info()
            elif text != "":
                self.text = text
            self.speech_counter = 0

    def get_text(self):
        return self.text

    def get_trades(self):
        return self.trades

    def check(self, mainhero):
        return pygame.sprite.spritecollideany(self, mainhero)

    def draw_interface(self, game):
        pygame.mouse.set_visible(True)
        game.background.draw(game.screen)
        game.shop.draw(game.screen)

    def say(self, screen):
        if self.is_said:
            self.dialog.dialog(screen, self.text, False)
        else:
            self.dialog.dialog(screen, self.text, True)
            self.reset_flag(True)
