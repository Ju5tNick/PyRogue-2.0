import pygame

from helpers.config import TILES_COUNT_X, TILE_WIDTH, TILES_COUNT_Y, TILE_HEIGHT


class Image:

    @staticmethod
    def change_alpha(orig_surf, alpha):
        surf = orig_surf.copy()
        alpha_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, alpha))
        surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return surf

    @staticmethod
    def grow(screen, clock, image, skip=True):
        done, alpha = False, 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and skip):
                    done = True
            if alpha < 255:
                alpha += 2
                alpha = min(255, alpha)
                surf = Image.change_alpha(image, alpha)
            else:
                done = True

            screen.fill((0, 0, 0))
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            clock.tick(30)

    @staticmethod
    def fade(screen, clock, image, skip=True):
        done, alpha = False, 255
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and skip):
                    done = True
            if alpha > 0:
                alpha -= 2
                alpha = max(0, alpha)
                surf = Image.change_alpha(image, alpha)
            else:
                done = True

            screen.fill((0, 0, 0))
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            clock.tick(30)

    @staticmethod
    def alt_fade(screen, clock, callback_draw, skip=True):
        done, alpha = False, 255

        s = pygame.Surface((TILES_COUNT_X * TILE_WIDTH, TILES_COUNT_Y * TILE_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, alpha))  # notice the alpha value in the color

        while not done:
            for event in pygame.event.get():
                possible_events = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]
                if event.type == pygame.QUIT or (event.type in possible_events and skip):
                    done = True
            if alpha > 0:
                alpha -= 4
                alpha = max(0, alpha)
                s.fill((0, 0, 0, alpha))
            else:
                done = True

            callback_draw(auto_update=False)
            screen.blit(s, (0, 0))
            pygame.display.flip()
            clock.tick(30)
