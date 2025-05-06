# ----

class State():
   def __init__(self):
      self.machine = None
  
   def enter(self):
    pass
   
   def update(self, dt):
      pass
   
   def exit(self):
      pass


class StateMachine():
   def __init__(self, context, init_state_name, init_state):
      self.states = {}
      self.add_state(init_state_name, init_state)
      self.current_state : State = init_state

   def add_state(self, name, state : State):
      if name not in self.states:
         self.states[name] = state
         state.machine = self

   def change_state(self, new_state_name):
      if new_state_name not in self.states:
         print(f"No state called {new_state_name}")
      
      self.current_state.exit()
      self.current_state = self.states[new_state_name]
      self.current_state.enter()
   
   def update(self, dt):
      if self.current_state != None:
         self.current_state.update(dt)


# ----