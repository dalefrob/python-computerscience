import turtle as t
import random

t.delay(0)

leo = t.Turtle("turtle")
leo.color("blue")
leo.forward(30)

mikey = t.Turtle("turtle")
mikey.color("orange")
mikey.backward(30)

turtles_list = [leo, mikey]



for i in range(2):
    newturtle = t.Turtle("turtle")
    rand_angle = random.randint(0, 359)
    newturtle.setheading(rand_angle)
    newturtle.forward(rand_angle)
    newturtle.color(random.random(), 0, random.random())
    newturtle.speed(0)
    turtles_list.append(newturtle)

for i in range(2):        # 2
    for t in turtles_list:  # turtles_list[0], turtles_list[1], turtles_list[2]...
        rand_angle = random.randint(0, 359)
        t.setheading(rand_angle)
        t.forward(random.randrange(2,12))

# ----
CIRCLESIZE = 25
for i in range(5):
    for j in range(5):
        leo.pensize(3)
        leo.penup()
        leo.goto((CIRCLESIZE*2) * i, (CIRCLESIZE*2) * j)
        leo.pendown()
        leo.color(random.random(), random.random(), random.random())
        leo.circle(CIRCLESIZE)

t.screen.exitonclick()
