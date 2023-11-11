from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import time
from math import *

WINDOW_W = 800
WINDOW_H = 600

FOV = 70
Z_NEAR = 0.1
Z_FAR = 400

CAM_POS = [0, 7, 0]
CAM_DIRECTION = [0, 3, 0]

ROTATE = False
ROTATE_SPEED = 0.5
ROTATE_RADIUS = 15

angle = 90


def rotate_camera(deg=None):
    global CAM_POS, CAM_DIRECTION, angle
    radius = ROTATE_RADIUS
    height = CAM_POS[1]
    angle += ROTATE_SPEED if deg is None else deg
    angle = angle % 360
    CAM_POS[0] = CAM_DIRECTION[0] + radius * cos(radians(angle))
    CAM_POS[1] = height
    CAM_POS[2] = CAM_DIRECTION[2] + radius * sin(radians(angle))
    move_camera()


def move_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, WINDOW_W / WINDOW_H, Z_NEAR, Z_FAR)
    gluLookAt(*CAM_POS, *CAM_DIRECTION, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)


def keyboard(key, _x, _y):
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
        CAM_POS[1] += 0.5
        move_camera()
    elif key == GLUT_KEY_DOWN or key == b's':
        CAM_POS[1] -= 0.5
        move_camera()


def mouse(button, state, _x, _y):
    global ROTATE_RADIUS
    if state == GLUT_DOWN:
        if button == 3:
            ROTATE_RADIUS -= 0.25
        elif button == 4:
            ROTATE_RADIUS += 0.25
        rotate_camera(0)


def ground():
    glBegin(GL_QUADS)
    glVertex3f(-200, 0, -200)
    glVertex3f(-200, 0, 200)
    glVertex3f(200, 0, 200)
    glVertex3f(200, 0, -200)
    glEnd()


def display():
    current_time = time()
    rotation = current_time * 100 % 360
    elevation = 3 + current_time * 5 % 5
    if current_time * 5 % 10 >= 5:
        elevation = 8 - current_time * 5 % 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if ROTATE:
        rotate_camera()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.1, 0.1, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 30)
    ground()

    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.19, 0.19, 0.19, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    glTranslatef(0, elevation, 0)
    glRotatef(rotation, 0, 1, 0)
    glutSolidCylinder(1, 5, 100, 100)
    glPopMatrix()

    light_x = 0
    light_y = 10
    light_z = 0
    glLightfv(GL_LIGHT0, GL_POSITION, [light_x, light_y, light_z, 1])

    glutSwapBuffers()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow("Light")
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glClearColor(0.25, 0.25, 0.25, 1)
    rotate_camera(0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.9, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.9, 0.9, 1, 1])
    glutMainLoop()


if __name__ == "__main__":
    main()
