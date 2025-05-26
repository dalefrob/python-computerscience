import turtle

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

t = turtle.Turtle()
t.color("green")
t.speed(0)
turtle.delay(0)

turtles = []
for i in range(4):
    new_t = turtle.Turtle("turtle")
    new_t.setheading(90 * i)
    turtles.append(new_t)


def draw_rect(t, x, y, width, height, color = "red"):
    t.penup()
    t.setheading(0)
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.forward(width)
    t.right(90)
    t.forward(height)
    t.right(90)
    t.forward(width)
    t.right(90)
    t.forward(height)
    t.end_fill()

isBlack = True
for row in range(4):
    isBlack = not isBlack
    for col in range(4):
        color = "black" if isBlack else "red"
        draw_rect(t, -200 + row * 20, -200 + col * 20, 20, 20, color)
        isBlack = not isBlack

c_index = 0
for i in range(100):
    c_index = i % len(colors)
    color = colors[c_index]
    draw_rect(t, -300 + i * 20, 300, 20, 20, color)

n = 0
while n < 200:
    for t in turtles:
        t.forward(2)
        if n % 20 == 0:
            t.right(25)
    n += 1

turtle.done()