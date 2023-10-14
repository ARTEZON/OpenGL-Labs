from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt


CANVAS_W = 800
CANVAS_H = 500


def draw_rect(x, y, w, h):
    glPushMatrix()
    glTranslate(x, y, 0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(w, 0)
    glVertex2f(w, h)
    glVertex2f(0, h)
    glEnd()
    glPopMatrix()


def draw_stripes():
    def stripe(is_yellow):
        if is_yellow:
            glColor3f(1, 0.808, 0)
        else:
            glColor3f(0, 0.416, 0.306)
        draw_rect(0, 0, CANVAS_W, 1)

    glPushMatrix()
    glScale(100, 100, 1)
    yellow = False
    for i in range(5):
        stripe(yellow)
        yellow = not yellow
        glTranslate(0, 1, 0)
    glPopMatrix()


def draw_star(x, y, size):
    def top():
        glBegin(GL_TRIANGLES)
        glVertex2f(0, 1)
        glVertex2f(sqrt(50 - 22 * sqrt(5)) / 4.0, (sqrt(5) - 1) / 4.0)
        glVertex2f(-sqrt(50 - 22 * sqrt(5)) / 4.0, (sqrt(5) - 1) / 4.0)
        glEnd()

    def side():
        glBegin(GL_TRIANGLES)
        glVertex2f(sqrt(50 - 22 * sqrt(5)) / 4.0, (sqrt(5) - 1) / 4.0)
        glVertex2f(sqrt((5 - sqrt(5)) / 8.0), (-1 - sqrt(5)) / 4.0)
        glVertex2f(-sqrt((5 + sqrt(5)) / 8.0), (sqrt(5) - 1) / 4.0)
        glEnd()

    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(size, -size, 1)
    top()
    side()
    glScale(-1, 1, 1)
    side()
    glPopMatrix()


def loop():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_stripes()
    glColor3f(0.824, 0.063, 0.204)
    draw_rect(0, 0, 300, 300)
    glColor3f(1, 1, 1)
    draw_star(150, 150, 95)
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)
    glutInitWindowSize(CANVAS_W, CANVAS_H)
    glutCreateWindow("Flag of Togo")
    glutDisplayFunc(loop)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, CANVAS_W, CANVAS_H, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
