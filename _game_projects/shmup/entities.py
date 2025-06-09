import random
import math
import pygame as pg
from resources import *
from statemachine import *

def is_out_of_bounds(sprite : pg.sprite.Sprite, threshold : int = 64):
        outleft = sprite.rect.right + threshold < 0
        outright = sprite.rect.left - threshold > SCREENWIDTH
        outbottom = sprite.rect.top - threshold > SCREENHEIGHT
        outtop = sprite.rect.bottom + threshold < 0
        return outleft or outright or outbottom or outtop


class Explosion(pg.sprite.Sprite):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        f1 = assets["tile_sheet"].subsurface(pg.Rect(16 * 4, 0, 16, 16)).copy()
        f2 = pg.transform.flip(f1, True, False)
        f3 = assets["tile_sheet"].subsurface(pg.Rect(16 * 7, 0, 16, 16)).copy()
        f4 = assets["tile_sheet"].subsurface(pg.Rect(16 * 8, 0, 16, 16)).copy()
        frames = [f1, f2, f3, f4]
        
        self.last_update = 0
        self.speed = 100
        self.animation = Animation(frames, False)
        self.image = f1
        self.rect = self.image.get_rect(center=position)
    

    def update(self, dt):
        self.image = self.animation.get_frame()
        now = pg.time.get_ticks()
        if now - self.last_update > self.speed:
            has_next_frame = self.animation.animate()
            if not has_next_frame:
                self.kill()
                del self
                return
            self.last_update = now

        


class Bullet(pg.sprite.Sprite):
    """
    Bullet class. TODO - Make flexible and possibly do pooling
    """

    MAX_SPEED = 500
    def __init__(self, source, position : tuple, velocity : tuple, *groups):
        super().__init__(*groups)
        self.enemy_bullet = False
        self.source = source
        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2(velocity)
        self.image = assets["tile_sheet"].subsurface(pg.Rect(0, 0, 16, 16)).copy()
        self.rect = self.image.get_rect(center=self.position)

        if isinstance(source, EnemyShip):
            self.set_enemy_bullet_visual()
            self.enemy_bullet = True

        self.active = True


    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity.clamp_magnitude_ip(self.MAX_SPEED)
        self.rect = self.image.get_rect(center=self.position)

        # check collision
        _coll = self.rect.collideobjects(ship_group.sprites())
        if _coll:
            is_enemy_ship = isinstance(_coll, EnemyShip)
            is_player_ship = isinstance(_coll, PlayerShip)
            if (is_enemy_ship and not self.enemy_bullet) or (is_player_ship and self.enemy_bullet):
                self.destroy()
                _coll.take_damage(2)

        if is_out_of_bounds(self):
            self.destroy()
    

    def set_enemy_bullet_visual(self):
        replacement_color = (255, 0, 0)

        width, height = self.image.get_size()
        for x in range(width):
            for y in range(height):
                if self.image.get_at((x, y))[:3] == (255, 189, 32):
                    self.image.set_at((x, y), replacement_color)
        self.image = pg.transform.flip(self.image, False, True)

    
    def destroy(self):
        self.active = False
        self.kill()


class Ship(pg.sprite.Sprite):
    """
    Common functionality for ships
    """
    ACCEL = 20
    MAX_SPEED = 300.0
    def __init__(self, image : pg.Surface, position : pg.Vector2, *groups):
        super().__init__(*groups)
        self.image = image

        # flash image
        self.original_image = image
        flash_image = image.copy()
        flash_image.fill((255, 255, 255), special_flags=pg.BLEND_RGB_ADD)
        self.flash_image = flash_image
        self.flash_time = 0

        self.position = pg.Vector2(position)
        self.velocity = pg.Vector2()
        self.shooting = False

        # properties
        self.health = 10

        # events
        self.on_destroyed = lambda: ()

        # shooting
        self.last_shot_time = 0
        self.shoot_cd = 100
        self.bullets = []
        self.bullets_to_remove = []


    def get_rect(self):
        return self.image.get_rect(center=self.position)


    def update(self, dt):
        self.position += self.velocity * dt # move
        self.rect = self.get_rect() # set the rect fro drawing and collision

        # flash
        if self.flash_time > pg.time.get_ticks():
            self.image = self.flash_image
        else:
            self.image = self.original_image

        # organise bullets

        for bullet in self.bullets:
            assert isinstance(bullet, Bullet)
            if not bullet.active:
                self.bullets_to_remove.append(bullet)

        for b in self.bullets_to_remove:
            if b in self.bullets:
                self.bullets.remove(b)
                del b

        self.bullets_to_remove.clear()


    def shoot(self):
        bullet = Bullet(self, self.position + pg.Vector2(0, -20), (0, -300) ,bullet_group)
        self.bullets.append(bullet)
    

    def take_damage(self, amount):
        self.flash_time = pg.time.get_ticks() + 50
        self.health -= amount
        if self.health <= 0:
            # explosion before kill to pass the spritegroup
            explosion = Explosion(self.position, self.groups())
            self.kill() # remove sprite
            self.on_destroyed()
            del self


