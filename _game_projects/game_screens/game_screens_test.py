import pygame
import sys

SCREENWIDTH = 400
SCREENHEIGHT = 400
FRAMERATE = 60

class Game():
   def __init__(self):
      pygame.init()
      self.mainsurf = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
      self.clock = pygame.time.Clock()
      self.font = pygame.font.SysFont(None, 20)
      self.running = True
      self.screens = {
         "mainmenu": MainMenuScreen(self),
         "gamescreen": GameScreen(self)
      }

      self.current_screen : Screen = self.screens["mainmenu"]
   
   def run(self):
      while self.running:
        dt = min(self.clock.tick(FRAMERATE) / 1000.0, 0.05)

        events = pygame.event.get()
        self.current_screen.handle_input(events)
        self.current_screen.update(dt)
        self.current_screen.render(self.mainsurf)

        pygame.display.flip()
    
   def change_screen(self, screen_name : str):
      if screen_name in self.screens:
         self.current_screen = self.screens[screen_name]
        

# Base class for Screens        
class Screen():
   def __init__(self, gameref : Game):
      self.gameref = gameref
   
   def update(self, dt):
      pass
   
   def render(self, screen : pygame.Surface):
      pass
   
   def handle_input(self, events):
      pass
      

# Main Menu Screen
class MainMenuScreen(Screen):
   def __init__(self, gameref):
      super().__init__(gameref)
      
      # def onplayclick():
      #   self.gameref.change_screen("gamescreen")

      self.buttons = [
         Button(20, 20, 50, 20, gameref.font, "Play", lambda: self.gameref.change_screen("gamescreen"))
      ]
   
   def render(self, screen):
      screen.fill((100, 100, 0))
      text_surface = self.gameref.font.render(f"Main Menu", True, "white")
      text_rect = text_surface.get_rect(center=(SCREENWIDTH/2, SCREENHEIGHT/2))
      screen.blit(text_surface, text_rect)
      for b in self.buttons:
         b.render(screen)

   def update(self, dt):
      for b in self.buttons:
         b.update()

   def handle_input(self, events):
      for event in events:
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
      
      key = pygame.key.get_pressed()
      if key[pygame.K_UP]:
         self.gameref.change_screen("gamescreen")


# Game Screen where all of the action happens.
# It makes sense to put this in another file.
class GameScreen(Screen):
   def __init__(self, gameref):
      super().__init__(gameref)
      self.menubutton = Button(20, 100, 50, 20, gameref.font, "Menu", lambda: self.gameref.change_screen("mainmenu"))
   
   def render(self, screen):
      screen.fill((0, 100, 100))
      text_surface = self.gameref.font.render(f"Game Screen", True, "white")
      text_rect = text_surface.get_rect(center=(SCREENWIDTH/2, SCREENHEIGHT/2))
      screen.blit(text_surface, text_rect)
      self.menubutton.render(screen)

   def update(self, dt):
      self.menubutton.update()

   def handle_input(self, events):
      for event in events:
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()


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
      




# Entry point
def main():
  game = Game()
  game.run()



if __name__ == "__main__":
   main()