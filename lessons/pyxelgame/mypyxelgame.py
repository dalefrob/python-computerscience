import pyxel

bullets = []

# Projectile
class Fireball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 2
        self.life = 100


    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.life -= 1


    def draw(self):
        img_u = 32
        img_v = 0
        if self.dy != 0:
            img_v = 8
            img_u = 32 if self.dy < 0 else 40
        else:
            img_u = 32 if self.dx < 0 else 40

        pyxel.blt(self.x, self.y, 0, img_u, img_v, 8, 8, 1)


# Player controlled object
class Player:
    MOVE_KEYS = (pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN)
    DIR_RIGHT = 0
    DIR_LEFT = 1
    DIR_UP = 2
    DIR_DOWN = 3

    def __init__(self, x, y):
        self.x = 10
        self.y = 40
        self.dir_x = 1
        self.dir_y = 1
        self.last_pressed_dir = self.DIR_RIGHT
        self.animate = False
    
    def update(self):
        self.animate = False
        if any(pyxel.btn(k) for k in self.MOVE_KEYS):
            self.animate = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
            self.dir_x = 1
            self.last_pressed_dir = self.DIR_RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
            self.dir_x = -1
            self.last_pressed_dir = self.DIR_LEFT

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
            self.dir_y = -1
            self.last_pressed_dir = self.DIR_UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1
            self.dir_y = 1
            self.last_pressed_dir = self.DIR_DOWN

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shoot()

    def shoot(self):
        new_bullet = None
        match self.last_pressed_dir:
            case self.DIR_LEFT:
                new_bullet = Fireball(self.x, self.y, -1, 0)
            case self.DIR_RIGHT:
                new_bullet = Fireball(self.x, self.y, 1, 0)
            case self.DIR_UP:
                new_bullet = Fireball(self.x, self.y, 0, -1)
            case self.DIR_DOWN:
                new_bullet = Fireball(self.x, self.y, 0, 1)
        if new_bullet:
            bullets.append(new_bullet)

    def draw(self):
        frame_u = 16
        if self.animate:
            frame_u = 16 if (pyxel.frame_count // 8) % 2 == 0 else 24
        frame_v = 0 if self.dir_x == 1 else 8
        pyxel.blt(self.x, self.y, 0, frame_u, frame_v, 8, 8, 8,)
        # pyxel.rect(self.x, self.y, 8, 8, 6)


# The Game 
class App:
    def __init__(self):
        pyxel.init(128, 128, "My Game")
        pyxel.load("my_resource.pyxres")

        self.player = Player(64, 64)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        for b in bullets:
            b.update()

    def draw(self):
        pyxel.cls(1)
        self.player.draw()
        for b in bullets:
            b.draw()


App()