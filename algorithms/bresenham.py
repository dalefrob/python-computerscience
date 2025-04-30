import pygame
import math
import sys

vec2 = pygame.math.Vector2

# BTW
# '*' unpacks the tuple arguments, like in *args

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bresenham Line Drawing")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fill background
screen.fill(WHITE)

clock = pygame.time.Clock()

wall = pygame.Rect(100, 100, 20, 20)
obstacles = [wall] # expand this to add more obstacles

def draw_line(x0, y0, x1, y1, screen):
  delta_x = x1 - x0
  delta_y = y1 - y0
  step = max(abs(delta_x), abs(delta_y)) # Which is the longest distance to travel?
  if step != 0:
    step_x = delta_x / step
    step_y = delta_y / step
    for i in range(step + 1):
      x = int(x0 + i * step_x)
      y = int(y0 + i * step_y)
      pygame.draw.circle(screen, "white", (x, y), 1)

def draw_line_bresenham(x1, y1, x2, y2, color):
    """
    Draws a line between two points (x1, y1) and (x2, y2) using Bresenham's line algorithm.
    Bresenham's algorithm is an efficient way to calculate and draw a straight line 
    between two points in a grid-based system, such as a pixel-based screen.
    Parameters:
        x1 (int): The x-coordinate of the starting point.
        y1 (int): The y-coordinate of the starting point.
        x2 (int): The x-coordinate of the ending point.
        y2 (int): The y-coordinate of the ending point.
        color (tuple): The color of the line, typically represented as an RGB tuple.
    Steps:
        1. Cast the input coordinates to integers to ensure proper grid alignment.
        2. Calculate the absolute differences in the x and y directions (dx, dy).
        3. Determine the step direction (sx, sy) for x and y based on the relative positions 
           of the start and end points.
        4. Initialize the decision variable `err` to half of the larger difference (dx or dy).
        5. Depending on whether the line is more horizontal (dx > dy) or vertical (dy >= dx):
           - Iterate through the grid points along the dominant axis (x or y).
           - Draw a pixel at the current position using `pygame.draw.circle`.
           - Adjust the decision variable `err` by subtracting the smaller difference (dy or dx).
           - If the decision variable becomes negative, adjust the secondary axis (y or x) 
             and reset `err` by adding the larger difference (dx or dy).
        6. Continue until the end point (x2, y2) is reached.
        7. Draw the final point to ensure the line is complete.
    Note:
        This function uses `pygame.draw.circle` to draw individual pixels on the screen. 
        Ensure that the `screen` object is properly initialized in your Pygame environment 
        before calling this function.
    """

    # cast to integers
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # Calculate differences
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Determine the direction of step (+1 or -1)
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    # Decision variable
    if dx > dy:
        err = dx / 2.0
        while x1 != x2:
            pygame.draw.circle(screen, color, (x1, y1), 1)
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
    else:
        err = dy / 2.0
        while y1 != y2:
            pygame.draw.circle(screen, color, (x1, y1), 1)
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy

    # Draw the final point
    pygame.draw.circle(screen, color, (x2, y2), 1)

def bresenham_collision_detection(start_x, start_y, end_x, end_y):
    # Cast coordinates to integers
    start_x = int(start_x)
    start_y = int(start_y)
    end_x = int(end_x)
    end_y = int(end_y)

    # Calculate horizontal and vertical distances
    delta_x = abs(end_x - start_x)
    delta_y = abs(end_y - start_y)

    # Determine step direction along each axis (+1 or -1)
    step_x = 1 if end_x >= start_x else -1
    step_y = 1 if end_y >= start_y else -1

    collision_detected = False

    # Determine which axis is dominant
    if delta_x > delta_y:
        error_term = delta_x / 2.0
        while start_x != end_x:
            if any(obstacle.collidepoint(start_x, start_y) for obstacle in obstacles):
                collision_detected = True
                break
            pygame.draw.circle(screen, BLACK, (start_x, start_y), 1)
            error_term -= delta_y
            if error_term < 0:
                start_y += step_y
                error_term += delta_x
            start_x += step_x
    else:
        error_term = delta_y / 2.0
        while start_y != end_y:
            if any(obstacle.collidepoint(start_x, start_y) for obstacle in obstacles):
                collision_detected = True
                break
            pygame.draw.circle(screen, BLACK, (start_x, start_y), 1)
            error_term -= delta_x
            if error_term < 0:
                start_x += step_x
                error_term += delta_y
            start_y += step_y

    # Draw the final point
    pygame.draw.circle(screen, BLACK, (end_x, end_y), 1)
    return collision_detected


# Example points
start_point = vec2(250, 250)
end_point = vec2(500, 0)

# Main game loop
running = True
time_elapsed = 0

while running:
    dt = clock.tick(60) / 1000.0  # Seconds since last frame (limit to 60 FPS)
    time_elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # draw obstacles
    pygame.draw.rect(screen, (255, 0, 0), wall)

    length = 300 # math.sin(time_elapsed * 1.7) * 400
    # Update endpoint with slow-moving sine/cosine animation
    end_point.x = 250 - math.sin(time_elapsed) * length
    end_point.y = 250 + math.cos(time_elapsed) * length

    # Draw the line
    if bresenham_collision_detection(start_point.x, start_point.y, end_point.x, end_point.y):
        print("Hit a wall!")
    pygame.display.update()


# Quit Pygame
pygame.quit()
sys.exit()
