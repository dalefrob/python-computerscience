import turtle as t
import random

t.write("Turtle", font=("Arial", 40, "normal"))
t.delay(0)
t.color("red")
t.speed(0)
t.forward(30)
t.left(40)
t.forward(30)
t.penup()
t.goto(-100, 100)
t.pendown()
t.color("green")
t.circle(20)

t.penup()
t.goto(100, 100)
t.setheading(0)
t.pendown()
t.begin_fill()
t.forward(70)
t.left(90)
t.forward(70)
t.left(90)
t.forward(70)
t.left(90)
t.forward(70)
t.left(90)
t.end_fill()

def draw_star(turt : t.Turtle, x, y, size):
    turt.penup()
    turt.goto(x, y)
    turt.setheading(0)
    turt.color("#92A8D1")
    turt.pendown()

    turt.begin_fill()
    for i in range(10):
        if i % 2 == 0:
            turt.left(126)
        else:
            turt.right(54)
        turt.forward(size)
    turt.penup()
    turt.end_fill()

for _ in range(20):
  x = random.randrange(-200, 200)
  y = random.randrange(-200, 200)
  size = random.randrange(5, 20)
  draw_star(t, x, y, size)

#colors = ["red", "orange", "yellow", "green", "blue", "violet"]

# brad = t.Turtle("turtle")
# brad.speed(0)
# brad.left(180)
# brad.forward(100)
# brad.right(90)
# brad.forward(100)

# t.delay(0.5)

# index = 0
# for i in range(100):
#     if i % 7 == 0:
#       index += 1
#       brad.begin_fill()
#       brad.circle(40)
#       brad.end_fill()
#       t.circle(30)
#       if index == len(colors):
#         index = 0
#     brad.color(colors[index])
#     t.forward(1)
#     t.left(1)
#     brad.forward(1)
#     brad.right(1)

t.done()