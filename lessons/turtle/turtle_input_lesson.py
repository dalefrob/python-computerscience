import turtle
import math
import random

# Try to understand Turtle as an instance of a class
# Functions pointers can be stored as variables
# Function signatures

# Setup the turtle

turt = turtle.Turtle("turtle")
turt.color("#000000", "#FF0000")
turt.shapesize(3,3,3)
turt.color(random.random(),random.random(),random.random())

screen = turt.screen

def move():
    turt.forward(10)

def turnleft():
    turt.left(90)

def turnright():
    turt.right(90)


screen.onkey(move, "w")
screen.onkey(turnleft, "a")
screen.onkey(turnright, "d")
screen.onkeypress(move, "Up")

turtlemoving = False
def onscreenclick(x, y):
    global turtlemoving
    if turtlemoving == True:
        return

    angle_radians = math.atan2(y - turt.ycor(), x - turt.xcor())
    angle_degrees = angle_radians * 180 / math.pi
    turt.seth(angle_degrees)
    turtlemoving = True
    turt.goto(x, y)
    turtlemoving = False

colors = ["red", "green", "blue"]
colorindex = 0
def button2(x, y):
    global colorindex
    colorindex += 1
    turt.color( "black", colors[colorindex % len(colors)])
    print(x, y)

screen.onscreenclick(onscreenclick, 1)
screen.onscreenclick(button2, 3)

screen.listen()
turtle.done()