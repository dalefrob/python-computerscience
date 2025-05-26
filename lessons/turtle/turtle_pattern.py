import turtle
import random
CIRCLE_SIZE = 40
BGCOLOR = "#335566"
colors = ["red", "black"]
yellows = [i for i in range(1, 256, 5)]
is_black = True

s = turtle.Screen()
turtle.delay(0)
turtle.speed(0)
turtle.bgcolor(BGCOLOR)
x = (-s.window_width()/2) +(CIRCLE_SIZE/2)
y = (s.window_height()/2) -CIRCLE_SIZE
count = 0
for i in range(s.window_width() // CIRCLE_SIZE):
    is_black = not is_black
    for j in range(s.window_height() // CIRCLE_SIZE):
        count += 1
        turtle.penup()
        pos = (x + (i * CIRCLE_SIZE), y + (-j * CIRCLE_SIZE))
        turtle.goto(pos[0], pos[1])
        turtle.pendown()
        turtle.begin_fill()
        fillcolor = colors[is_black]
        if (count) in yellows:
            fillcolor = "orange"
        turtle.color(fillcolor)
        turtle.circle(CIRCLE_SIZE/2)
        turtle.end_fill()
        if random.random() < 0.4:
            turtle.color("white")
            turtle.penup()
            turtle.goto(pos[0], pos[1] + CIRCLE_SIZE/4)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(CIRCLE_SIZE / 4)
            turtle.end_fill()
        is_black = not is_black
    

turtle.done()