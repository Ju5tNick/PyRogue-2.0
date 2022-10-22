import random
import pygame

from helpers.sounds import CHANNELS_PARAMS


class Sound:
    @staticmethod
    def overlay(track, overlay=1500):
        channel = track["channel"]
        Sound.stop(channel, overlay)
        if Sound.is_busy(channel):
            return False
        Sound.play(track)
        return True

    @staticmethod
    def play(track, force=False):
        path = track["path"]

        if type(path) != str:
            path = path[random.randint(0, len(path) - 1)]

        file = pygame.mixer.Sound(path)
        params = CHANNELS_PARAMS[track["channel"]]
        if track["channel"] == "main":
            ch = pygame.mixer.find_channel()
        else:
            ch = pygame.mixer.Channel(params["id"])
        if (not ch or ch.get_busy()) and not force:
            return False
        ch.set_volume(params["volume"])
        ch.play(file, loops=params["loops"])
        return True

    @staticmethod
    def stop(channel, fade=0):
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        ch.fadeout(fade)

    @staticmethod
    def stop_all_channels():
        for ch_name in CHANNELS_PARAMS:
            ch = pygame.mixer.Channel(CHANNELS_PARAMS[ch_name]["id"])
            ch.stop()

    @staticmethod
    def is_busy(channel):
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        return ch.get_busy()
