#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from collections import namedtuple
from math import *
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import argparse

global zoom
global movement
global loopActive
global startLoop
zoom = 60
movement = 0
loopActive = 0
startLoop = 0

parser = argparse.ArgumentParser(
    description='Fase 3 do projeto final de Computacao Grafica.')
parser.add_argument('--dummy-draw-function', '-d', dest='use_dummy_draw_function',
                    action='store_true', default=False,
                    help='usa uma funcao padrao para o desenho do objeto')

options = parser.parse_args()

try:
    import aviao
except ImportError:
    print >> sys.stderr, '*** ERRO: Arquivo "aviao.py" nao foi encontrado.'
    print >> sys.stderr, '    Voce deve criar sua versao da funcao desenhaAviao()'
    print >> sys.stderr, '    e coloca-la em um arquivo chamado "aviao.py"'
    print >> sys.stderr, '    neste mesmo diretorio.'
    sys.exit(1)


Point = namedtuple('Point', 'x y z')
Orientation = namedtuple('Orientation', 'roll pitch yaw')


class Plane(object):
    _BASE_Z = 10.
    _LOOP_RADIUS = 4.

    def __init__(self, scene):
        self.scene = scene

    @property
    def time_in_loop(self):
        return self.scene.current_time % 10000.

    @property
    def phase(self):
        return int(self.time_in_loop / 2000.)

    @property
    def time_in_phase(self):
        return (self.time_in_loop - 2000. * self.phase) / 2000.

    @property
    def pos(self):
        phase = self.phase

        if phase == 0:
            return Point(-15. + 30. * self.time_in_phase, -10., self._BASE_Z)

        elif phase == 1:
            angle = 2 * pi * self.time_in_phase - pi / 2
            return Point(15 + self._LOOP_RADIUS * cos(angle),
                         -10.,
                         self._BASE_Z + self._LOOP_RADIUS + self._LOOP_RADIUS * sin(angle))

        elif phase == 2:
            angle = -pi / 2. + pi * self.time_in_phase
            return Point(15 + 10 * cos(angle), 10 * sin(angle), self._BASE_Z)

        elif phase == 3:
            return Point(15. - 30. * self.time_in_phase, 10., self._BASE_Z)

        else:
            angle = pi / 2. + pi * self.time_in_phase
            return Point(-15 + 10 * cos(angle), 10 * sin(angle), self._BASE_Z)

    @property
    def orientation(self):
        global loopActive
        global startLoop

        phase = self.phase
        time_in_phase = self.time_in_phase

        def smooth_roll():
            if time_in_phase <= 0.2:
                return 30 * time_in_phase / 0.2
            if time_in_phase >= 0.8:
                return 30 * (1 - time_in_phase) / 0.2
            return 30

        if phase == 0:
            if(startLoop == 1):
                return Orientation(360*time_in_phase, 0, 0)
            else:
                return Orientation(0, 0, 0)

        elif phase == 1:
            if(loopActive == 1):
                startLoop = 1
            else:
                startLoop = 0
            
            return Orientation(0, 360. * time_in_phase, 0)

        elif phase == 2:
            if(startLoop == 1):
                return Orientation(-smooth_roll()-360*time_in_phase, 0, 180. * time_in_phase)
            else:
                return Orientation(-smooth_roll(), 0, 180. * time_in_phase)

        elif phase == 3:
            if(startLoop == 1):
                return Orientation(-360*time_in_phase, 0, 180)
            else:
                return Orientation(0, 0, 180)

        else:
            if(startLoop == 1):
                return Orientation(-smooth_roll()+360*time_in_phase, 0, 180. + 180. * time_in_phase)
            else:
                return Orientation(-smooth_roll(), 0, 180. + 180. * time_in_phase)


