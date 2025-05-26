import turtle
#turtle.mode("logo")

s = turtle.Screen()
s.bgcolor("lightgreen")

turtle.delay(0)

# PLayer 1
player = turtle.Turtle()
player.shape("triangle")
player.penup()
player.speed(0)
player.goto(50, 50)

# Player 2
player2 = turtle.Turtle()
player2.shape("triangle")
player2.color("Red")
player2.penup()
player2.speed(0)

def p1turnleft():
    player.left(20)

def p1turnright():
    player.right(20)

def p2turnleft():
    player2.left(20)

def p2turnright():
    player2.right(20)

def is_collided_with(a, b):
    return abs(a.xcor() - b.xcor()) < 10 and abs(a.ycor() - b.ycor()) < 10

running = True
def quit():
    global running
    running = False

turtle.listen()
turtle.onkey(p1turnleft, "Left")
turtle.onkey(p1turnright, "Right")
turtle.onkey(p2turnleft, "z")
turtle.onkey(p2turnright, "c")
turtle.onkey(quit, "q")

while running:
    player.forward(0.5)
    player2.forward(0.5)
    if is_collided_with(player, player2):
        turtle.bgcolor("yellow")
    else:
        turtle.bgcolor("lightgreen")
    