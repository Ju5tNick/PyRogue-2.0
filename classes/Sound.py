import random
import pygame

from helpers.sounds import CHANNELS_PARAMS


class Sound:
    @staticmethod
    def play(track):
        path = track["path"]

        if type(path) != str:
            path = path[random.randint(0, len(path) - 1)]

        file = pygame.mixer.Sound(path)
        params = CHANNELS_PARAMS[track["channel"]]
        ch = pygame.mixer.Channel(params["id"])
        ch.set_volume(params["volume"])
        ch.play(file, loops=params["loops"])

    @staticmethod
    def stop(channel, fade=0):
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        ch.fadeout(fade)

    @staticmethod
    def stop_all_channels():
        for ch_name in CHANNELS_PARAMS:
            ch = pygame.mixer.Channel(CHANNELS_PARAMS[ch_name]["id"])
            ch.stop()
