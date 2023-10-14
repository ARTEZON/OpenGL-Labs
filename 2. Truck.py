from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *

WINDOW_W = 800
WINDOW_H = 600

FOV = 70
Z_NEAR = 0.1
Z_FAR = 400

CAM_POS = (0, 7, 0)
CAM_DIRECTION = (8, 5, -2)

ROTATE = False
ROTATE_SPEED = 0.5
ROTATE_RADIUS = 15

angle = 220


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


def grass():
    glColor3f(0.247, 0.608, 0.043)
    glBegin(GL_QUADS)
    glVertex3f(-200, -0.005, -200)
    glVertex3f(-200, -0.005, 200)
    glVertex3f(200, -0.005, 200)
    glVertex3f(200, -0.005, -200)
    glEnd()


def road():
    def line(z, width, x=0, length=400):
        glColor3f(0.987, 0.987, 1)
        glBegin(GL_QUADS)
        glVertex3f(x - length / 2, 0.005, (z - width / 2))
        glVertex3f(x - length / 2, 0.005, (z + width / 2))
        glVertex3f(x + length / 2, 0.005, (z + width / 2))
        glVertex3f(x + length / 2, 0.005, (z - width / 2))
        glEnd()

    def dashed_line(z, width):
        x = -200
        while x < 200:
            line(z, width, x, 3)
            x += 9

    glColor3f(0.278, 0.298, 0.333)
    glBegin(GL_QUADS)
    glVertex3f(-200, 0, -7.5)
    glVertex3f(-200, 0, 7.5)
    glVertex3f(200, 0, 7.5)
    glVertex3f(200, 0, -7.5)
    glEnd()

    line(-7.3, 0.15)
    line(7.3, 0.15)
    line(-0.15, 0.15)
    line(0.15, 0.15)
    dashed_line(-3.58, 0.15)
    dashed_line(3.58, 0.15)


def circle(x, y, z, radius, rotate=0):
    vertices = 50
    if rotate != 0:
        glRotate(rotate, 0, 1, 0)
    glBegin(GL_POLYGON)
    for v in range(vertices):
        rad = 2 * pi / vertices * v
        glVertex3f(x + radius * cos(rad), y + radius * sin(rad), z)
    glEnd()
    if rotate != 0:
        glRotate(rotate, 0, -1, 0)


def wheel(x, y, z, radius, rotate=0):
    glColor3f(0.704, 0.707, 0.714)
    circle(x, y, z - 0.005, radius * 0.6, rotate)
    circle(x, y, z + 0.005, radius * 0.6, rotate)
    glColor3f(0.1, 0.1, 0.1)
    circle(x, y, z, radius, rotate)


def cuboid(x, y, z, length, width, height, color1=None, color2=None, color3=None, skip=0):
    glBegin(GL_QUADS)
    if color1:
        glColor3f(*color1)
    if skip != 2:
        glVertex3f(x, y, z)
        glVertex3f(x, y, z + width)
        glVertex3f(x, y + height, z + width)
        glVertex3f(x, y + height, z)
    if skip != 1:
        glVertex3f(x + length, y, z)
        glVertex3f(x + length, y, z + width)
        glVertex3f(x + length, y + height, z + width)
        glVertex3f(x + length, y + height, z)
    if color2:
        glColor3f(*color2)
    glVertex3f(x, y, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y + height, z)
    glVertex3f(x, y + height, z)
    glVertex3f(x, y, z + width)
    glVertex3f(x + length, y, z + width)
    glVertex3f(x + length, y + height, z + width)
    glVertex3f(x, y + height, z + width)
    if color3:
        glColor3f(*color3)
    glVertex3f(x, y, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y, z + width)
    glVertex3f(x, y, z + width)
    if skip != 2:
        glVertex3f(x, y + height, z)
        glVertex3f(x + length, y + height, z)
        glVertex3f(x + length, y + height, z + width)
        glVertex3f(x, y + height, z + width)
    glEnd()


def prism(x, y, z, length, width, height):
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + width)
    glVertex3f(x, y + height, z + width)
    glVertex3f(x, y + height, z)
    glVertex3f(x, y, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y, z + width)
    glVertex3f(x, y, z + width)
    glVertex3f(x, y + height, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y, z + width)
    glVertex3f(x, y + height, z + width)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex3f(x, y, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x, y + height, z)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex3f(x, y, z + width)
    glVertex3f(x + length, y, z + width)
    glVertex3f(x, y + height, z + width)
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


def display():
    if ROTATE:
        rotate_camera()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    skybox()
    grass()
    road()

    cuboid(0, 0.5, -3.1, 13.6, 2.4, 2.7, (0.7, 0.7, 0.7), (0.8, 0.8, 0.8), (0.9, 0.9, 0.9))
    glColor3f(0.6, 0.6, 0.6)
    cuboid(13.605, 0.5, -2.7, 0.19, 1.6, 1)

    wheel(1, 0.5, -0.695, 0.5)
    wheel(2, 0.5, -0.695, 0.5)
    wheel(3, 0.5, -0.695, 0.5)
    wheel(12, 0.5, -0.695, 0.5)

    wheel(1, 0.5, -3.105, 0.5)
    wheel(2, 0.5, -3.105, 0.5)
    wheel(3, 0.5, -3.105, 0.5)
    wheel(12, 0.5, -3.105, 0.5)

    cuboid(13.8, 0.5, -3.1, 1.4, 2.4, 2.7, (0.8, 0.518, 0), (0.9, 0.582, 0), (1, 0.647, 0), 1)
    cuboid(15.205, 0.5, -3.1, 1, 2.4, 1.5, (0.8, 0.518, 0), (0.9, 0.582, 0), (1, 0.647, 0), 2)
    glColor4f(0.25, 0.162, 0, 0.5)
    prism(15.205, 2, -3.1, 1, 2.4, 1.2)

    wheel(15, 0.5, -3.105, 0.5)
    wheel(15, 0.5, -0.695, 0.5)

    glutSwapBuffers()
    glutPostRedisplay()


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


def mouse(button, state, x, y):
    global ROTATE_RADIUS
    if state == GLUT_DOWN:
        if button == 3:
            ROTATE_RADIUS -= 0.25
        elif button == 4:
            ROTATE_RADIUS += 0.25
        rotate_camera(0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow("Truck")
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glClearColor(0.3, 0.3, 0.3, 1.0)
    glMatrixMode(GL_PROJECTION)
    rotate_camera(0)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glutMainLoop()


if __name__ == "__main__":
    main()
