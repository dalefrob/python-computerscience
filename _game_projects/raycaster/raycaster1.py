"""
Raycaster - Python/Pygame+PyOpenGL port of 3DSage's C raycaster tutorial
Original: https://www.youtube.com/watch?v=gYRrGTC7GtA
Controls: WASD to move/rotate player, ESC to quit
"""

import math
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ─────────────────────────────────────────
#  MAP
# ─────────────────────────────────────────
MAP_COLS   = 8   # number of columns in the map grid
MAP_ROWS   = 8   # number of rows    in the map grid
CELL_SIZE  = 64  # pixel size of each map cell (must be a power of 2 for bit-shifts)

MAP = [
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1,
]


def draw_map_2d():
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            if MAP[row * MAP_COLS + col] == 1:
                glColor3f(1, 1, 1)   # wall  → white
            else:
                glColor3f(0, 0, 0)   # floor → black
            # pixel origin of this cell
            cell_left = col * CELL_SIZE
            cell_top  = row * CELL_SIZE
            glBegin(GL_QUADS)
            glVertex2i(cell_left            + 1, cell_top             + 1)
            glVertex2i(cell_left            + 1, cell_top + CELL_SIZE - 1)
            glVertex2i(cell_left + CELL_SIZE - 1, cell_top + CELL_SIZE - 1)
            glVertex2i(cell_left + CELL_SIZE - 1, cell_top             + 1)
            glEnd()


# ─────────────────────────────────────────
#  PLAYER
# ─────────────────────────────────────────
player = {
    "x":     150.0,   # pixel position X
    "y":     400.0,   # pixel position Y
    "angle":  90,     # facing angle in degrees (0 = right, 90 = up)
    "dir_x":  0.0,    # unit direction vector X  (cos of angle)
    "dir_y":  0.0,    # unit direction vector Y (-sin of angle, Y grows downward)
}


def deg_to_rad(degrees):
    return degrees * math.pi / 180.0


def clamp_angle(angle):
    """Keep angle in the [0, 359] range."""
    if angle > 359: angle -= 360
    if angle < 0:   angle += 360
    return angle


def update_direction():
    """Recalculate the direction vector from the current angle."""
    player["dir_x"] =  math.cos(deg_to_rad(player["angle"]))
    player["dir_y"] = -math.sin(deg_to_rad(player["angle"]))  # negative: screen Y is flipped


update_direction()


def draw_player_2d():
    px, py = player["x"], player["y"]
    glColor3f(1, 1, 0)   # yellow
    glPointSize(8)
    glLineWidth(4)
    # dot at player position
    glBegin(GL_POINTS)
    glVertex2i(int(px), int(py))
    glEnd()
    # short line showing facing direction
    glBegin(GL_LINES)
    glVertex2i(int(px), int(py))
    glVertex2i(int(px + player["dir_x"] * 20), int(py + player["dir_y"] * 20))
    glEnd()


def handle_keys():
    keys = pygame.key.get_pressed()
    if keys[K_a]:   # rotate left
        player["angle"] = clamp_angle(player["angle"] + 5)
        update_direction()
    if keys[K_d]:   # rotate right
        player["angle"] = clamp_angle(player["angle"] - 5)
        update_direction()
    if keys[K_w]:   # move forward
        player["x"] += player["dir_x"] * 5
        player["y"] += player["dir_y"] * 5
    if keys[K_s]:   # move backward
        player["x"] -= player["dir_x"] * 5
        player["y"] -= player["dir_y"] * 5


# ─────────────────────────────────────────
#  RAYCASTING
# ─────────────────────────────────────────
# Number of rays equals the width of the 3-D viewport in "columns".
# Each ray sweeps 1° so the total FOV is 60°.
RAY_COUNT = 60   # one ray per screen column in the 3-D view
FOV_HALF  = 30   # rays span from (player_angle + 30) to (player_angle - 30)

# Screen-space constants for the 3-D viewport
VIEW_LEFT    = 526   # left edge of the 3-D viewport (pixels)
VIEW_MID_Y   = 160   # vertical midpoint / horizon line
VIEW_BOTTOM  = 320   # bottom of the 3-D viewport
VIEW_RIGHT   = 1006  # right edge of the 3-D viewport
COLUMN_WIDTH = 8     # pixel width of each rendered wall column


