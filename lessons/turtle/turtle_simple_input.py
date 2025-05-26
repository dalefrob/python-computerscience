from turtle import *
from random import random

brad = Turtle()

def f():
    brad.fd(5)

def ml():
    brad.left(5)

def mr():
    brad.right(5)

screen = Screen()

screen.onkeypress(f, "Up")
screen.onkeypress(ml, "Left")
screen.onkeypress(mr, "Right")

screen.listen()
screen.exitonclick()