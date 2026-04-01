import turtle as t
import random

START_X = -220
FINISHLINE_X = 220

ws = t.Screen()
ws.setup(1.0, 1.0)
ws.bgcolor(0.2, 0.4, 0.1)

half_window_height = ws.window_height() / 2

t.penup()
t.goto(FINISHLINE_X, -half_window_height) 
t.pendown()
t.goto(FINISHLINE_X, half_window_height)

turtle_names = ["Bob", "Steve", "SixSeven", "Captain", "Leo", "Mike", "Raph", "Don"]
turtles = []
racer_names = {}


def make_random_name() -> str:
    prefixes = ["Fire", "Ice", "Thunder", "Dark", "Cyber", "Arcane"]
    suffixes = ["Dragon", "Fly", "Bloke", "Toaster", "Spoon", "Container"]
    return random.choice(prefixes) + random.choice(suffixes)


def make_turtle(y_pos : int):
    new_turtle = t.Turtle("turtle")
    new_turtle.penup()
    new_turtle.goto(START_X, -200 + y_pos)
    new_turtle.fillcolor(random.random(), random.random(), random.random())
    new_turtle.pencolor("black")

    name =  make_random_name() # random.choice(turtle_names) # Choose a random name from the list
    racer_names[new_turtle] = name # Set the KEY VALUE dict for turtle object to its name
    new_turtle.write(name, False, "left", ("Arial", 12, "normal"))

    turtles.append(new_turtle)

def show_winner(winning_turtle : t.Turtle):
    # Turtle spins around in place
    for i in range(90):
        winning_turtle.left(4)

for i in range(4):
    make_turtle(i * 20)

winner = None
racing = len(turtles) > 0
while(racing):
    for _t in turtles:
        _t.forward( random.randint(1, 5) )
        if _t.xcor() > FINISHLINE_X:
            print(racer_names[_t] + " wins!")
            racing = False
            winner = _t
            break

show_winner(winner)

t.done()