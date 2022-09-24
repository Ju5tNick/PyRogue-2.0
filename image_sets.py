import os
import sys
import pygame



def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    return pygame.image.load(name)


hero_sets = {

	"still": {
            "up": load_image("data/images/mainhero/knight11.png"),
            "down": load_image("data/images/mainhero/knight2.png"),
            "left": load_image("data/images/mainhero/knight5.png"),
            "right": load_image("data/images/mainhero/knight8.png")
            },

    "directions": {
            "up": [load_image("data/images/mainhero/knight9.png"), load_image("data/images/mainhero/knight10.png")],
            "down": [load_image("data/images/mainhero/knight0.png"), load_image("data/images/mainhero/knight1.png")],
            "left": [load_image("data/images/mainhero/knight3.png"), load_image("data/images/mainhero/knight4.png")],
            "right": [load_image("data/images/mainhero/knight7.png"), load_image("data/images/mainhero/knight6.png")]
            },

    "hero_image": load_image("data/images/mainhero/knight2.png")

}


weapon_sets = {

	"default_image": load_image("data/images/sword/sword.png"),
	"image": load_image("data/images/sword/sword.png")

}

enemy_sets = {

	"still": [load_image("data/images/enemies/slime/static/0.png"), load_image("data/images/enemies/slime/static/1.png"),
              load_image("data/images/enemies/slime/static/2.png"), load_image("data/images/enemies/slime/static/3.png"),
              load_image("data/images/enemies/slime/static/4.png"), load_image("data/images/enemies/slime/static/5.png"),
              load_image("data/images/enemies/slime/static/6.png")],

    "moves": [load_image("data/images/enemies/slime/move/0.png"), load_image("data/images/enemies/slime/move/1.png"),
              load_image("data/images/enemies/slime/move/2.png"), load_image("data/images/enemies/slime/move/3.png"),
              load_image("data/images/enemies/slime/move/4.png"), load_image("data/images/enemies/slime/move/5.png"),
              load_image("data/images/enemies/slime/move/6.png"), load_image("data/images/enemies/slime/move/7.png")],

    "angry_moves": [load_image("data/images/enemies/slime/angry_move/0.png"), load_image("data/images/enemies/slime/angry_move/1.png")],

    "gets_angry": [load_image("data/images/enemies/slime/gets_angry/0.png"), load_image("data/images/enemies/slime/gets_angry/1.png"),
                   load_image("data/images/enemies/slime/gets_angry/2.png"), load_image("data/images/enemies/slime/gets_angry/3.png"),
                   load_image("data/images/enemies/slime/gets_angry/4.png")],

    "die_animation": [load_image("data/images/enemies/slime/die/0.png"), load_image("data/images/enemies/slime/die/1.png"),
                      load_image("data/images/enemies/slime/die/2.png"), load_image("data/images/enemies/slime/die/3.png"),
                      load_image("data/images/enemies/slime/die/4.png"), load_image("data/images/enemies/slime/die/5.png")],

    "attack_animation": [load_image("data/images/enemies/slime/attack/0.png"), load_image("data/images/enemies/slime/attack/1.png"),
                         load_image("data/images/enemies/slime/attack/2.png"), load_image("data/images/enemies/slime/attack/3.png"),
                         load_image("data/images/enemies/slime/attack/4.png"), load_image("data/images/enemies/slime/attack/5.png"),
                         load_image("data/images/enemies/slime/attack/0.png"), load_image("data/images/enemies/slime/attack/1.png")],

    "image": load_image("data/images/enemies/slime/static/0.png"),
    "clot": load_image("data/images/objects/slimes_clot.png")

}

trader_sets = {

	"dishes": [load_image("data/images/objects/watermelon.png"), load_image("data/images/objects/fish.png"),
              load_image("data/images/objects/mushroom.png"), load_image("data/images/objects/corn.png")],

    "weapons_logo": [load_image("data/images/objects/potion1.png"), load_image("data/images/objects/potion2.png"),
                    load_image("data/images/objects/dagger.png"), load_image("data/images/objects/potion3.png")],

    "image": load_image("data/images/trader/0.png")

}

other_objects = {
	
	"logo": load_image("data/images/objects/logo.png"),
	"game_over": load_image("data/images/objects/game_over.jpg"),
	"chest": load_image("data/images/objects/chest.png"),
	"shield": load_image("data/images/objects/shield.png"),
	"label": load_image("data/images/objects/label.png"),
	"trader": load_image("data/images/trader/trader.png"),
	"begin": load_image("data/images/objects/begin.png"),
	"coin": load_image("data/images/objects/coin.png"),
	"heart": load_image("data/images/objects/heart.png"),
	"tall_grass": load_image(f"data/images/objects/tall_grass.png"),
	"water_lily": load_image(f"data/images/objects/water_lily.png")  

}

