import time

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = b'Rect & Line'

"""
    Rect
        r2(x, y) |--------| r3(x, y)
                 |        |
        r1(x, y) |--------| r4(x, y)
    
    Line
        p1(x, y) --------------- p2(x, Y)
"""
Rect = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]
r1x = Rect[0][0]
r1y = Rect[0][1]
r2x = Rect[1][0]
r2y = Rect[1][1]
r3x = Rect[2][0]
r3y = Rect[2][1]
r4x = Rect[3][0]
r4y = Rect[3][1]

Line = [[-0.2, -0.6], [-0.6,0.4]]
p1x = Line[0][0]
p1y = Line[0][1]
p2x = Line[1][0]
p2y = Line[1][1]

pos_x = 0
pos_y = 0
move = False

flag = True
show = False
show2 = False

def initial():
    glClearColor(0, 0, 0, 0)
    glColor3ub(0, 0, 0)
    glColor3f(1, 1, 1)

def main():
    glutInit(sys.argv)

    glutInitWindowSize(400, 400)
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowPosition(200, 200)
    glutCreateWindow(name)
    initial()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(loop)
    glutMainLoop()
    return

def loop1():
    global show
    show = True
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT )
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glPushMatrix()
    #glRotatef(45,0,0,1)
    glBegin(GL_POLYGON)
    for i in range(Rect.__len__()):
        glVertex2f(Rect[i][0], Rect[i][1])
    glEnd()
    glPopMatrix()

    if show:
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex2f(p1x, p1y)
        glVertex2f(p2x, p2y)
        glEnd()
        glPopMatrix()

    if show2:
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex2f(Line[0][0] + pos_x, Line[0][1] + pos_y)
        glVertex2f(Line[1][0] + pos_x, Line[1][1] + pos_y)
        glEnd()
        glPopMatrix()

    glFlush()
    return

def keyboard(key, x, y):
    global p1x, p2x, p1y, p2y, pos_x, pos_y, move, show2, show
    unit = 0.01

    while True:
        if key == b'\x20':
            if show2:
                show2 = False
                show = True
            else:
                show2 = True
                show = False
            break
        if key == b'a':
            p1x -= unit
            p2x -= unit

            move = True
            pos_x -= unit
            break
        if key == b'd':
            p1x += unit
            p2x += unit

            move = True
            pos_x += unit
            break
        if key == b'w':
            p1y += unit
            p2y += unit

            move = True
            pos_y += unit
            break
        if key == b's':
            p1y -= unit
            p2y -= unit

            move = True
            pos_y -= unit
            break
        else:
            break

def loop():
    global flag, show, p1x, p1y, p2x, p2y, Line, move
    if p1x - p2x != 0:
        m = (p1y - p2y) / (p1x - p2x)
    if p1y - p2y != 0:
        m1 = (p1x - p2x) / (p1y - p2y)
    # reset
    flag = True
    show = False

    if move:
        p1x = Line[0][0] * pos_x
        p1y = Line[0][1] * pos_y
        p2x = Line[1][0] * pos_x
        p2y = Line[1][1] * pos_y

    # IF p1 is outside of Rect THEN move p1 onto Rect's edge(s)
    def adjust_p1():
        global p1x, p1y
    # on X Axis
        #left
        if p1x<r1x:
            p1y += m * abs(p1x - r1x)
            p1x = r1x
            return 1
        #right
        elif p1x>r4x:
            p1y -= m * abs(p1x - r4x)
            p1x = r4x
            return 2
    # on Y Axis
        #bottom
        elif p1y<r1y:
            p1x += m1 * abs(p1y - r1y)
            p1y = r1y
            return 3
        #top
        elif p1y>r2y:
            p1x -= m1 * abs(p1y - r2y)
            p1y = r2y
            return 4


    while flag:
        if accept():
            flag = False
            show = True
        elif reject():
            flag = False
            show = False
        else:
            # IF p1 is not outside THEN swap with p2
            if r1x<=p1x<=r4x and r1y<=p1y<=r2y:
                p1x, p2x = p2x, p1x
                p1y, p2y = p2y, p1y
            adjust_p1()

    glutPostRedisplay()

def accept():
    # both p1 & p2 are inside of Rect
    if r1x<=p1x<=r4x and r1y<=p1y<=r2y  and  r1x<=p2x<=r4x and r1y<=p2y<=r2y:
        return True
    else:
        return False

def reject():
    # both p1 & p2 are outside of Rect
    if p1x<r1x and p2x<r1x  or  p1x>r4x and p2x>r4x  or  p1y<r1y and p2y<r1y  or  p1y>r2y and p2y>r2y:
        return True
    else:
        return False

if __name__ == '__main__':
    main()