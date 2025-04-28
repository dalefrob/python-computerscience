import pygame as pg
from pathlib import Path

FPS = 60

current_path = Path(__file__).parent
clock = pg.time.Clock()


class Player(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load the sprite sheet and extract the player sprite
        image_path = current_path / "tilemap-characters_packed.png"
        region = pg.Rect(0, 0, 24, 24)
        self.rect = region.move(position)
        self.animation_frames = load_animation(image_path, region, 2, 1)
        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]

        self.current_time = 0.0 # For animation timing

        self.speed = 3
        self.velocity = pg.Vector2(0, 0)
        self.is_on_floor = False

    def handle_input(self, keys):
        if keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
        elif keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        if keys[pg.K_UP] and self.is_on_floor:
            self.velocity.y = -10
            self.is_on_floor = False

    def update(self, dt):
        # apply gravity and update position
        if not self.is_on_floor:
            self.velocity.y += 0.5
        else:
            self.velocity.y = 0

        self.rect.y += self.velocity.y
        self.rect.x += self.velocity.x

        # animate the player sprite
        self.current_time += dt
        if self.current_time >= 0.1:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            self.current_time = 0.0


# Load animation frames
def load_animation(image_path, rect, cols, rows):
    image = pg.image.load(image_path).convert_alpha()
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame_rect = pg.Rect(col * rect.width, row * rect.height, rect.width, rect.height)
            frames.append(image.subsurface(frame_rect))
    return frames


class Game:
    def __init__(self):
        pg.init()
        self.displaysurface = pg.display.set_mode((400, 400))
        pg.display.set_caption("Game")
        self.is_running = True

        # Create player
        self.player = Player((100, 100))
        # Create a temporary platform for the player to fall onto
        self.platform = pg.Rect(0, 300, 400, 20)
        self.platform_image = pg.Surface((400, 20))
        self.platform_image.fill((255, 255, 255))

        self.all_sprites = pg.sprite.Group(self.player)


    def handle_collisions(self):
        # Check for collision between the player and the platform
        if self.player.rect.colliderect(self.platform):
            self.player.rect.y > self.platform.top - self.player.rect.height
            # adjust the player's position to be on top of the platform
            self.player.rect.y = self.platform.top - self.player.rect.height
            self.player.is_on_floor = True


    def run(self):
        while self.is_running:
            dt = clock.tick(FPS) / 1000
            
            self.player.handle_input(pg.key.get_pressed())
            self.all_sprites.update(dt)

            # Handle collisions
            self.handle_collisions()

             # Clear the screen
            self.displaysurface.fill((0, 0, 0))
            self.displaysurface.blit(self.platform_image, self.platform.topleft)
            self.all_sprites.draw(self.displaysurface)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()