from turtle import *
from random import random

# Teaching Points
# -- Getting the screen
# -- Onscreen events
# -- Passing functions as parameters
# -- Timer
# -- Global keyword - Maybe

brad = Turtle()
screen = brad.screen # Use the screen on Brad

# Keyboard inputs

def f():
    brad.fd(5)

def ml():
    brad.left(5)

def mr():
    brad.right(5)

screen.onkeypress(f, "Up")
screen.onkeypress(ml, "Left")
screen.onkeypress(mr, "Right")

# Mouse inputs

def on_brad_drag(x, y):
    print(x, y)

def on_turtle_click(x, y):
    brad.circle(20)
    brad.write("Hello!", False, "center")

brad.onclick(on_turtle_click)
brad.ondrag(brad.goto)   # The first parameter is looking for a function with two parameters - 'goto' has two parameters

# Timer
def timeout():
    brad.circle(20)
    screen.ontimer(timeout, t=1500)

# screen.ontimer(timeout, t=500) // Uncomment this

# Inputs
screen.textinput("NIM", "Name of first player:")
screen.numinput("Poker", "Your stakes:", 1000, minval=10, maxval=10000)

screen.listen()
done()