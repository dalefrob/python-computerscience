class State():
    def __init__(self):
        self.machine = None

    def get_context(self):
        return self.machine.context

    def enter(self):
        pass

    def update(self, dt):
        pass

    def exit(self):
        pass


class StateMachine():
    def __init__(self, context):
        self.context = context
        self.states = {}
        self.current_state = None

    def add_state(self, name, state: State, enter: False):
        if name not in self.states:
            self.states[name] = state
            state.machine = self
        if enter:
            self.change_state(name)

    def change_state(self, new_state_name):
        if new_state_name not in self.states:
            print(f"No state called {new_state_name}")

        # for the case when a new machine is made and no state assigned
        if self.current_state != None:
            self.current_state.exit()
        
        self.current_state = self.states[new_state_name]
        self.current_state.enter()

    def update(self, dt):
        if self.current_state != None:
            self.current_state.update(dt)
