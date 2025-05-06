import time
from statemachine import *

class RedLight(State):
  def enter(self):
    print("Stop!")

class GreenLight(State):
  def enter(self):
    print("Go!")

class YellowLight(State):
  def enter(self):
    print("Careful...")

machine = StateMachine(None, "red", RedLight())
machine.add_state("green", GreenLight())
machine.add_state("yellow", YellowLight())

def main():
  running = True
  while(running):
    i = input("Next state (red, yellow, green)?: ")
    machine.change_state(i)

if __name__ == "__main__":
  main()