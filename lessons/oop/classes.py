class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.hobby = "Programming"

  def introduce(self):
    print(f"Hello, my name is {self.name} and my hobby is {self.hobby}.")

  def __str__(self):
    return f"An instance of Person with name: {self.name}"

p1 = Person("John", 36)
p1.introduce() # call the method

print(p1)

# YOU ALMOST NEVER DO THIS
del p1.age # delete a property

# THIS IS MORE COMMON
del p1 # delete the object