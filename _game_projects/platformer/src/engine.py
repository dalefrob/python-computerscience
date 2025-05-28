import pygame as pg


class Animation():
    """
    A data class to hold information for an animation
    """
    def __init__(self, frames, loop = True, finished_callback = lambda: ()):
        self.frames = frames
        self.frame_index = 0

        self.last_update = 0
        self.speed = 60

        self.loop = True
        self.playing = True
        self.on_animation_finished = finished_callback # TODO - Create a reusuable observer pattern

    def get_animation_frame(self):
        return self.frames[self.frame_index]


    def play(self, restart=False):
        self.playing = True
        if restart:
            self.frame_index = 0


    def update(self, dt):
        now = pg.time.get_ticks()
        if now - self.last_update > self.speed and self.playing:  # 700 ms
            self.animate(dt)
            self.last_update = now  # Reset the timer


    def animate(self, dt):
        self.frame_index += 1
        if self.frame_index > len(self.frames) - 1:
            self.on_animation_finished()
            if self.loop:
                self.frame_index = 0
            else:
                self.playing = False
    

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
        
        self.frame_index = 0

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
            self.__animate()
            self.last_update = now
    
    
    def __animate(self):
        self.frame_index += 1
        if self.frame_index > len(self.get_current_animation()) - 1:
            self.on_animation_finished()
            if self.loop:
                self.frame_index = 0
            else:
                self.playing = False
    

    def change_animation(self, next_animation_name, force=False):
        if self.current_animation != next_animation_name or force:
            self.frame_index = 0
            self.current_animation = next_animation_name
            self.on_animation_changed()


    def get_current_animation(self) -> Animation:
        return self.animations[self.current_animation]


    def get_surface(self) -> pg.Surface:
        return self.get_current_animation()[self.frame_index]
