from turtle import Turtle

t = Turtle()

def right():
  t.setheading(0)
  t.forward(10)

def left():
  t.setheading(180)
  t.forward(10)

def up():
  t.setheading(90)
  t.forward(10)

def down():
  t.setheading(270)
  t.forward(10)

def main():
  t.speed(0)
  
  s = t.screen # Screen is a singleton
  s.delay(0)

  # Input commands
  s.listen()
  s.onkey(right, "Right")
  s.onkey(left, "Left")
  s.onkey(up, "Up")
  s.onkey(down, "Down")

  s.mainloop()


if __name__ == "__main__":
  main()