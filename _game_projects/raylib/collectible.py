from pyray import *

class Collectible:
    def __init__(self, position : Vector3, texture : Texture):
        self.position = position
        self.texture = texture
        self.scale = 1.0 / 8
        self.frames = [
            Rectangle(0, 48, 16, 16),
            Rectangle(0, 64, 16, 16)
        ]
        self.frame = 0
        self.frame_delay = 0.5
        self.frame_time = 0.5
    
    def get_bounding_box(self):
        min = vector3_add(self.position, Vector3(-0.1, -0.1, -0.1))
        max = vector3_add(self.position, Vector3(0.1, 0.1, 0.1))
        return BoundingBox(min, max)

    def update(self):
        dt = get_frame_time()
        self.frame_time -= dt
        if self.frame_time <= 0:
            self.frame_time = self.frame_delay
            self.frame = (self.frame + 1) % len(self.frames)


    def draw(self, camera):
        source_rect = self.frames[self.frame]  # x, y, width, height in pixels
        draw_billboard_rec(camera, self.texture, source_rect, self.position, Vector2(self.scale, self.scale), WHITE)
        draw_bounding_box(self.get_bounding_box(), ORANGE)
