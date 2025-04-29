import pygame as pg
from tilemap import Tilemap

def load_animation_frames(sprite_sheet, x, y, frame_size, frame_count):
    frames = []
    for i in range(frame_count):
      frame = sprite_sheet.subsurface(x + (i * frame_size), y, frame_size, frame_size)
      frames.append(frame)
    return frames


def point_in_rect(point_x, point_y, rect : pg.Rect):
    return (
        rect.left <= point_x <= rect.right and
        rect.top <= point_y <= rect.bottom
    )


def resolve_tilemap_collision(other_rect: pg.Rect, tilemap : Tilemap):
    tilesize = tilemap.get_tilesize()

    top_left = tilemap.world_to_map(other_rect.left, other_rect.top)
    bottom_right = tilemap.world_to_map(other_rect.right, other_rect.bottom)

    total_push = pg.Vector2(0,0)
    total_normal = pg.Vector2(0,0)

    # check tiles that surround the rect
    for ty in range(top_left[1], bottom_right[1] + 1):
        for tx in range(top_left[0], bottom_right[0] + 1):
            tile_id = tilemap.get_tile_id_at(tx, ty)

            if tile_id == 0:
                continue

            tile = tilemap.tileset.get_tile_by_id(tile_id)

            # Only full blocks for now
            shape_name = tile.data.get("shape", "full")
            if shape_name != "full":
                continue  # TODO: Handle slopes later

            tile_rect = pg.Rect(tx * tilesize, ty * tilesize, tilesize, tilesize)

            # Check collision
            collision = get_aabb_collision(other_rect, tile_rect)
            if collision:
                push_vector, normal = collision
                total_push += push_vector
                total_normal += normal
            # Avoid stacking y push to stop bouncing
            if total_normal.y < 0:
                total_push.y = -1

    if total_push.length_squared() > 0:
        return total_push, total_normal.normalize()
    else:
      return None


def get_aabb_collision(rect1 : pg.Rect, rect2 : pg.Rect):
    # Calculate how much rect1 is overlapping rect2
    dx = (rect1.centerx - rect2.centerx)
    dy = (rect1.centery - rect2.centery)
    
    overlap_x = (rect1.width / 2 + rect2.width / 2) - abs(dx)
    overlap_y = (rect1.height / 2 + rect2.height / 2) - abs(dy)

    if overlap_x <= 0 or overlap_y <= 0:
        # No collision!
        return None

    # Now figure out which axis to push along (smallest overlap wins)
    if overlap_x < overlap_y:
        # Push horizontally
        if dx > 0:
            normal = pg.Vector2(1, 0)  # rect1 is to the right → push right
        else:
            normal = pg.Vector2(-1, 0)  # rect1 is to the left → push left
        penetration = overlap_x
    else:
        # Push vertically
        if dy > 0:
            normal = pg.Vector2(0, 1)  # rect1 is below → push down
        else:
            normal = pg.Vector2(0, -1)  # rect1 is above → push up
        penetration = overlap_y

    # The minimum push vector
    push_vector = normal * penetration

    return push_vector, normal


def is_point_in_polygon(x, y, polygon):
  """
  Algorithm to check if a point is within a polygon by raycasting
  a horizontal line across the polygon and counting the intersections.
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