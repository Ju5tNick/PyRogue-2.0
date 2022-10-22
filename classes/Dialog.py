import pygame
import time

from classes.Sound import Sound
from helpers.images import DIALOG_BAR
from helpers.sounds import SOUNDS


class Dialog(pygame.sprite.Sprite):
    image = DIALOG_BAR

    def __init__(self):
        super().__init__(pygame.sprite.Group())
        self.rect = pygame.Rect(50, 380, 900, 100)
        self.mask = pygame.mask.from_surface(self.image)

    def dialog(self, screen, text, is_slow):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        if is_slow:
            Sound.play(SOUNDS["CONTEXT"]["allow"])
            self.x = 0
            for i, letter in enumerate(text):
                message = pygame.font.Font(None, 25).render(letter, True, (0, 0, 0))
                screen.blit(message, (70 + self.x, 400))
                self.x += message.get_width()
                pygame.display.flip()
                time.sleep(0.002)
        else:
            screen.blit(pygame.font.Font(None, 25).render(text, True, (0, 0, 0)), (70, 400))

