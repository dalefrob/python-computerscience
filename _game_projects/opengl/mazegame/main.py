import random
import math
import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from pygame import Vector2, Vector3

class Wall:
    def __init__(self, position : Vector3):
        self.position = position
        self.rotation = math.pi / 4

        self.verts = []
        
    

    def update(self, dt):
        self.rotation += 1


    def draw(self):
        glPushMatrix()
        # Set positions
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)

        # Draw
        glBegin(GL_QUADS)
        for v in self.verts:
            glColor3fv([1,0,1])
            glVertex3fv([v.x, v.y, v.z])

        glEnd()

        glPopMatrix()
    
    @staticmethod
    def from_brush(a : Vector3, b : Vector3, c : Vector3):
        min_x = min(a.x, b.x, c.x)
        max_x = max(a.x, b.x, c.x)
        min_y = min(a.y, b.y, c.y)
        max_y = max(a.y, b.y, c.y)
        min_z = min(a.z, b.z, c.z)
        max_z = max(a.z, b.z, c.z)
        extents = Vector3(max_x - min_x, max_y - min_y, max_z - min_z)
        edge1 = b - a
        edge2 = c - a
        normal = edge1.cross(edge2).normalize()
        d = a + c - b  # b is the "middle" corner, a and c are its neighbours
        new_wall = Wall([0,0,0])
        new_wall.verts = [
            a, b, c, d
        ]
        return new_wall


class Game:
    def __init__(self):
        pygame.init()
        window_size = (800, 600)
        self.screen = pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
        self.clock = pygame.Clock()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

         # --- Projection matrix: defines the lens/FOV ---
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (window_size[0] / window_size[1]), 0.1, 50.0)

        # --- ModelView matrix: defines camera and object positions ---
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Load temp
        v3 = Vector3
        self.wall = Wall.from_brush(v3([-2,2,2]), v3([0, 2, -2]), v3([6, 2, -2]))



        self.running = True
    

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.update(dt)
            self.draw()


    def handle_input(self):
        pass


    def update(self, dt):
        self.wall.update(dt)


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(*[0, 0, -5])
        self.wall.draw()
        pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.run()