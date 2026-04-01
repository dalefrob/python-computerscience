import random
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Brush:
    def __init__(self, position = (0.0, 0.0, 0.0), scale = (1.0, 1.0, 1.0)):
        self.color = [random.random(), random.random(), random.random()]
        self.position = position
        self.scale = scale
        self.pivot = np.array([0.5, 0.5, 0.5])
        self.basis = ( 
            # x, y, z
            (1, 0, 0), 
            (1, 1, 0), 
            (0, 1, 0), 
            (0, 0, 0),
            (1, 0, 1), 
            (1, 1, 1),
            (0, 0, 1), 
            (0, 1, 1) 
        )
        self.vertices = np.array([ 
            # x, y, z
            [1, 0, 0], 
            [1, 1, 0], 
            [0, 1, 0], 
            [0, 0, 0],
            [1, 0, 1], 
            [1, 1, 1],
            [0, 0, 1], 
            [0, 1, 1] 
        ], dtype=np.float32)
        self.edges = ( 
            (0,1), 
            (0,3), 
            (0,4), 
            (2,1), 
            (2,3), 
            (2,7), 
            (6,3), 
            (6,4), 
            (6,7), 
            (5,1), 
            (5,4), 
            (5,7)
        )
        self.rotaxis = [random.random(), random.random(), random.random()]
        self.rotation = 0
        self.rotspeed = random.random()
        self.faces = [
            [0,1,2,3],
            [5,4,6,7],
            [4,5,1,0],
            [6,3,2,7],
        ]
        self.normals = [
            [0,0,-1],
            [0,0,1],
            [1,0,0],
            [-1,0,0],
        ]
    
    def get_vertices(self):
        return self.vertices

    def update(self):
        self.rotation += self.rotspeed


    def draw(self):
         # Push a copy of the current matrix so our translate is temporary
        glPushMatrix()
        verts = self.get_vertices()
        # Move the brush to its world position
        glTranslatef(*self.position)

        neg_pivot = self.pivot * -1
        glTranslatef(*self.pivot)
        glRotatef(self.rotation, *self.rotaxis)
        glTranslatef(*neg_pivot)
        
        glBegin(GL_LINES)
        glColor3fv([1,1,1])
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(verts[vertex])
        glEnd()

        glBegin(GL_QUADS)
        glColor3fv(self.color)
        for face, normal in zip(self.faces, self.normals):
            glNormal3fv(normal)
            for vertex_index in face:
                glVertex3fv(verts[vertex_index])
        glEnd()
        # Restore the matrix — camera transform is preserved, brush transform is gone
        glPopMatrix()



def main():
    pygame.init()
    display = (800, 600)
    # The DOUBLEBUF | OPENGL flags are critical for enabling the OpenGL context
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.Clock()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CW)

    brushes = [
        Brush((1, 1, 1), (2,1.5,3)),
        Brush((-0.5, 0, 0.5), 1),
        Brush((0.22, -2, 1), 1)
    ]
    for i in range(20):
        x, y, z = (random.random() - 0.5) * 10, (random.random() - 0.5) * 10, (random.random() - 0.5) * 10
        b = Brush((x, y, z), 1)
        brushes.append(b)

    # --- Projection matrix: defines the lens/FOV ---
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # --- ModelView matrix: defines camera and object positions ---
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    camera_pos = [0, 0, -15]
    camera_y_rot = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            camera_y_rot += 1
        if keys[K_RIGHT]:
            camera_y_rot += -1
        if keys[K_UP]:
            camera_pos[2] += 0.2
        if keys[K_DOWN]:
            camera_pos[2] += -0.2



        # Clear the buffers before drawing
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        glRotatef(camera_y_rot, 0, 1, 0)
        glTranslatef(*camera_pos)

        for brush in brushes:
            brush.update()
            brush.draw()

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