class PlayerShip(Ship):
    def __init__(self, image, position, *groups):
        super().__init__(image, position, *groups)
    

    def update(self, dt):
        self.do_input()
        
        super().update(dt) # movement happens

        self.velocity.clamp_magnitude_ip(self.MAX_SPEED) # clamp max speed
        self.velocity *= 0.9 # damping

        # keep ship within boundaries
        self.position.x = pg.math.clamp(self.position.x, 0 + self.rect.w / 2, SCREENWIDTH - self.rect.w / 2)
        self.position.y = pg.math.clamp(self.position.y, 0 + self.rect.h / 2, SCREENHEIGHT - self.rect.h / 2)

        can_shoot = pg.time.get_ticks() >= self.last_shot_time
        if self.shooting and can_shoot:
            self.shoot()
            self.last_shot_time = pg.time.get_ticks() + self.shoot_cd
    

    def do_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.velocity.x -= self.ACCEL
        elif keys[pg.K_RIGHT]:
            self.velocity.x += self.ACCEL
        if keys[pg.K_UP]:
            self.velocity.y -= self.ACCEL
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.ACCEL
        self.shooting = keys[pg.K_z]


class EnemyShip(Ship):
    """
    Base enemy ship.
    """
    def __init__(self, image, position, *groups):
        flipped_image = pg.transform.flip(image, False, True)
        super().__init__(flipped_image, position, *groups)

        self.shoot_timer = Timer(random.randint(1000, 3000), self.shoot, True, True)

        # state machine setup
        sm = StateMachine(self)
        sm.add_state("zigzag", SweepMovementState(), True)

        self.state_machine = sm
    

    def shoot(self):
        snd : pg.mixer.Sound = assets["shoot_sound"]
        snd.set_volume(0.05)
        snd.play()

        bullet = Bullet(self, self.position + pg.Vector2(0, 32), (0, 100), bullet_group)
        self.bullets.append(bullet)


    def update(self, dt):
        super().update(dt)

        self.shoot_timer.update()
        self.state_machine.update(dt)

        # remove ship when left screen
        if is_out_of_bounds(self):
            print(self, "left screen")
            self.kill()
            del self


#Enemy movement states

class ShipMovementState(State):
    def __init__(self):
        super().__init__()
    

    def get_context(self):
        context = super().get_context()
        assert isinstance(context, EnemyShip)
        return context



class ZigzagMovementState(ShipMovementState):
    def __init__(self, move_left = False):
        super().__init__()
        self.move_dir_x = -1 if move_left else 1
        self.flip_timer = Timer(2000, self.flip_x, True, True)
    
    def update(self, dt):
        self.flip_timer.update()
        ctx = self.get_context()
        ctx.velocity = pg.Vector2(20 * self.move_dir_x, 20)
    
    def flip_x(self):
        self.move_dir_x *= -1


class SweepMovementState(ShipMovementState):
    def __init__(self, move_left = False):
        super().__init__()
        self.move_dir_x = -1 if move_left else 1
        self.time = 0

        # params
        self.x_magnitude = 170
        self.y_magnitude = 0    # make 0 to do a horizontal sweep
        self.x_frequency = 500
        self.y_frequency = 50

        self.const_y = 80       # constant vertical movement
        self.speed = 2          # speed of sin/cos wave traversion
    
    def update(self, dt):
        self.time += self.speed
        x = self.x_magnitude * math.sin(self.time / self.x_frequency)
        y = self.y_magnitude * math.cos(self.time / self.y_frequency)
        ctx = self.get_context()
        ctx.velocity = pg.Vector2(x * self.move_dir_x, self.const_y + y)



class Animation():
    """
    A data class to hold information for an animation
    """
    def __init__(self, frames, loop=True):
        self.frame_index = 0
        self.frames = frames
        self.loop = loop

    
    """
    Load an animation from a sprite sheet
    """
    @classmethod
    def from_spritesheet(cls, sheet, h_frames, v_frames, loop=True):
        frames = []
        img = pg.image.load(sheet).convert_alpha()
        frame_width = img.width // h_frames
        frame_height = img.height // v_frames
        for f_y in range(v_frames):
            for f_x in range(h_frames):
                surf = img.subsurface(pg.Rect(frame_width * f_x, frame_height * f_y, frame_width, frame_height))
                frames.append(surf) 
        return Animation(frames, loop)


    def set_frame(self, index):
        self.frame_index = index


    def get_frame(self):
        return self.frames[self.frame_index]
    

    def animate(self):
        self.frame_index += 1
        if self.frame_index > len(self.frames) - 1:
            self.frame_index = 0
            return False
        return True


class Timer():
    """
    A timer that calls a function on finished.
    {duration} in ms
    """
    def __init__(self, duration, func=None, repeat=False, autostart=False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate()
    

    def __bool__(self):
        return self.active


    def activate(self):
        self.active = True
        self.start_time = pg.time.get_ticks()
    

    def deactivate(self):
        self.active = False
        self.start_time = 0


    def update(self):
        if pg.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
            if self.repeat:
                self.activate()