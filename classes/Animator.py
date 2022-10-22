import pygame

from classes.Sound import Sound
from helpers.common import terminate
from helpers.images import TRADER_SETS
from helpers.sounds import SOUNDS


class Animator:

    @staticmethod
    def handle_quiet_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

    @staticmethod
    def hut_entrance(hero, draw_sprites, trader):
        hero.stop()
        hero.pos = 378, 240
        hero.update()
        hero.image = hero.hero_sets["still"]["up"]

        Sound.stop("bg-music", 3000)
        event = None

        hero.vel.y = -0.2
        for _ in range(100):
            Animator.handle_quiet_event()
            hero.animation(event)
            hero.update()
            draw_sprites()

        hero.stop()
        Sound.play(SOUNDS["TRADER"]["open-door"])
        trader.image = TRADER_SETS["huts"]["open"]

        for _ in range(100):
            Animator.handle_quiet_event()
            draw_sprites()

        Sound.play(SOUNDS["CONTEXT"]["jump"])
        draw_sprites(without_hero=True)

        for _ in range(100):
            Animator.handle_quiet_event()
            draw_sprites(without_hero=True)

        Sound.play(SOUNDS["TRADER"]["close-door"])
        trader.image = TRADER_SETS["huts"]["close"]
        draw_sprites(without_hero=True)

        for _ in range(100):
            Animator.handle_quiet_event()
            draw_sprites(without_hero=True)
