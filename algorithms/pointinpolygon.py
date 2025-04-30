import pygame
import sys

#game window
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Polygon Check')
clock = pygame.time.Clock()

def is_point_in_polygon(x, y, polygon):
    """
    Determines if a point is inside a given polygon using the ray-casting algorithm.
    Args:
        x (float): The x-coordinate of the point to test.
        y (float): The y-coordinate of the point to test.
        polygon (list of tuple): A list of (x, y) tuples representing the vertices of the polygon
                                 in order (either clockwise or counterclockwise).
    Returns:
        bool: True if the point (x, y) is inside the polygon, False otherwise.
    Algorithm:
        1. Initialize a variable `inside` to False. This will track whether the point is inside the polygon.
        2. Loop through each edge of the polygon:
           - For each edge, consider two consecutive vertices (xi, yi) and (xj, yj).
           - Check if the y-coordinate of the point lies between the y-coordinates of the edge's endpoints.
             This determines if the horizontal ray from the point intersects the edge.
        3. If the ray intersects the edge, calculate the x-coordinate of the intersection point.
           - Use the formula for a line segment to find the x-coordinate of the intersection.
           - If the x-coordinate of the point is less than the intersection point, toggle the `inside` variable.
        4. Repeat the process for all edges of the polygon.
        5. Return the value of `inside`. If `inside` is True, the point is inside the polygon; otherwise, it is outside.
    Notes:
        - The algorithm assumes the polygon is simple (no self-intersections).
        - The polygon can be convex or concave.
        - Points on the boundary of the polygon may be considered outside depending on the implementation.
    """
    num = len(polygon)
    j = num - 1
    inside = False

    for i in range(num):
        xi, yi = polygon[i] # point a
        xj, yj = polygon[j] # point a - 1 (previous point)
        if ((yi > y) != (yj > y)):
            x_intersect = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < x_intersect:
                inside = not inside
        j = i

    return inside

# polygon
points = [(2,0), (6,1), (7,5), (3,7), (0,2)]
# Scale up the points by 10
transformed_points = [((x * 20)+100, (y * 20)+100) for x, y in points]

# Main game loop
running = True
time_elapsed = 0

while running:
    dt = clock.tick(60) / 1000.0  # Seconds since last frame (limit to 60 FPS)
    time_elapsed += dt

    screen.fill("white")
    pygame.draw.polygon(screen, "black", transformed_points)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          # Check for mouse button (1 for left click, 2 for middle click, 3 for right click)
          if event.button == 1:  # Left mouse button
              mouse_pos = pygame.mouse.get_pos()  # Get mouse position
              if is_point_in_polygon(*mouse_pos, transformed_points):
                  print("Is inside polygon!")
                  pygame.draw.polygon(screen, "red", transformed_points)
    
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
