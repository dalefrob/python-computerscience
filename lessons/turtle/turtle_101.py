import turtle

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

t = turtle.Turtle()
t.color("green")
t.speed(0)
turtle.delay(0)


def draw_rect(x, y, width, height, color = "red"):
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
for row in range(10):
    isBlack = not isBlack
    for col in range(10):
        color = "black" if isBlack else "red"
        draw_rect(-200 + row * 20, -200 + col * 20, 20, 20, color)
        isBlack = not isBlack

c_index = 0
for i in range(100):
    c_index = i % len(colors)
    color = colors[c_index]
    draw_rect(-300 + i * 20, 300, 20, 20, color)
    

turtle.done()