def draw_rays_and_walls():
    player_x    = player["x"]
    player_y    = player["y"]
    player_angle = player["angle"]

    # ── Sky (cyan) and floor (blue) background quads ────────────────────────
    glColor3f(0, 1, 1)
    glBegin(GL_QUADS)
    glVertex2i(VIEW_LEFT,  0);         glVertex2i(VIEW_RIGHT,  0)
    glVertex2i(VIEW_RIGHT, VIEW_MID_Y); glVertex2i(VIEW_LEFT, VIEW_MID_Y)
    glEnd()
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex2i(VIEW_LEFT,  VIEW_MID_Y);  glVertex2i(VIEW_RIGHT, VIEW_MID_Y)
    glVertex2i(VIEW_RIGHT, VIEW_BOTTOM); glVertex2i(VIEW_LEFT,  VIEW_BOTTOM)
    glEnd()

    # Start the first ray at FOV_HALF degrees to the LEFT of the player's gaze
    ray_angle = clamp_angle(player_angle + FOV_HALF)

    for ray_index in range(RAY_COUNT):

        cos_ray = math.cos(deg_to_rad(ray_angle))
        sin_ray = math.sin(deg_to_rad(ray_angle))
        # tan of the ray angle — used to step along grid lines
        tan_ray = math.tan(deg_to_rad(ray_angle))

        # ── VERTICAL WALL CHECK ─────────────────────────────────────────────
        # Step along vertical grid lines (x = 0, 64, 128 …) until we hit a wall.
        steps_taken     = 0
        dist_vertical   = 100000.0   # large sentinel = no hit yet

        if cos_ray > 0.001:          # ray faces RIGHT → first grid line is to the right
            hit_x = (int(player_x) >> 6 << 6) + CELL_SIZE   # next vertical line (right)
            hit_y = (player_x - hit_x) * tan_ray + player_y
            step_x =  CELL_SIZE
            step_y = -step_x * tan_ray
        elif cos_ray < -0.001:       # ray faces LEFT → first grid line is to the left
            hit_x = (int(player_x) >> 6 << 6) - 0.0001      # next vertical line (left)
            hit_y = (player_x - hit_x) * tan_ray + player_y
            step_x = -CELL_SIZE
            step_y = -step_x * tan_ray
        else:                        # ray is perfectly horizontal → will never cross a vertical line
            hit_x, hit_y = player_x, player_y
            steps_taken  = 8         # skip the loop

        while steps_taken < 8:
            map_col = int(hit_x) >> 6   # which map column does this pixel fall in?
            map_row = int(hit_y) >> 6   # which map row?
            map_idx = map_row * MAP_COLS + map_col
            if 0 < map_idx < MAP_COLS * MAP_ROWS and MAP[map_idx] == 1:
                steps_taken  = 8    # wall found — stop stepping
                dist_vertical = cos_ray * (hit_x - player_x) - sin_ray * (hit_y - player_y)
            else:
                hit_x += step_x     # advance to the next vertical grid line
                hit_y += step_y
                steps_taken += 1

        # Remember the vertical-hit coordinates so we can compare later
        vert_hit_x, vert_hit_y = hit_x, hit_y

        # ── HORIZONTAL WALL CHECK ───────────────────────────────────────────
        # Step along horizontal grid lines (y = 0, 64, 128 …) until we hit a wall.
        steps_taken      = 0
        dist_horizontal  = 100000.0

        # Reciprocal of tan_ray — used for stepping in the X direction
        inv_tan = (1.0 / tan_ray) if abs(tan_ray) > 1e-10 else 1e10 * (1 if tan_ray >= 0 else -1)

        if sin_ray > 0.001:          # ray faces UP (screen Y decreases)
            hit_y = (int(player_y) >> 6 << 6) - 0.0001
            hit_x = (player_y - hit_y) * inv_tan + player_x
            step_y = -CELL_SIZE
            step_x = -step_y * inv_tan
        elif sin_ray < -0.001:       # ray faces DOWN (screen Y increases)
            hit_y = (int(player_y) >> 6 << 6) + CELL_SIZE
            hit_x = (player_y - hit_y) * inv_tan + player_x
            step_y =  CELL_SIZE
            step_x = -step_y * inv_tan
        else:                        # ray is perfectly vertical → will never cross a horizontal line
            hit_x, hit_y = player_x, player_y
            steps_taken  = 8

        while steps_taken < 8:
            map_col = int(hit_x) >> 6
            map_row = int(hit_y) >> 6
            map_idx = map_row * MAP_COLS + map_col
            if 0 < map_idx < MAP_COLS * MAP_ROWS and MAP[map_idx] == 1:
                steps_taken     = 8
                dist_horizontal = cos_ray * (hit_x - player_x) - sin_ray * (hit_y - player_y)
            else:
                hit_x += step_x
                hit_y += step_y
                steps_taken += 1

        # ── PICK THE CLOSER HIT ─────────────────────────────────────────────
        # Vertical walls get a brighter green; horizontal walls are slightly darker.
        glColor3f(0, 0.8, 0)         # bright green = horizontal wall hit
        if dist_vertical < dist_horizontal:
            hit_x, hit_y    = vert_hit_x, vert_hit_y
            dist_horizontal = dist_vertical
            glColor3f(0, 0.6, 0)     # darker green = vertical wall hit

        # Draw the 2-D ray line on the mini-map
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2i(int(player_x), int(player_y))
        glVertex2i(int(hit_x),    int(hit_y))
        glEnd()

        # ── DRAW THE 3-D WALL COLUMN ────────────────────────────────────────
        # Correct fish-eye distortion: the true wall distance is the perpendicular
        # distance, not the straight-line distance to the hit point.
        angle_diff   = clamp_angle(player_angle - ray_angle)
        true_dist    = dist_horizontal * math.cos(deg_to_rad(angle_diff))

        # Wall height is inversely proportional to distance
        wall_height  = int((CELL_SIZE * VIEW_BOTTOM) / true_dist) if true_dist > 0 else VIEW_BOTTOM
        wall_height  = min(wall_height, VIEW_BOTTOM)              # clamp so it never exceeds viewport

        # Centre the wall column vertically around the horizon line
        wall_top     = VIEW_MID_Y - (wall_height >> 1)

        screen_col_x = ray_index * COLUMN_WIDTH + VIEW_LEFT + 4   # +4 centres the 8-px line

        glLineWidth(COLUMN_WIDTH)
        glBegin(GL_LINES)
        glVertex2i(screen_col_x, wall_top)
        glVertex2i(screen_col_x, wall_top + wall_height)
        glEnd()

        ray_angle = clamp_angle(ray_angle - 1)   # sweep one degree to the right


# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────
def main():
    pygame.init()
    pygame.display.set_mode((1024, 510), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Raycaster - Pygame/PyOpenGL")

    glClearColor(0.3, 0.3, 0.3, 0)
    gluOrtho2D(0, 1024, 510, 0)   # 2-D orthographic projection, Y=0 at the top

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit(); sys.exit()

        handle_keys()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_map_2d()
        draw_player_2d()
        draw_rays_and_walls()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()