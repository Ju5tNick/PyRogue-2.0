from helpers.config import SOUND_MAIN_CHANNEL_VOLUME, SOUND_BG_MUSIC_CHANNEL_VOLUME, SOUND_MOVEMENT_CHANNEL_VOLUME

SOUNDS_BASE_PATH = "assets/sounds/"

CHANNELS_PARAMS = {
    "main": {
        "id": 0,
        "volume": SOUND_MAIN_CHANNEL_VOLUME,
        "loops": 0,
    },
    "bg-music": {
        "id": 1,
        "volume": SOUND_BG_MUSIC_CHANNEL_VOLUME,
        "loops": 0,
    },
    "movement": {
        "id": 2,
        "volume": SOUND_MOVEMENT_CHANNEL_VOLUME,
        "loops": -1,
    },
}

SOUNDS = {
    "SOUNDTRACKS": {
        "start-menu": {
            "path": SOUNDS_BASE_PATH + "soundtracks/start-menu.mp3",
            "channel": "bg-music",
        },
        "gameplay": {
            "path": [SOUNDS_BASE_PATH + f"soundtracks/gameplay/{i}.mp3" for i in range(1, 4)],
            "channel": "bg-music",
        },
        "fight": {
            "path": [SOUNDS_BASE_PATH + f"soundtracks/fight/{i}.mp3" for i in range(1, 4)],
            "channel": "bg-music",
        },
        "trader": {
            "path": SOUNDS_BASE_PATH + "soundtracks/trader.mp3",
            "channel": "bg-music",
        },
    },
    "GAME": {
        "game-over": {
            "path": SOUNDS_BASE_PATH + "game/game-over.mp3",
            "channel": "main",
        }
    },
    "HERO": {
        "hit": {
            "path": SOUNDS_BASE_PATH + "mainhero/hit.mp3",
            "channel": "main",
        },
        "pick-coins": {
            "path": SOUNDS_BASE_PATH + "mainhero/pick-coins.mp3",
            "channel": "main",
        },
        "step": {
            "path": SOUNDS_BASE_PATH + "mainhero/step.wav",
            "channel": "movement",
        },
        "step-in-water": {
            "path": SOUNDS_BASE_PATH + "mainhero/step-in-water.wav",
            "channel": "movement",
        },
        "run": {
            "path": SOUNDS_BASE_PATH + "mainhero/run.wav",
            "channel": "movement",
        },
        "run-in-water": {
            "path": SOUNDS_BASE_PATH + "mainhero/run-in-water.wav",
            "channel": "movement",
        },
    },
    # "TRADER": {
    #     "buy-item": {
    #         "path": SOUNDS_BASE_PATH + "trader/buy-item.wav",
    #         "channel": "main",
    #     },
    # },
    "ENEMY": {
        "death": {
            "path": SOUNDS_BASE_PATH + "enemy/death.wav",
            "channel": "main",
        },
        "exp-death": {
            "path": SOUNDS_BASE_PATH + "enemy/exp-death.wav",
            "channel": "main",
        },
        "hit": {
            "path": SOUNDS_BASE_PATH + "enemy/hit.mp3",
            "channel": "main",
        },
    },
    "CONTEXT": {
        "context": {
            "path": SOUNDS_BASE_PATH + "context.mp3",
            "channel": "main",
        },
    }
}