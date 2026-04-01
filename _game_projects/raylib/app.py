from pyray import *
import math

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

camera_pos = [0, 0, -5]
camera_rot = 0.0

def handle_input(camera_pos, camera_rot):
    global camera
    speed = 0.01
    front = [math.sin(camera_rot), 0.0, math.cos(camera_rot)]
    right = [math.cos(camera_rot), 0.0, -math.sin(camera_rot)]

    if is_key_down(KeyboardKey.KEY_LEFT):
        camera_rot += 0.005
    if is_key_down(KeyboardKey.KEY_RIGHT):
        camera_rot -= 0.005
    if is_key_down(KeyboardKey.KEY_UP):
        camera_pos[0] += front[0] * speed
        camera_pos[2] += front[2] * speed
    if is_key_down(KeyboardKey.KEY_DOWN):
        camera_pos[0] -= front[0] * speed
        camera_pos[2] -= front[2] * speed

    camera.target = Vector3(
        camera_pos[0] + front[0],
        camera_pos[1] + front[1],
        camera_pos[2] + front[2],
    )
    camera.position = Vector3(camera_pos[0], camera_pos[1], camera_pos[2])

    return camera_rot  # camera_pos mutates in place (it's a list), rot needs returning


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


camera = Camera3D(
    [0, 2, -5],
    [0, 0, 0],
    [0, 1, 0],
    45.0,
    CameraProjection.CAMERA_PERSPECTIVE
)

set_config_flags(ConfigFlags.FLAG_MSAA_4X_HINT)
init_window(SCREENWIDTH, SCREENHEIGHT, "Hello")
while not window_should_close():
    camera_rot = handle_input(camera_pos, camera_rot)  # capture returned rot
    begin_drawing()

    clear_background(WHITE)
    draw_map_2d(0, 0)

    begin_mode_3d(camera)
    draw_map_3d()
    end_mode_3d()

    end_drawing()
close_window()