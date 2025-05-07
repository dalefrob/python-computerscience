# Lesson 7 - 
# Split screen and cameras

import pygame
import sys, os
from math import *

# Constants - unchanging values
TILESIZE = 128
SCREENWIDTH = TILESIZE * 6
SCREENHEIGHT = TILESIZE * 3
GRASS_GREEN = (30, 150, 50)
MAXLAPS = 3

game_canvas = pygame.Surface((TILESIZE * 5, TILESIZE * 5))
p1_camera = pygame.Rect(0, 0, TILESIZE * 3, TILESIZE * 3)
p2_camera = pygame.Rect(0, 0, TILESIZE * 3, TILESIZE * 3)

class Car(pygame.sprite.Sprite):
  def __init__(self, name, x, y, angle, surface, *groups):
    super().__init__(*groups)
    self.name = name
    self.position = pygame.Vector2(x, y)
    self.orig_image = surface
    self.original_pivot = [39/4, 65/4]

    self.collision_rect = pygame.Rect(x, y, 20, 20)

    self.max_speed = 10.0
    self.speed = 0.0
    self.angle = angle
    self.accerating = False
    self.direction = pygame.Vector2(0) 

    # Gameplay vars
    self.current_checkpoint = 0
    self.lap = 1
  
  def update(self, dt):
    self.direction = pygame.Vector2(cos(self.angle), -sin(self.angle))
    self.position += self.direction * dt * self.speed
    # Set collision rect
    self.collision_rect.center = self.position + self.original_pivot
    self.set_image()
    # Speed damping to slow down
    if not self.accerating:
       self.speed *= 0.975

  def debug_draw(self, screen : pygame.Surface):
    pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

  def set_image(self):
    self.image = pygame.transform.rotozoom(self.orig_image, (self.angle - (pi/2)) * (180/pi), 0.5)
    offset = pygame.Vector2(round(self.position.x), round(self.position.y))
    self.rect = self.image.get_rect(center=self.original_pivot + offset)

  def do_input(self, dt, keybinds):
      key = pygame.key.get_pressed()
      if key[keybinds[0]]:
        self.speed = max(self.speed + 0.5, self.max_speed)
        self.accerating = True
      elif key[keybinds[1]]:
        self.speed = max(self.speed - 1, -self.max_speed * 0.75)
        self.accerating = True
      else:
         self.accerating = False

      if key[keybinds[3]]: 
          self.angle -= 2.0 * dt
      elif key[keybinds[2]]:
          self.angle += 2.0 * dt


# Load resources
dir_path = os.path.dirname(os.path.realpath(__file__))
car_image = pygame.image.load(dir_path + "/assets/car_red_small_5.png")
track_pieces = {
  1: pygame.image.load(dir_path + "/assets/road_asphalt01.png"), # vertical
  2: pygame.image.load(dir_path + "/assets/road_asphalt02.png"), # horizontal
  3: pygame.image.load(dir_path + "/assets/road_asphalt03.png"), # topleft
  5: pygame.image.load(dir_path + "/assets/road_asphalt05.png"), # topright
  39: pygame.image.load(dir_path + "/assets/road_asphalt39.png"), # bottomleft
  41: pygame.image.load(dir_path + "/assets/road_asphalt41.png"), # bottomright
  42: pygame.image.load(dir_path + "/assets/road_asphalt42.png"), # verticalstart
}

def draw_track_piece(surface : pygame.Surface, id : int, cell : tuple):
  surface.blit(track_pieces[id], (cell[0] * TILESIZE, cell[1] * TILESIZE))

def draw_course(surface):
    # Straights
    draw_track_piece(surface, 2, (1,0))
    draw_track_piece(surface, 2, (2,0))
    draw_track_piece(surface, 2, (3,0))
    draw_track_piece(surface, 1, (0,1))
    draw_track_piece(surface, 1, (0,2))
    draw_track_piece(surface, 1, (0,3))
    draw_track_piece(surface, 1, (4,1))
    draw_track_piece(surface, 42, (4,2))
    draw_track_piece(surface, 1, (4,3))
    draw_track_piece(surface, 2, (1,4))
    draw_track_piece(surface, 2, (2,4))
    draw_track_piece(surface, 2, (3,4))
  # Corners
    draw_track_piece(surface, 3, (0,0))
    draw_track_piece(surface, 5, (4,0))
    draw_track_piece(surface, 39, (0,4))
    draw_track_piece(surface, 41, (4,4))

def aabb_collision_check(rect1 : pygame.Rect, rect2 : pygame.Rect):
  """
  Rect1 is the main rect and will be pushed out in reponse
  """
  penetration = False
  if rect1.right > rect2.left and \
    rect1.left < rect2.right and \
    rect1.bottom > rect2.top and \
    rect1.top < rect2.bottom:
      dx = rect2.centerx - rect1.centerx # difference in x
      dy = rect2.centery - rect1.centery # difference in y
      overlap_x = ((rect2.width + rect1.width) / 2) - abs(dx)
      overlap_y = ((rect2.height + rect1.height) / 2) - abs(dy)
      # Choose which axis to push along
      if overlap_x > overlap_y:
         penetration = pygame.Vector2(0, overlap_y * copysign(1, dy*-1))
      else:
         penetration = pygame.Vector2(overlap_x * copysign(1, dx*-1), 0)
  return penetration

