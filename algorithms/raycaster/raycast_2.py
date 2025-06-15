import pygame
import sys
import math
import os

MAPWIDTH = 24
MAPHEIGHT = 24
SCREENWIDTH = 640
SCREENHEIGHT = 480

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

textures = {}

RENDER_WIDTH = SCREENWIDTH // 2
MAX_RAY_LENGTH = 20.0  # Maximum distance a ray can travel

def main():
    pos_x, pos_y = 22, 12
    dir_x, dir_y = -1, 0
    plane_x, plane_y = 0, 0.66
    time = 0.0
    old_time = 0.0

    pygame.init()
    win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption('Raycaster')

    # Load textures
    texture_dir = os.path.join(os.path.dirname(__file__), 'textures')
    textures[1] = pygame.image.load(
        os.path.join(texture_dir, 'wall.png')).convert()

    clock = pygame.time.Clock()

    buffer = pygame.Surface((RENDER_WIDTH, SCREENHEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Clear the screen
        buffer.fill((0, 0, 0))

        # Calculate time difference
        new_time = pygame.time.get_ticks()
        time = (new_time - old_time) / 1000.0
        old_time = new_time

        drawrays(pos_x, pos_y, dir_x, dir_y, plane_x, plane_y, buffer, RENDER_WIDTH)

        # Scale the buffer to fit the screen
        scaled_buffer = pygame.transform.scale(buffer, (SCREENWIDTH, SCREENHEIGHT))
        win.blit(scaled_buffer, (0, 0))

        move_speed = 5.0 * time
        rot_speed = 2.0 * time

        # Handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            new_dir_x = dir_x * \
                math.cos(rot_speed) - dir_y * math.sin(rot_speed)
            new_dir_y = dir_x * \
                math.sin(rot_speed) + dir_y * math.cos(rot_speed)
            dir_x, dir_y = new_dir_x, new_dir_y

            new_plane_x = plane_x * \
                math.cos(rot_speed) - plane_y * math.sin(rot_speed)
            new_plane_y = plane_x * \
                math.sin(rot_speed) + plane_y * math.cos(rot_speed)
            plane_x, plane_y = new_plane_x, new_plane_y
        elif keys[pygame.K_RIGHT]:
            new_dir_x = dir_x * \
                math.cos(-move_speed) - dir_y * math.sin(-move_speed)
            new_dir_y = dir_x * \
                math.sin(-move_speed) + dir_y * math.cos(-move_speed)
            dir_x, dir_y = new_dir_x, new_dir_y

            new_plane_x = plane_x * \
                math.cos(-move_speed) - plane_y * math.sin(-move_speed)
            new_plane_y = plane_x * \
                math.sin(-move_speed) + plane_y * math.cos(-move_speed)
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


def drawrays(player_x, player_y, player_dir_x, player_dir_y, camera_plane_x, camera_plane_y, surface, render_width):
    texture_width = textures[1].get_width()
    texture_height = textures[1].get_height()
    buffer_height = surface.get_height()
    for screen_column in range(render_width):
        camera_offset = 2 * screen_column / float(render_width) - 1
        ray_dir_x = player_dir_x + camera_plane_x * camera_offset
        ray_dir_y = player_dir_y + camera_plane_y * camera_offset

        map_grid_x = int(player_x)
        map_grid_y = int(player_y)

        delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else float('inf')
        delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else float('inf')

        if ray_dir_x < 0:
            step_x = -1
            side_dist_x = (player_x - map_grid_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_grid_x + 1.0 - player_x) * delta_dist_x

        if ray_dir_y < 0:
            step_y = -1
            side_dist_y = (player_y - map_grid_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_grid_y + 1.0 - player_y) * delta_dist_y

        wall_hit = False
        while not wall_hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_grid_x += step_x
                side_hit = 0
            else:
                side_dist_y += delta_dist_y
                map_grid_y += step_y
                side_hit = 1
            if MAP[map_grid_x][map_grid_y] > 0:
                wall_hit = True

        # --- CRITICAL: Use perpendicular wall distance ---
        if side_hit == 0:
            perp_wall_dist = (map_grid_x - player_x + (1 - step_x) / 2) / ray_dir_x
        else:
            perp_wall_dist = (map_grid_y - player_y + (1 - step_y) / 2) / ray_dir_y
        if perp_wall_dist == 0:
            perp_wall_dist = 0.0001

        wall_slice_height = int(buffer_height / perp_wall_dist)
        draw_start_y = int(-wall_slice_height / 2 + buffer_height / 2)
        if draw_start_y < 0:
            draw_start_y = 0
        draw_end_y = int(wall_slice_height / 2 + buffer_height / 2)
        if draw_end_y >= buffer_height:
            draw_end_y = buffer_height - 1

        # --- Texture mapping using perpendicular distance ---
        if side_hit == 0:
            wall_hit_x = player_y + perp_wall_dist * ray_dir_y
        else:
            wall_hit_x = player_x + perp_wall_dist * ray_dir_x
        wall_hit_x -= int(wall_hit_x)

        texture_x = int(wall_hit_x * texture_width)
        if (side_hit == 0 and ray_dir_x > 0) or (side_hit == 1 and ray_dir_y < 0):
            texture_x = texture_width - texture_x - 1
        texture_x = min(max(texture_x, 0), texture_width - 1)

        wall_type = MAP[map_grid_x][map_grid_y]
        wall_texture = textures[1]

        # Draw the wall slice using blit for speed, with centering fix
        texture_column = wall_texture.subsurface((texture_x, 0, 1, texture_height))
        scaled_column = pygame.transform.scale(texture_column, (1, wall_slice_height))
        if side_hit == 1:
            arr = pygame.surfarray.pixels3d(scaled_column)
            arr //= 2
            del arr

        # Center the texture slice if it's taller than the buffer
        if wall_slice_height > buffer_height:
            y_offset = (wall_slice_height - buffer_height) // 2
            surface.blit(scaled_column, (screen_column, 0), area=pygame.Rect(0, y_offset, 1, buffer_height))
        else:
            # Clamp draw_start_y to 0 if negative
            surface.blit(scaled_column, (screen_column, max(draw_start_y, 0)))


if __name__ == "__main__":
    main()
