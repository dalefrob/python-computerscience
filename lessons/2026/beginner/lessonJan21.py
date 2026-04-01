import turtle as t
import random

leo = t.Turtle("turtle")
leo.color(0, 0, 1)

raph = t.Turtle("turtle")
raph.color("red")

def drawSquare(x, y, _t):
    _t.goto(x, y)
    for i in range(4):
        _t.forward(200)
        _t.left(90)


for i in range(100):
    for ninjaturtle in [leo, raph]:
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        drawSquare(x, y, ninjaturtle)

# for i in range(360 * 8):
#     leo.forward((0.001 * i))
#     leo.left(1)


t.done()