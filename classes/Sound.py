import pygame


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
    def sound(filename, volume=0.5, repeat=1):
        s = pygame.mixer.Sound(filename)
        s.set_volume(volume)
        s.play(loops=repeat)

    # @staticmethod
    # def pause_sound():
    #     pygame.mixer.Sound.stop()
