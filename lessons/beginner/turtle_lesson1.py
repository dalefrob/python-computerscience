import turtle

def draw_square(xpos : int, ypos : int, length : int):
    turtle.penup()
    turtle.goto(xpos, ypos)
    turtle.pendown()
    turtle.forward(length)
    turtle.left(90)
    turtle.forward(length)
    turtle.left(90)
    turtle.forward(length)
    turtle.left(90)
    turtle.forward(length)

def draw_triangle(xpos : int, ypos : int, length : int):
    turtle.penup()
    turtle.goto(xpos, ypos)
    turtle.setheading(0)
    turtle.pendown()
    turtle.forward(length)
    turtle.left(120)
    turtle.forward(length)
    turtle.left(120)
    turtle.forward(length)

for i in range(10):
    draw_triangle(-300 + (i * 50), 0, 50)

turtle.done()

# LISTS and DICTIONARIES