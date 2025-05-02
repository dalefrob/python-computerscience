# An intermediate project to teach classes and instantiation

import pygame as pg

# ----

class Block(pg.sprite.Sprite):
  def __init__(self, x, y, color):
    super().__init__()
    self.image = pg.Surface([20, 20])
    self.image.fill(color)
    
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def set_color(self, color : tuple):
      self.image.fill(color)


class Ball(pg.sprite.Sprite):
  def __init__(self):
    super().__init__()

   # Create transparent surface with a white circle
    self.image = pg.Surface((10, 10), pg.SRCALPHA)
    pg.draw.circle(self.image, (255, 255, 255), (5, 5), 5)

    # Setup rect and position
    self.rect = self.image.get_rect(center=(300, 100))

    # Movement setup
    self.position = pg.math.Vector2(self.rect.center)
    self.direction = pg.math.Vector2(1.0, 1.0)
    self.speed = 2.0

  
  def update(self):
    velocity = self.direction.normalize() * self.speed
    self.position += velocity
    self.rect.center = (round(self.position.x), round(self.position.y))
    self.bounce()
  

  def bounce(self):
    x, y = self.rect.center
    if not (0 < x < 400):
        self.direction.x *= -1
    if not (0 < y < 400):
        self.direction.y *= -1

class Paddle(pg.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pg.Surface([50, 10])
    self.image.fill((0, 200, 200))
    
    self.rect = self.image.get_rect()
    self.rect.topleft = (200, 380)

  def handle_keys(self):
      key = pg.key.get_pressed()
      if key[pg.K_RIGHT]: 
          self.rect.x += 2 
      elif key[pg.K_LEFT]:
          self.rect.x -= 2 

# ----

pg.init()
screen = pg.display.set_mode((400, 400))
pg.display.set_caption("Hello PyGame!")

# font
font = pg.font.SysFont(None, 48)
text_surface = None

# clock
FPS = 60
clock = pg.time.Clock()

# sprites

block_sprites = pg.sprite.Group()

for i in range(10):
   block = Block(30 * i + 20, 50, "yellow")
   block_sprites.add(block)

ball = Ball()
paddle = Paddle()


# test
color = (200, 0, 0)
g = 0


def ball_block_collision(block : Block, ball : Ball):
    dx_left = abs(ball.rect.right - block.rect.left) # depth into left of block
    dx_right = abs(ball.rect.left - block.rect.right) # depth into right of block
    dy_top = abs(ball.rect.bottom - block.rect.top) # depth into the top
    dy_bottom = abs(ball.rect.top - block.rect.bottom) # depth into the bottom

    # Find smallest overlap to decide axis of bounce
    if min(dx_left, dx_right) < min(dy_top, dy_bottom):
        ball.direction.x *= -1
    else:
        ball.direction.y *= -1


running = True
while running:
  g = g + 1 if g < 255 else 0
  screen.fill(color)

  pg.draw.circle(screen, (0, 0, g), (200, 200), 20)
  pg.draw.circle(screen, (0, g, 0), (200, 200), 10)
  # draw text
  fps = clock.get_fps()
  text_surface = font.render(f"FPS: {fps:.2f}", True, "white")
  screen.blit(text_surface, (100, 100))

  #input
  paddle.handle_keys()

  # sprites
  ball.update()
  paddle.update()

  blocks_hit_list : list[Block] = pg.sprite.spritecollide(ball, block_sprites, True)
  for block in blocks_hit_list:
    ball_block_collision(block, ball)

  # paddles  
  if ball.rect.colliderect(paddle.rect):
    ball.direction.y = -1
    ball.speed += 0.25

  block_sprites.draw(screen)

  screen.blit(ball.image, ball.rect)
  screen.blit(paddle.image, paddle.rect)

  pg.display.flip()

  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

  
  clock.tick(FPS)

pg.quit()