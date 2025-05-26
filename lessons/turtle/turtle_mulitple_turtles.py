import turtle as t
import random

# Teach turtle instances, importing as t, storing objects in lists, returning objects from a function

#t.delay(0)
#turtle_instance = t.Turtle()

def make_turtle(color = "black"):
    new_turtle = t.Turtle("turtle")
    new_turtle.color(color)
    new_turtle.setheading(random.random() * 360)
    return new_turtle

turtle_list = [
    make_turtle("orange"),
    make_turtle("blue"),
    make_turtle("red"),
    make_turtle("purple"),
]

for i in range(100):
    for turtle in turtle_list:
        # turtle.speed(0)
        # turtle.screen.delay(0)
        #steps = int(random() * 50)
        
        turtle.right(random.random() * 360)
        turtle.fd(20)

t.done()