import pygame

from classes.Tips import Tip


'''
parser = argparse.ArgumentParser()
parser.add_argument("data", nargs="*", default=[])
parser.add_argument("--negative", type=int, default=-1, nargs="?")
parser.add_argument("--largest", type=int, default=100, nargs="?")
args = parser.parse_args()
print(args)
'''

pygame.init()

tip = Tip("чтобы ходить, идите прямо и вниз, а также можете налево и направо")

print(*tip.tip)
print(tip.size)