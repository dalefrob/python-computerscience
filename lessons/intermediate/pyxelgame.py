import pyxel

def collide(a, b):
    return (
        a.x < b.x + b.w and
        a.x + a.w > b.x and
        a.y < b.y + b.h and
        a.y + a.h > b.y
    )


def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[0].pget(tile_x, tile_y)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
    
    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 8,)


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class App:
    def __init__(self):
        pyxel.init(128, 128, "My Game", 30)
        pyxel.load("my_resource.pyxres")

        self.player = Player(80, 60)
        self.tile = Rect(0, 100, 160, 8)

        pyxel.run(self.update, self.draw)

    def update(self):
        dx = 0
        dy = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            dx = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            dx = -1
        if pyxel.btn(pyxel.KEY_DOWN):
            dy = 1
        elif pyxel.btn(pyxel.KEY_UP):
            dy = -1
        move_rect = Rect(self.player.x + dx, self.player.y + dy, self.player.w, self.player.h)
        if collide(move_rect, self.tile) == False:
            self.player.x += dx
            self.player.y += dy
        print(get_tile(self.player.x / 8, self.player.y / 8))

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)

        self.player.draw()

App()
