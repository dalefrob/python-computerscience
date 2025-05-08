import pygame

class Screen():
    def __init__(self):
        self.manager = None

    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def on_enter(self):
        """ Called when the screen is switched to """
        pass

    def on_exit(self):
        """ Called when the screen is switched away from """
        pass


class ScreenManager():
    """
    A manager class to handle changing of game screens
    """

    def __init__(self, gameref, alias: str, first_screen: Screen):
        self.gameref = gameref
        self._screens = {}
        self.current_screen = self.add_screen(alias, first_screen)

    def add_screen(self, alias: str, screen: Screen) -> Screen:
        if not alias in self._screens:
            screen.manager = self  # Ensure each screen has access to its manager
            self._screens[alias] = screen
            return screen
        return False

    def update(self, dt):
        self.current_screen.update(dt)

    def render(self, surface):
        self.current_screen.render(surface)

    def change_screen(self, screen_name: str) -> bool:
        if screen_name in self._screens:
            if self.current_screen:
                self.current_screen.on_exit()
            self.current_screen = self._screens[screen_name]
            self.current_screen.on_enter()
            return True
        return False


class Button():
   def __init__(self, x, y, width, height, font, buttonText="Button", onclick=None):
      self.x = x
      self.y = y
      self.width = width
      self.height= height

      self.onclick = onclick # Click function
      self.was_pressed = False

      self.buttonSurface = pygame.Surface((self.width, self.height))
      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
      self.textSurface = font.render(buttonText, True, (200, 200, 200))

      self.state = "normal"


   def update(self):
      mouse_position = pygame.mouse.get_pos()
      mouse_pressed = pygame.mouse.get_pressed()[0]

      if self.rect.collidepoint(mouse_position): # If mouse is over the rect
         self.state = "hover"
         if mouse_pressed: # If mouse is pressed
            self.was_pressed = True # Was pressed, but we're waiting for an unpress
            self.state = "click"
         elif self.was_pressed: # Mouse is still over rect, pressed and an unpress happens
          self.was_pressed = False
          if self.onclick: # Run the click function
            self.onclick()
            return      
            
      else:
         self.state = "normal"
         self.was_pressed = False # If we leave the rect, reset to no press
   

   def render(self, screen : pygame.Surface):
      match self.state:
         case "normal": self.buttonSurface.fill((20, 20, 20))
         case "hover": self.buttonSurface.fill((80, 80, 80))
         case "click": self.buttonSurface.fill((100, 100, 255))

      screen.blit(self.buttonSurface, self.rect)
      
      # Center the text on the button
      text_rect = self.textSurface.get_rect(center=self.rect.center)
      screen.blit(self.textSurface, text_rect)