import math
import turtle

turtle = turtle.Turtle()

radius = int(input("enter a number"))
c = 2 * math.pi * radius
a = math.pi * radius * radius

print(c)
print(a)

turtle.circle(radius)
turtle.screen.mainloop()
