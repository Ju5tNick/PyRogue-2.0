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
        params = CHANNELS_PARAMS[track["channel"]]

        if type(path) != str:
            path = path[random.randint(0, len(path) - 1)]

        params["path"] = path
        params["channel"] = track["channel"]
        params["force"] = force

        if track["channel"] == "bg-music":
            return Sound.__play_music(params)
        return Sound.__play_sound(params)

    @staticmethod
    def stop(channel, fade=0):
        if channel == "bg-music":
            pygame.mixer.music.fadeout(fade)
        else:
            ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
            ch.fadeout(fade)

    @staticmethod
    def stop_all_channels():
        for ch_name in CHANNELS_PARAMS:
            ch = pygame.mixer.Channel(CHANNELS_PARAMS[ch_name]["id"])
            ch.stop()
        pygame.mixer.music.stop()

    @staticmethod
    def is_busy(channel):
        if channel == "bg-music":
            return pygame.mixer.music.get_busy()
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        return ch.get_busy()

    @staticmethod
    def __play_music(params):
        if pygame.mixer.music.get_busy() and not params["force"]:
            return False

        pygame.mixer.music.load(params["path"])
        pygame.mixer.music.set_volume(params["volume"])
        pygame.mixer.music.play(-1)
        return True

    @staticmethod
    def __play_sound(params):
        file = pygame.mixer.Sound(params["path"])
        if params["channel"] == "main":
            ch = pygame.mixer.find_channel()
        else:
            ch = pygame.mixer.Channel(params["id"])
        if (not ch or ch.get_busy()) and not params["force"]:
            return False
        ch.set_volume(params["volume"])
        ch.play(file, loops=params["loops"])
        return True