# Collision rects
#left_rect = pygame.Rect((-10, 0), (10, SCREENHEIGHT))
#right_rect = pygame.Rect((SCREENWIDTH+10, 0), (10, SCREENHEIGHT))
#top_rect = pygame.Rect((0, -10), (SCREENWIDTH, 10))
#bottom_rect = pygame.Rect((0, SCREENHEIGHT), (SCREENWIDTH, 10))
middle_rect = pygame.Rect((TILESIZE, TILESIZE), (3*TILESIZE, 3*TILESIZE))
# Add them to a list
coll_rects = list()
coll_rects.append(middle_rect)



# Initalize
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
# Fonts for text
font = pygame.font.SysFont(None, 48)

# Cars
car_group = pygame.sprite.Group()
car_start = pygame.Vector2(4 * TILESIZE, 2 * TILESIZE) + pygame.Vector2(TILESIZE / 2)
car1_surf = pygame.image.load(dir_path + "/assets/car_red_small_5.png")
car2_surf = pygame.image.load(dir_path + "/assets/car_green_small_5.png")
car1 = Car("Red", car_start.x+20, car_start.y, pi/2, car1_surf, car_group)
car2 = Car("Green", car_start.x-20, car_start.y, pi/2, car2_surf, car_group)

# Different inputs for different players
car1_keybinds = [
   pygame.K_UP,
   pygame.K_DOWN,
   pygame.K_LEFT,
   pygame.K_RIGHT 
]
car2_keybinds = [
   pygame.K_w,
   pygame.K_s,
   pygame.K_a,
   pygame.K_d
]

# Game
checkpoints = [
   [(256, 0),(256, 128)],
   [(256, TILESIZE*5-128),(256, TILESIZE*5)],
   [(TILESIZE*5-128, TILESIZE*5/2),(TILESIZE*5, TILESIZE*5/2)],
]

def end_race(winning_car):
   global winner, is_racing
   print(f"{winning_car.name} is the winner!")
   winner = winning_car
   is_racing = False

is_racing = True
winner = None

# Camera view sizes (you can adjust this as needed)
CAMERA_WIDTH, CAMERA_HEIGHT = TILESIZE * 3, TILESIZE * 3

# Create "windowed" camera surfaces
p1_view = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
p2_view = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))

game_running = True
while game_running == True:
  dt = min(clock.tick(60) / 1000.0, 0.05)
  
  game_canvas.fill(GRASS_GREEN)
  
  draw_course(game_canvas)

  # Debug draw checkpoints
  for chk in checkpoints:
     pygame.draw.line(game_canvas, (255, 255, 0), chk[0], chk[1], 1)

  # AABB for overlaps
  for car in [car1, car2]:
    # Checkpoints
    line = checkpoints[car.current_checkpoint]
    intersect = car.collision_rect.clipline(line[0], line[1])
    if intersect:
      print("Checkpoint reached!")
      car.current_checkpoint += 1
      if car.current_checkpoint >= len(checkpoints):
         car.current_checkpoint = 0
         car.lap += 1
         if car.lap > MAXLAPS:
            end_race(car)
    
    # Collision
    for cr in coll_rects:
      penetration = aabb_collision_check(car.collision_rect, cr)
      if penetration:
        car.position += penetration
        car.speed *= 0.85
  
  # Simple car hit 
  car_hit = aabb_collision_check(car1.collision_rect, car2.collision_rect)
  if car_hit:
     car1.position += car_hit * 2.0
     car2.position += -car_hit * 2.0
     car1.speed = 0
     car2.speed = 0

  # Don't allow inputs if the race isnt going
  if is_racing:
    car1.do_input(dt, car1_keybinds)
    car2.do_input(dt, car2_keybinds)

  car_group.update(dt)

  # Update camera positions and constrain to world
  p1_camera.center = car1.position
  p1_camera.clamp_ip(game_canvas.get_rect())
  p2_camera.center = car2.position
  p2_camera.clamp_ip(game_canvas.get_rect())

  car_group.draw(game_canvas)

  if winner and not is_racing:
    # Turn off acceleration
    for car in [car1, car2]:
       car.accerating = False
    text_surface = font.render(f"{winner.name} is the winner!", True, "white")
    text_rect = text_surface.get_rect(center=(SCREENWIDTH/2, SCREENHEIGHT/2))
    screen.blit(text_surface, text_rect)

  # Blit only the camera's view to the smaller surfaces
  p1_view.blit(game_canvas, (0, 0), p1_camera)
  p2_view.blit(game_canvas, (0, 0), p2_camera)

  # Now blit the smaller surfaces to the main screen
  screen.blit(p1_view, (0, 0))
  screen.blit(p2_view, (CAMERA_WIDTH, 0))

  # Draw a line between the camera views
  pygame.draw.line(screen, (0, 0, 0), (CAMERA_WIDTH, 0), (CAMERA_WIDTH, CAMERA_HEIGHT), 3)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        game_running = False
        pygame.quit()
        sys.exit()