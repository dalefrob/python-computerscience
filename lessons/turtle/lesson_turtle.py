import turtle

turtle.color("#775533")  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f

# draw octagon
def draw_octagon(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.color("#224466")
    turtle.setheading(0)
    for iter in range(8):
        turtle.forward(30)
        turtle.left(360 / 8)

# for i in range(10):
#     x = -300 + (i * 60)
#     y = -80
#     draw_octagon(x, y)


# mickey mouse
# turtle.penup()
# turtle.goto(0, -100)
# turtle.setheading(170)
# turtle.pendown()
# turtle.begin_fill()
# turtle.circle(-60)
# turtle.end_fill()

# turtle.penup()
# turtle.goto(200, -100)
# turtle.setheading(170)
# turtle.pendown()
# turtle.begin_fill()
# turtle.circle(-60)
# turtle.end_fill()

#turtle.circle(100, 45)

turtle.speed(0)
turtle.delay(0)
c = 0.0
for i in range(100):
    if i == 0 or i == 100:
        continue
    c += 0.01
    turtle.begin_fill()
    turtle.color(c, c, c)
    turtle.goto(-300 + (i*5), 0)
    turtle.circle(50)
    turtle.end_fill()


turtle.done()