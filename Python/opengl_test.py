# this program uses pygame and PyOpenGl to render a cube on a surface and the camera can be moved around the surface
# sources used: 
# https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/

# imports
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import keyboard
import mouse
from pynput import mouse
import time

# define vertices of cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

# define edges of cube
edges = (
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

# define colors of cube
colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1)
)

# define surfaces of cube
surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

# define ground surfaces
ground_surface = (0, 1, 2, 3)

# define ground vertices
ground_vertices = (
    (-10, -0.1, 50),
    (10, -0.1, 50),
    (-10, -0.1, -300),
    (10, -0.1, -300),
)

# define dimensions for window
x = 800
y = 800

# define colors
white = (255, 255, 255)
green = (0, 255, 0)
blue =  (0, 0, 128)

# this functions makes the cube
def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Ground():
    glBegin(GL_QUADS)
    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 1))
        glVertex3fv(vertex)
    glEnd()

def main():
    needs_to_run = True
    paused = False
    pygame.init()
    display_surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption('Initialize')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('welcome', True, green)
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)
    display_surface.blit(text, textRect)
    pygame.display.update()
    time.sleep(2)
    


    pygame.display.set_caption('CUBE')
    display = (x,y)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL, RESIZABLE)
    gluPerspective(100, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    print(display[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True

        if needs_to_run:
            glRotatef(10, 10, 0 , 0)
            needs_to_run = False

        if not paused:
            if keyboard.is_pressed('down'):
                glTranslatef(0, 0, -0.5)
            if keyboard.is_pressed('up'):
                glTranslatef(0, 0, 0.5)
    
            if keyboard.is_pressed('left'):
                glTranslatef(0.5, 0, 0)
            if keyboard.is_pressed('right'):
                glTranslatef(-0.5, 0, 0)

        # glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Ground()
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()
