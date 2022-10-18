import pygame

from helpers.sounds import CHANNELS_PARAMS


class Sound:
    @staticmethod
    def music(filename, volume=0.5, repeat=1):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(repeat)

    @staticmethod
    def pause_music(fade=0):
        pygame.mixer.music.fadeout(fade)

    @staticmethod
    def sound(filename, channel, volume=0.5, repeat=1):
        file = pygame.mixer.Sound(filename)
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        ch.set_volume(volume)
        ch.play(file, loops=repeat)
        # s = pygame.mixer.Sound(filename)
        # s.set_volume(volume)
        # s.play(loops=repeat)

    @staticmethod
    def pause_sound(channel, fade=0):
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        ch.fadeout(fade)

    @staticmethod
    def play(track):
        file = pygame.mixer.Sound(track["path"])
        params = CHANNELS_PARAMS[track["channel"]]
        ch = pygame.mixer.Channel(params["id"])
        ch.set_volume(params["volume"])
        ch.play(file, loops=params["loops"])

    @staticmethod
    def pause(channel, fade=0):
        ch = pygame.mixer.Channel(CHANNELS_PARAMS[channel]["id"])
        ch.fadeout(fade)
