from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import random

WINDOW_W = 800
WINDOW_H = 600

FOV = 70
Z_NEAR = 0.1
Z_FAR = 400

CAM_POS = (0, 5, 0)
CAM_DIRECTION = (7, 3, -2)

ROTATE = False
ROTATE_SPEED = -0.5
ROTATE_RADIUS = 15

angle = 220

random.seed('caterpillar')
random_sequence = [random.random() for i in range(100)]


def skybox():
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)

    glColor3f(0.725, 0.871, 0.996)
    glVertex3f(-200, -1, 200)
    glVertex3f(-200, -1, -200)
    glColor3f(0.435, 0.714, 0.965)
    glVertex3f(-200, 200, -200)
    glVertex3f(-200, 200, 200)

    glColor3f(0.725, 0.871, 0.996)
    glVertex3f(200, -1, 200)
    glVertex3f(200, -1, -200)
    glColor3f(0.435, 0.714, 0.965)
    glVertex3f(200, 200, -200)
    glVertex3f(200, 200, 200)

    glColor3f(0.725, 0.871, 0.996)
    glVertex3f(200, -1, -200)
    glVertex3f(-200, -1, -200)
    glColor3f(0.435, 0.714, 0.965)
    glVertex3f(-200, 200, -200)
    glVertex3f(200, 200, -200)

    glColor3f(0.725, 0.871, 0.996)
    glVertex3f(200, -1, 200)
    glVertex3f(-200, -1, 200)
    glColor3f(0.435, 0.714, 0.965)
    glVertex3f(-200, 200, 200)
    glVertex3f(200, 200, 200)

    glVertex3f(200, 200, 200)
    glVertex3f(-200, 200, 200)
    glVertex3f(-200, 200, -200)
    glVertex3f(200, 200, -200)

    glEnd()


def rotate_camera(degrees=None):
    global CAM_POS, CAM_DIRECTION, angle
    radius = ROTATE_RADIUS
    height = CAM_POS[1]
    angle += ROTATE_SPEED if degrees is None else degrees
    angle = angle % 360
    CAM_POS = (CAM_DIRECTION[0] + radius * cos(radians(angle)),
               height,
               CAM_DIRECTION[2] + radius * sin(radians(angle)))
    move_camera()


def move_camera():
    glLoadIdentity()
    gluPerspective(FOV, WINDOW_W / WINDOW_H, Z_NEAR, Z_FAR)
    gluLookAt(*CAM_POS, *CAM_DIRECTION, 0, 1, 0)
    glutPostRedisplay()


def display():
    if ROTATE:
        rotate_camera()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    skybox()
    glPushMatrix()
    for i in range(16):
        glColor3f(0, 0.8 + (random_sequence[2 * i] - 0.5) / 20, 0)
        glutSolidSphere(1 + (random_sequence[4 * i] - 0.5) / 8, 100, 100)
        if i == 0:
            # eyes
            glPushMatrix()
            glTranslatef(-0.8, 0.25, 0.35)
            glColor3f(1, 1, 1)
            glutSolidSphere(0.15, 100, 100)
            glTranslatef(-0.1, 0, 0.02)
            glColor3f(0, 0, 0)
            glutSolidSphere(0.09, 100, 100)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(-0.8, 0.25, -0.35)
            glColor3f(1, 1, 1)
            glutSolidSphere(0.15, 100, 100)
            glTranslatef(-0.1, 0, -0.02)
            glColor3f(0, 0, 0)
            glutSolidSphere(0.09, 100, 100)
            glPopMatrix()

            # mouth
            glPushMatrix()
            glTranslatef(-0.9, -0.18, -0.2)
            glColor3f(0.855, 0.427, 0.373)
            glutSolidCylinder(0.08, 0.4, 100, 100)
            glPopMatrix()

            # horns
            glColor3f(0, 0.5, 0)
            glPushMatrix()
            glRotatef(-100, 1, 0, 0)
            glTranslatef(0, 0, 0.85)
            glutSolidCone(0.1, 0.35, 100, 100)
            glPopMatrix()
            glPushMatrix()
            glRotatef(-80, 1, 0, 0)
            glTranslatef(0, 0, 0.85)
            glutSolidCone(0.1, 0.35, 100, 100)
            glPopMatrix()

        glColor3f(0.96, 0.855, 0.008)
        glPushMatrix()
        glRotatef(70, 1, 0, 0)
        glutSolidCone(0.2, 1.3, 100, 100)
        glRotatef(40, 1, 0, 0)
        glutSolidCone(0.2, 1.3, 100, 100)
        glPopMatrix()
        glTranslatef(1.2 + (random_sequence[4 * i + 1] - 0.5) / 16,
                     (random_sequence[4 * i + 2] - 0.5) / 4,
                     (random_sequence[4 * i + 3] - 0.5) / 4)

    glPopMatrix()
    glutSwapBuffers()


def keyboard(key, x, y):
    global ROTATE, ROTATE_SPEED, CAM_POS
    if key == b' ':
        ROTATE = not ROTATE
    elif key == GLUT_KEY_LEFT or key == b'a':
        if ROTATE:
            ROTATE_SPEED += 0.1
        else:
            rotate_camera(2)
    elif key == GLUT_KEY_RIGHT or key == b'd':
        if ROTATE:
            ROTATE_SPEED -= 0.1
        else:
            rotate_camera(-2)
    elif key == GLUT_KEY_UP or key == b'w':
        CAM_POS = (CAM_POS[0], CAM_POS[1] + 0.5, CAM_POS[2])
    elif key == GLUT_KEY_DOWN or key == b's':
        CAM_POS = (CAM_POS[0], CAM_POS[1] - 0.5, CAM_POS[2])
    move_camera()
    glutPostRedisplay()


def mouse(button, state, x, y):
    global ROTATE_RADIUS
    if state == GLUT_DOWN:
        if button == 3:
            ROTATE_RADIUS -= 0.25
        elif button == 4:
            ROTATE_RADIUS += 0.25
        rotate_camera(0)
        glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow("Caterpillar")
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glClearColor(0.506, 0.357, 0.25, 1.0)
    glMatrixMode(GL_PROJECTION)
    rotate_camera(0)
    glEnable(GL_DEPTH_TEST)
    glutMainLoop()


if __name__ == "__main__":
    main()
