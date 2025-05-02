import pygame
from camera import Camera

class SpriteGroup(pygame.sprite.Group):
  def __init__(self, *sprites):
    super().__init__(*sprites)
    self.camera = Camera.get_instance()
  
  def draw(self, surface, bgsurf=None, special_flags=0): 
    sprites = self.sprites()

    # Create list of blit instructions
    blit_data = []
    for spr in sprites:
        draw_rect = self.camera.apply(spr.rect)
        blit_data.append((spr.image, draw_rect, None, special_flags))

    # Perform the blits and get the resulting dirty rectangles
    dirty_rects = surface.blits(blit_data)

    # Zip each sprite with its corresponding dirty rect
    sprite_rect_pairs = zip(sprites, dirty_rects)

    # Update the spritedict with this mapping
    self.spritedict.update(sprite_rect_pairs)