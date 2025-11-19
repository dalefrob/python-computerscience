# race.py - simplest turtle race simulator
import turtle
import math
import random

screen = turtle.Screen()
screen.setup(width=600, height=300)
screen.title("Simple Turtle Race")
screen.colormode(255)
screen.bgcolor((20, 100, 30))

# Finish line x coordinate
finish_x = 230

number_of_turtles = int(screen.textinput("Turtle Race!", "How many racers 1-10?"))
# clamp value
if number_of_turtles <= 1:
    number_of_turtles = 2
elif number_of_turtles >= 10:
    number_of_turtles = 10

turtles = []
for i in range(number_of_turtles):
    t = turtle.Turtle(shape="turtle")
    t.speed(10)
    turtle.colormode(255)
    color_tuple = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    t.color((0,0,0),color_tuple)
    t.penup()
    t.goto(-250, -100 + (20 * i))
    turtles.append(t)

# Draw finish line
line = turtle.Turtle()
line.hideturtle()
turtle.tracer(0)
line.penup()
line.goto(finish_x, 150)
line.delay = 0
line.speed(0)

def draw_square(t : turtle.Turtle, x, y, black = False):
    t.goto(x, y)
    t.speed(0)
    t.pendown()
    t.setheading(0)
    if black:
        t.fillcolor("black")
    else:
        t.fillcolor("white")
    t.begin_fill()
    for i in range(4):
        t.forward(10)
        t.right(90)
    t.end_fill()
    t.penup()

# draw checkered finish
square_count = 0
for i in range(2):
    for j in range(30):
        square_count += 1
        black = square_count % 2 == 0
        draw_square(line, finish_x + (i * 10), 150 - j * 10, black)
    square_count += 1

turtle.update()
turtle.tracer(1)

# Race loop
winner : turtle.Turtle = None
while not winner:
    for t in turtles:
        t.forward(random.randint(1, 10))
        if t.xcor() >= finish_x:
            winner = t

# Announce winner
announce = turtle.Turtle()
announce.hideturtle()
announce.penup()
announce.goto(0, 0)
announce.write("We have a winner!", align="center", font=("Arial", 18, "bold"))

for i in range(720//10):
    winner.left(10)

screen.mainloop()
