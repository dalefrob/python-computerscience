from enum import Enum

# color text
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


class Elements(str, Enum):
   NONE = None
   FIRE = "Fire"
   WATER = "Water"
   EARTH = "Earth"
   AIR = "Air"