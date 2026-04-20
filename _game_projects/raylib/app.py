from pyray import *
import math

from player import Player
from collectible import Collectible

SCREENWIDTH = 800
SCREENHEIGHT = 600

gamemap = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def draw_map_2d(pos_x, pos_y):
    for y in range(len(gamemap)):
        for x in range(len(gamemap[y])):
            if gamemap[y][x] == 1:
                draw_rectangle(pos_x + 16 * x, pos_y + 16 * y, 16, 16, BLACK)

def draw_map_3d():
    cmx, cmz = len(gamemap) // 2, len(gamemap[0]) // 2
    draw_plane([cmx, -0.5, cmz], [8, 8], GRAY)

    for y in range(len(gamemap)):
        for x in range(len(gamemap[y])):
            if gamemap[y][x] == 1:
                wall_pos = [x, 0, y]
                draw_cube(wall_pos, 1, 1, 1, RED)
                draw_cube_wires(wall_pos, 1, 1, 1, BLACK)


def draw_crosshair():
    size = 8
    cx, cy = SCREENWIDTH // 2, SCREENHEIGHT // 2
    draw_line(cx - size, cy, cx + size, cy, YELLOW)
    draw_line(cx, cy - size, cx, cy + size, YELLOW)

player = Player(Vector3(3,0,2), gamemap)

set_config_flags(ConfigFlags.FLAG_MSAA_4X_HINT)
init_window(SCREENWIDTH, SCREENHEIGHT, "Hello")
set_target_fps(60)
disable_cursor()

# Collectible test
texture = load_texture("assets/goodies.png")
collectible = Collectible(Vector3(3,-0.25,3), texture)


while not window_should_close():
    player.update()
    collectible.update()
    if check_collision_boxes(player.get_bounding_box(), collectible.get_bounding_box()):
        print("Got collectible")

    begin_drawing()

    clear_background(WHITE)
    draw_map_2d(0, 0)

    begin_mode_3d(player.camera)
    draw_map_3d()
    collectible.draw(player.camera)


    end_mode_3d()

    draw_crosshair()
    # gui items
    gui_text_box(Rectangle(10, 10, 50, 20), "Textbox", 16, False)

    end_drawing()

unload_texture(texture)
close_window()