import pygame
import sys
import math
import os

MAPWIDTH = 24
MAPHEIGHT = 24
SCREENWIDTH = 640
SCREENHEIGHT = 480

MAP = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def main():
  pos_x, pos_y = 22, 12
  dir_x, dir_y = -1, 0
  plane_x, plane_y = 0, 0.66
  time = 0.0
  old_time = 0.0
  

  pygame.init()
  win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
  pygame.display.set_caption('Raycaster')

  clock = pygame.time.Clock()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)

    # Clear the screen
    win.fill((0, 0, 0))

    # Calculate time difference
    new_time = pygame.time.get_ticks()
    time = (new_time - old_time) / 1000.0
    old_time = new_time

    drawrays(pos_x, pos_y, dir_x, dir_y, plane_x, plane_y, win)

    move_speed = 5.0 * time
    rot_speed = 2.0 * time

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      new_dir_x = dir_x * math.cos(rot_speed) - dir_y * math.sin(rot_speed)
      new_dir_y = dir_x * math.sin(rot_speed) + dir_y * math.cos(rot_speed)
      dir_x, dir_y = new_dir_x, new_dir_y

      new_plane_x = plane_x * math.cos(rot_speed) - plane_y * math.sin(rot_speed)
      new_plane_y = plane_x * math.sin(rot_speed) + plane_y * math.cos(rot_speed)
      plane_x, plane_y = new_plane_x, new_plane_y
    elif keys[pygame.K_RIGHT]:
      new_dir_x = dir_x * math.cos(-move_speed) - dir_y * math.sin(-move_speed)
      new_dir_y = dir_x * math.sin(-move_speed) + dir_y * math.cos(-move_speed)
      dir_x, dir_y = new_dir_x, new_dir_y

      new_plane_x = plane_x * math.cos(-move_speed) - plane_y * math.sin(-move_speed)
      new_plane_y = plane_x * math.sin(-move_speed) + plane_y * math.cos(-move_speed)
      plane_x, plane_y = new_plane_x, new_plane_y
    
    if keys[pygame.K_UP]:
      if MAP[int(pos_x + dir_x * move_speed)][int(pos_y)] == 0:
        pos_x += dir_x * move_speed
      if MAP[int(pos_x)][int(pos_y + dir_y * move_speed)] == 0:
        pos_y += dir_y * move_speed
    elif keys[pygame.K_DOWN]:
      if MAP[int(pos_x - dir_x * move_speed)][int(pos_y)] == 0:
        pos_x -= dir_x * move_speed
      if MAP[int(pos_x)][int(pos_y - dir_y * move_speed)] == 0:
        pos_y -= dir_y * move_speed

    # Update the display
    pygame.display.flip()
    clock.tick(60)

def drawrays(pos_x, pos_y, dir_x, dir_y, plane_x, plane_y, win):
    for ray in range(SCREENWIDTH):
      # Calculate ray position and direction
      camera_x = 2 * ray / float(SCREENWIDTH) - 1
      ray_dir_x = dir_x + plane_x * camera_x
      ray_dir_y = dir_y + plane_y * camera_x

      # Which box of the map we're in
      map_x = int(pos_x)
      map_y = int(pos_y)

      # Length of ray from current position to next x or y-side
      side_dist_x = 0.0
      side_dist_y = 0.0

      # Length of ray from one x or y-side to next x or y-side
      delta_dist_x = 1e30 if ray_dir_x == 0 else abs(1 / ray_dir_x)
      delta_dist_y = 1e30 if ray_dir_y == 0 else abs(1 / ray_dir_y)

      # Step direction and initial side_dist
      step_x, step_y = 0, 0
      if ray_dir_x < 0:
        step_x = -1
        side_dist_x = (pos_x - map_x) * delta_dist_x
      else:
        step_x = 1
        side_dist_x = (map_x + 1.0 - pos_x) * delta_dist_x

      if ray_dir_y < 0:
        step_y = -1
        side_dist_y = (pos_y - map_y) * delta_dist_y
      else:
        step_y = 1
        side_dist_y = (map_y + 1.0 - pos_y) * delta_dist_y

      # Perform DDA algorithm
      hit = False
      while not hit:
        # Jump to next map square, either in x-direction, or in y-direction
        if side_dist_x < side_dist_y:
          side_dist_x += delta_dist_x
          map_x += step_x
          side = 0
        else:
          side_dist_y += delta_dist_y
          map_y += step_y
          side = 1
        
        # Check if ray has hit a wall
        if MAP[map_x][map_y] > 0:
          hit = True
          # Calculate distance projected on camera direction
          if side == 0:
            perp_wall_dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
          else:
            perp_wall_dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y
          # Calculate height of line to draw on screen
          line_height = int(SCREENHEIGHT / perp_wall_dist)
          # Calculate lowest and highest pixel to fill in current stripe
          draw_start = -line_height / 2 + SCREENHEIGHT / 2
          if draw_start < 0:
            draw_start = 0
          draw_end = line_height / 2 + SCREENHEIGHT / 2
          if draw_end >= SCREENHEIGHT:
            draw_end = SCREENHEIGHT - 1
          # Choose color based on side
          if MAP[map_x][map_y] == 1:
            color = (255, 0, 0)  # Red
          elif MAP[map_x][map_y] == 2:
            color = (0, 255, 0)  # Green
          elif MAP[map_x][map_y] == 3:
            color = (0, 0, 255)  # Blue
          elif MAP[map_x][map_y] == 4:
            color = (255, 255, 255)  # White
          else:
            color = (255, 255, 0)  # Yellow

          # Give x and y sides different brightness
          if side == 1:
            color = tuple(c // 2 for c in color)

          # Draw the pixels of the stripe as a vertical line
          pygame.draw.line(win, color, (ray, draw_start), (ray, draw_end))

if __name__ == "__main__":
  main()