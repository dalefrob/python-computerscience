from enum import IntFlag, Enum, auto

# Colors
ORANGE = (255, 190, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHTBLUE = (0, 100, 200)
GRAY = (160, 160, 160)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)

# color text
def colored_by_value(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def colored(rgb: tuple, text):
    return colored_by_value(rgb[0], rgb[1], rgb[2], text)


class Elements(str, Enum):
    NONE = None
    FIRE = "Fire"
    WATER = "Water"
    EARTH = "Earth"
    AIR = "Air"

    def __str__(self):
        return self.value


class Stat(str, Enum):
    STRENGTH = "strength"
    STAMINA = "stamina"
    AGILITY = "agility"
    INTELLECT = "intellect"

    def __str__(self):
        return self.value


class BonusStat(str, Enum):
    DODGE = "dodge"
    CRIT = "crit"
    PARRY = "parry"

    def __str__(self):
        return self.value


class BuffFlags(IntFlag):
    NONE = auto()
    PREVENT_ACTION = auto()
    REFLECT_MAGIC = auto()
    MAG_WEAKNESS = auto()
    MAG_RESISTANCE = auto()


class ProcTiming(IntFlag):
    ON_TURNSTART = auto()
    ON_TURNEND = auto()
    ON_HIT = auto()
    ON_CRIT = auto()
    ON_PARRY = auto()
    ON_TOOKDAMAGE = auto()
    ON_FATAL = auto()