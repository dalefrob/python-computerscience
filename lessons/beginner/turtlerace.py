# race.py - simplest turtle race simulator
import turtle
import random
import time

super_colors = [(0,255,255), (255,255,0), (255,0,255)]

class SuperTurtle(turtle.Turtle):
    def __init__(self, name : str, orig_color):
        super().__init__("turtle", 1000, True)
        self.name = name
        self.super = 0
        self.orig_color = orig_color

        self.color((0,0,0), orig_color)
    
    def move(self):
        move_amt = random.randint(1, 4)
        if self.super > 0:
            self.color(super_colors[self.super % 3], self.orig_color)
            move_amt *= 2
            self.super -= 1
        else:
            self.color((0,0,0),self.orig_color)
        self.forward(move_amt)


screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Simple Turtle Race")
screen.colormode(255)
screen.bgcolor((20, 100, 30))
screen.delay = 0

# Finish line x coordinate
finish_x = 330

number_of_turtles = int(screen.textinput("Turtle Race!", "How many racers 1-10?"))
# clamp value
if number_of_turtles <= 1:
    number_of_turtles = 2
elif number_of_turtles >= 10:
    number_of_turtles = 10

turtles : list[SuperTurtle] = []
for i in range(number_of_turtles):
    color_tuple = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    t = SuperTurtle("default", color_tuple)
    t.speed(10)
    t.penup()
    t.goto(-250, -100 + (20 * i))
    turtles.append(t)

# Draw finish line
line = turtle.Turtle()
line.hideturtle()
turtle.tracer(0, 0)
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

# Race loop
winner : turtle.Turtle = None
while not winner:
    random.shuffle(turtles)
    for t in turtles:
        if random.random() < 0.01:
            t.super = 20
        t.move()
        if t.xcor() >= finish_x:
            winner = t
    screen.update()
    time.sleep(0.05)

# Announce winner
announce = turtle.Turtle()
announce.hideturtle()
announce.penup()
announce.goto(0, 0)
announce.write("We have a winner!", align="center", font=("Arial", 18, "bold"))

screen.tracer(1)

for i in range(720):
    winner.left(1)

screen.mainloop()
