import pyxel
import random

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def aabb(a : Rect, b : Rect):
    return a.y + a.h > b.y and \
    a.y < b.y + b.h and \
    a.x < b.x + b.w and \
    a.x + a.w > b.x




class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.speed = 2
        self.dx = dx
        self.dy = dy
        self.life = 30 #4 * 60
    
    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, 1, 1)

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.life -= 1

    def draw(self):
        pyxel.circ(self.x, self.y, 0.5, 10)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
    
    def update(self):
        if (pyxel.btn(pyxel.KEY_RIGHT)):
            self.x += 1
            self.direction = 1
        elif (pyxel.btn(pyxel.KEY_LEFT)):
            self.x -= 1
            self.direction = -1
        if (pyxel.btn(pyxel.KEY_UP)):
            self.y -= 1
        elif (pyxel.btn(pyxel.KEY_DOWN)):
            self.y += 1
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.shoot()
        
        for b in self.bullets:
            assert isinstance(b, Bullet)
            b.update()
            if b.life < 0:
                self.bullets.remove(b)
    
    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, 16, 8)

    def shoot(self):
        new_bullet = Bullet(self.x + 16, self.y + 4, 1, 0)
        self.bullets.append(new_bullet)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 8, 8)
        for b in self.bullets:
            assert isinstance(b, Bullet)
            b.draw()


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5
    
    def update(self):
        self.x -= self.speed

    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, 8, 8)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, 8)


class App:
    def __init__(self):
        pyxel.init(160, 120, "My Game", 60)
        pyxel.load("my_resource.pyxres")

        self.player = Player(20, 60)

        self.enemies = []

        for i in range(10):
            new_enemy = Enemy(140, 10 * i)
            self.enemies.append(new_enemy)
        
        self.t = 0

        pyxel.run(self.update, self.draw)


    def update(self):
        self.player.update()
        for e in self.enemies:
            e.update()
            enemyrect = e.get_rect()
            if aabb(enemyrect, self.player.get_rect()):
                print("HIT!")
            for b in self.player.bullets:
                if aabb(enemyrect, b.get_rect()):
                    self.enemies.remove(e)
                    self.player.bullets.remove(b)
                    break
        
        self.t += 1
        if (self.t % 120 == 0):
            self.spawn(random.randint(1,5))


    def spawn(self, amount = 1):
        for i in range(amount):
            new_enemy = Enemy(170, random.randint(10, 110))
            self.enemies.append(new_enemy)


    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        for e in self.enemies:
            e.draw()

App()