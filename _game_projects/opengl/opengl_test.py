import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes

from OpenGL.GL.shaders import compileProgram, compileShader

class App:

    def __init__(self):
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF) # doublebuff - system where two drawable surfaces are used - one frame on gfx card and one on screen
        self.clock = pg.time.Clock()
        # init opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        self.triangle = Triangle()
        
        self.mainLoop()
    
    def createShader(self, vertexFilepath, fragmentFilepath):
        # using with auto closes the file after use
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
        
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # refresh
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            self.clock.tick(60)
        
        self.quit()
    
    def quit(self):
        print(glGetError())
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Triangle:
        def __init__(self):
            # x, y, x, r, g, b
            self.vertices = (
                -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                0.0, 0.5, 0.0, 0.0, 0.0, 1.0
            )

            self.vertices = np.array(self.vertices, dtype=np.float32) # opengl needs 32bit float - IMPORTANT

            self.vertex_count = 3

            self.vao = glGenVertexArrays(1) # vao = vertex array object - declares vertex data
            glBindVertexArray(self.vao) # bind before making the vbo
            self.vbo = glGenBuffers(1) # vbo = vertex buffer object
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0) # pos
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))  # ctype - void pointer

            glEnableVertexAttribArray(1) # color
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        
        def destroy(self):
            glDeleteVertexArrays(1, (self.vao,))  # need to wrap self.vao as a list
            glDeleteBuffers(1, (self.vbo,)) # same as above


if __name__ == "__main__":
    app = App()