class Scene(object):
    @staticmethod
    def draw_dummy_object(angulo_helice):
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 0.2, 0.9, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0, 0, 0, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0])

        glPushMatrix()
        glScale(1.4, 0.3, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.2, 0.8, 0.6, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [.7, .7, .7, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [127])

        glPushMatrix()
        glTranslate(0.8, 0, 0)
        glutSolidSphere(0.1, 32, 32)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0, 0.25, 0)
        glutSolidSphere(0.1, 32, 32)
        glTranslate(0, -0.50, 0)
        glutSolidSphere(0.1, 32, 32)
        glPopMatrix()

        glPushMatrix()
        glTranslate(-0.6, 0, 0.15)
        glutSolidSphere(0.1, 32, 32)
        glPopMatrix()

    current_time = 0.0
    delta_time = 0.0

    draw_object_function = None

    window_width = 300
    window_height = 300


    def __init__(self):
        if self.draw_object_function is None:
            self.draw_object_function = Scene.draw_dummy_object

        self.plane = Plane(self)

        self.enabled_lights = [True, True, True, True, False, False, False, False]

        self.arrow = glGenLists(1)
        glNewList(self.arrow, GL_COMPILE)

        glBegin(GL_LINES)
        glVertex(0, 0, 0)
        glVertex(1, 0, 0)
        glEnd()

        glPushMatrix()
        glTranslate(0.8, 0, 0)
        glRotate(90, 0, 1, 0)
        glutSolidCone(0.12, 0.25, 8, 2)
        glPopMatrix()

        glEndList()

        self.city = glGenLists(1)
        glNewList(self.city, GL_COMPILE)

        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0, 0, 0, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0])

        for x in range(-30, 31):
            for y in range(-30, 31):
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [
                    random.uniform(0.5, 0.7),
                    random.uniform(0.3, 0.5),
                    random.uniform(0.0, 0.2),
                    1])

                height = random.uniform(0.8, 3)
                glPushMatrix()
                glTranslate(2 * x, 2 * y, height / 2.)
                glScale(0.8, 0.8, height)
                glutSolidCube(1)
                glPopMatrix()

        for x in range(-10, 11):
            for y in range(-10, 11):
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [
                    random.uniform(0.5, 0.7),
                    random.uniform(0.3, 0.5),
                    random.uniform(0.0, 0.2),
                    1])

                height = random.uniform(5, 8)
                glPushMatrix()
                glTranslate(5*x, 5*y, height / 2.)
                glScale(0.8, 0.8, height)
                glutSolidCube(1)
                glPopMatrix()

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 0, 0, 1])
        glPushMatrix()
        glScale(250, 250, 0.01)
        glutSolidCube(1)
        glPopMatrix()

        glEndList()

    def configure_glut(self):
        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)


    def update_time(self):
        current_time = glutGet(GLUT_ELAPSED_TIME)
        self.delta_time = current_time - self.current_time
        self.current_time = current_time


    def switch_to_scene_viewport(self):
        glViewport(0, 0, self.window_width, self.window_height)

        if self.window_width >= self.window_height:
            x_range = float(self.window_width) / self.window_height
            y_range = 1.
        else:
            x_range = 1.
            y_range = float(self.window_height) / self.window_width

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(zoom, float(self.window_width) / self.window_height,
                       1, 500)

        glMatrixMode(GL_MODELVIEW)


    def draw_scene_viewport(self):
        glDisable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glDisable(GL_SCISSOR_TEST)

        glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0, 0, 0, 1])

        for light in range(len(self.enabled_lights)):
            if self.enabled_lights[light]:
                glEnable(GL_LIGHT0 + light)
            else:
                glDisable(GL_LIGHT0 + light)

        glClearColor(0.3, 0.5, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        pos = self.plane.pos
        gluLookAt(-20, -30, 20, pos[0], pos[1], pos[2], 0, 0, 1)

        glLightfv(GL_LIGHT1, GL_POSITION, [-15, 3, 10, 0])
        glLightfv(GL_LIGHT2, GL_POSITION, [-5, -20, 10, 1])
        glLightfv(GL_LIGHT3, GL_POSITION, [-5, 20, 10, 1])
        glLightfv(GL_LIGHT4, GL_POSITION, [0, 0, 20, 1])

        glPushMatrix()
        orientation = self.plane.orientation
        glTranslate(*self.plane.pos)
        glRotate(orientation.yaw, 0, 0, 1)
        glRotate(orientation.roll, 1, 0, 0)
        glRotate(orientation.pitch, 0, -1, 0)
        self.draw_object_function(1.5 * self.current_time)
        glPopMatrix()

        if(loopActive == 1):
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 1, 0, 1])
        else:
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 0, 0, 1])

        glPushMatrix()
        glColor(1, 0, 0)
        glTranslate(0, 0, 20)
        glutSolidCube(0.5)
        glPopMatrix()

        glColor(1, 0, 0)
        glCallList(self.city)

    def draw(self):
        self.update_time()

        self.switch_to_scene_viewport()
        self.draw_scene_viewport()

        glutSwapBuffers()
        glutPostRedisplay()


    def reshape(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        glViewport(0, 0, window_width, window_height)

        if window_width >= window_height:
            x_range = float(window_width) / window_height
            y_range = 1.
        else:
            x_range = 1.
            y_range = float(window_height) / window_width

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(-1, 1, -1, 1, -1, 1)
        glOrtho(-x_range, x_range, -y_range, y_range, -1, 1)

        glMatrixMode(GL_MODELVIEW)


    def keyboard(self, char, x, y):
        global zoom
        global loopActive
        if char >= '0' and char <= '7':
            light = ord(char) - ord('0')
            self.enabled_lights[light] = not self.enabled_lights[light]
        if char == '[':
            if(zoom > 10):
                zoom = zoom-1
        if char == ']':
            if(zoom < 60):
                zoom = zoom+1
        if char == '9':
            if(loopActive == 1):
                loopActive = 0
            else: 
                loopActive = 1

    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.last_x = x
                self.last_y = y


    def motion(self, x, y):
        dx = x - self.last_x
        dy = y - self.last_y
        self.last_x = x
        self.last_y = y


if __name__ == '__main__':
    if not options.use_dummy_draw_function:
        try:
            Scene.draw_object_function = staticmethod(aviao.desenhaAviao)
        except AttributeError:
            print >> sys.stderr, '*** ERRO: Nao existe uma funcao chamada desenhaAviao()'
            print >> sys.stderr, '    dentro do arquivo "aviao.py".'
            print >> sys.stderr, '    Voce deve criar sua versao da funcao desenhaAviao()'
            print >> sys.stderr, '    e coloca-la em um arquivo chamado "aviao.py"'
            print >> sys.stderr, '    neste mesmo diretorio.'
            sys.exit(1)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(300, 300)
    glutCreateWindow("Aula 12")

    glEnable(GL_DEPTH_TEST)

    # Cor da fonte de luz 0
    glLight(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.02]);
    glLight(GL_LIGHT0, GL_DIFFUSE, [0, 0, 0]);
    glLight(GL_LIGHT0, GL_SPECULAR, [0, 0, 0]);
    glEnable(GL_LIGHT0)
    # Cor da fonte de luz 1
    glLight(GL_LIGHT1, GL_AMBIENT, [0, 0, 0]);
    glLight(GL_LIGHT1, GL_DIFFUSE, [0.8, 0.8, 0.8]);
    # Cor da fonte de luz 2
    glLight(GL_LIGHT2, GL_AMBIENT, [0, 0, 0]);
    glLight(GL_LIGHT2, GL_DIFFUSE, [0.1, 0.1, 0.1]);
    # Cor da fonte de luz 3
    glLight(GL_LIGHT3, GL_AMBIENT, [0, 0, 0]);
    glLight(GL_LIGHT3, GL_DIFFUSE, [0.1, 0.1, 0.1]);
    # Cor da fonte de luz 4
    glLight(GL_LIGHT4, GL_AMBIENT, [0, 0, 0]);
    glLight(GL_LIGHT4, GL_DIFFUSE, [0.6, 0.4, 0.1]);

    scene = Scene()
    scene.configure_glut()

    glutMainLoop()
