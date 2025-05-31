import pygame as pg

class Animation():
    """
    A data class to hold information for an animation
    """
    def __init__(self, image, h_frames, v_frames, loop=True):
        self.frame_index = 0
        self.frames = []
        self.loop = True

        img = pg.image.load(image).convert_alpha()
        frame_width = img.width // h_frames
        frame_height = img.height // v_frames
        for f_y in range(v_frames):
            for f_x in range(h_frames):
                surf = img.subsurface(pg.Rect(frame_width * f_x, frame_height * f_y, frame_width, frame_height))
                self.frames.append(surf)


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


    def __getitem__(self, index):
        """
        Allows use of square brackets to access frames
        """
        return self.frames[index]


    def __len__(self):
         return len(self.frames)


class AnimationPlayer():
    def __init__(self, default_animation = None):
        self.animations = {}
        self.current_animation = None

        if default_animation:
            self.current_animation = "default"
            self.add_animation("default", default_animation)

        self.last_update = 0
        self.speed = 60

        self.loop = True
        self.playing = True

        # callbacks
        self.on_animation_finished = lambda: ()
        self.on_animation_changed = lambda: ()
    

    def add_animation(self, alias, animation : Animation, set_current=False):
        if alias not in self.animations:
            self.animations[alias] = animation
            if set_current:
                self.current_animation = alias
    

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.speed and self.playing:
            current_anim = self.get_current_animation()
            has_next_frame = current_anim.animate()

            if not has_next_frame:
                self.on_animation_finished()
                if not current_anim.loop:
                    self.playing = False

            self.last_update = now
    

    def change_animation(self, next_animation_name, force=False):
        if self.current_animation != next_animation_name or force:
            self.frame_index = 0
            self.current_animation = next_animation_name
            self.on_animation_changed()


    def get_current_animation(self) -> Animation:
        return self.animations[self.current_animation]


    def get_surface(self) -> pg.Surface:
        return self.get_current_animation().get_frame()


class Timer():
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