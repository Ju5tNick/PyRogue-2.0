import os
import sys
import pygame


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    return pygame.image.load(name)


IMAGES_BASE_PATH = "assets/images/"

HERO_SETS = {
    "still": {
        "up": load_image(IMAGES_BASE_PATH + "mainhero/still/up.png"),
        "down": load_image(IMAGES_BASE_PATH + "mainhero/still/down.png"),
        "left": load_image(IMAGES_BASE_PATH + "mainhero/still/left.png"),
        "right": load_image(IMAGES_BASE_PATH + "mainhero/still/right.png"),
    },
    "move": {
        "up": [load_image(IMAGES_BASE_PATH + "mainhero/move/up/0.png"),
               load_image(IMAGES_BASE_PATH + "mainhero/move/up/1.png")],
        "down": [load_image(IMAGES_BASE_PATH + "mainhero/move/down/0.png"),
                 load_image(IMAGES_BASE_PATH + "mainhero/move/down/1.png")],
        "left": [load_image(IMAGES_BASE_PATH + "mainhero/move/left/0.png"),
                 load_image(IMAGES_BASE_PATH + "mainhero/move/left/1.png")],
        "right": [load_image(IMAGES_BASE_PATH + "mainhero/move/right/0.png"),
                  load_image(IMAGES_BASE_PATH + "mainhero/move/right/1.png")],
    },
    "image": load_image(IMAGES_BASE_PATH + "mainhero/still/down.png"),
}

WEAPON_SETS = {
    "sword": load_image(IMAGES_BASE_PATH + "weapons/sword.png"),
}

SLIME_SETS = {
    "still": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/1.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/2.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/3.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/4.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/5.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/static/6.png"),
    ],

    "move": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/1.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/2.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/3.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/4.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/5.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/6.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/move/7.png"),
    ],

    "angry_move": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/angry_move/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/angry_move/1.png"),
    ],

    "gets_angry": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/gets_angry/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/gets_angry/1.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/gets_angry/2.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/gets_angry/3.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/gets_angry/4.png"),
    ],

    "die_animation": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/1.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/2.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/3.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/4.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/die/5.png"),
    ],

    "attack_animation": [
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/1.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/2.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/3.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/4.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/5.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/0.png"),
        load_image(IMAGES_BASE_PATH + "enemies/slime/attack/1.png"),
    ],

    "image": load_image(IMAGES_BASE_PATH + "enemies/slime/static/0.png"),
    "clot": load_image(IMAGES_BASE_PATH + "enemies/slime/slimes_clot.png"),
}

TRADER_SETS = {
    "dishes": [
        load_image(IMAGES_BASE_PATH + "objects/watermelon.png"),
        load_image(IMAGES_BASE_PATH + "objects/fish.png"),
        load_image(IMAGES_BASE_PATH + "objects/mushroom.png"),
        load_image(IMAGES_BASE_PATH + "objects/corn.png"),
    ],

    "weapons_logo": [
        load_image(IMAGES_BASE_PATH + "objects/potion1.png"),
        load_image(IMAGES_BASE_PATH + "objects/potion2.png"),
        load_image(IMAGES_BASE_PATH + "objects/dagger.png"),
        load_image(IMAGES_BASE_PATH + "objects/potion3.png"),
    ],

    "image": load_image(IMAGES_BASE_PATH + "trader/0.png"),
}

OTHER_OBJECTS = {
    "logo": load_image(IMAGES_BASE_PATH + "objects/logo.png"),
    "game_over": load_image(IMAGES_BASE_PATH + "objects/game_over.jpg"),
    "chest": load_image(IMAGES_BASE_PATH + "objects/chest.png"),
    "shield": load_image(IMAGES_BASE_PATH + "objects/shield.png"),
    "label": load_image(IMAGES_BASE_PATH + "objects/label.png"),
    "trader": load_image(IMAGES_BASE_PATH + "trader/trader.png"),
    "begin": load_image(IMAGES_BASE_PATH + "objects/begin.png"),
    "coin": load_image(IMAGES_BASE_PATH + "objects/coin.png"),
    "heart": load_image(IMAGES_BASE_PATH + "objects/heart.png"),
    "tall_grass": load_image(IMAGES_BASE_PATH + "objects/tall_grass.png"),
    "water_lily": load_image(IMAGES_BASE_PATH + "objects/water_lily.png"),
    "merchant": [load_image(IMAGES_BASE_PATH + "trader/trader2.png"), "Не надо на меня тыкать!"],
    "background": [load_image(IMAGES_BASE_PATH + "trader/ocr.jpg"), ""],
    "rock": [
        load_image(IMAGES_BASE_PATH + "objects/rock1.png"),
        load_image(IMAGES_BASE_PATH + "objects/rock2.png")
    ],
}

POTIONS = {
    "potion1": [
        load_image(IMAGES_BASE_PATH + "objects/potion1.png"),
        "Зеленое зелье ... Цена: 10 Купить? (Y/N)",
        10,
    ],
    "potion2": [
        load_image(IMAGES_BASE_PATH + "objects/potion2.png"),
        "Синее зелье ... Цена: 15 Купить? (Y/N)",
        15,
    ],
    "potion3": [
        load_image(IMAGES_BASE_PATH + "objects/potion3.png"),
        "Красное зелье ... Цена: 20 Купить? (Y/N)",
        20,
    ],
}
