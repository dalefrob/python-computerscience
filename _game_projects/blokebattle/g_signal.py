class Signal:
  def __init__(self):
      self._listeners = []

  def connect(self, callback):
      """Connect a function to the signal."""
      if callback not in self._listeners:
          self._listeners.append(callback)

  def disconnect(self, callback):
      """Disconnect a function from the signal."""
      if callback in self._listeners:
          self._listeners.remove(callback)

  def emit(self, *args, **kwargs):
      """Emit the signal, calling all connected listeners."""
      for listener in self._listeners:
          listener(*args, **kwargs)
