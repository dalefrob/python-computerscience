TYPE_NORMAL = 0
TYPE_FIRE = 1
TYPE_WATER = 2
TYPE_ELECTRIC = 3
TYPE_GRASS = 4

typetable = [
    [1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 0.5, 0.5, 1.0, 2.0],
    [1.0, 2.0, 0.5, 1.0, 0.5],
    [1.0, 1.0, 2.0, 0.5, 0.5],
    [1.0, 0.5, 2.0, 1.0, 0.5],
]

allpokemon = [
    { # 0
        "name": "Ivysaur",
        "type": TYPE_GRASS,
        "power": 2
    },
    { # 1
        "name": "Charmander",
        "type": TYPE_FIRE,
        "power": 1
    },
    {
        "name": "Blastoise",
        "type": TYPE_WATER,
        "power": 3
    },
    {
        "name": "Pikachu",
        "type": TYPE_ELECTRIC,
        "power": 2
    },
    {
        "name": "Snorlax",
        "type": TYPE_NORMAL,
        "power": 3
    }
]