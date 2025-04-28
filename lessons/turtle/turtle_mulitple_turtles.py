from turtle import Turtle
from random import random

brad = Turtle()
rob = Turtle()
carter = Turtle()

for i in range(100):
    for turtle in [brad, rob, carter]:
        # turtle.speed(0)
        # turtle.screen.delay(0)
        steps = int(random() * 100)
        angle = int(random() * 360)
        turtle.right(angle)
        turtle.fd(steps)