from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = b'Rect & Line'

Rec = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]
r1x = Rec[0][0]
r1y = Rec[0][1]
r2x = Rec[1][0]
r2y = Rec[1][1]
r3x = Rec[2][0]
r3y = Rec[2][1]
r4x = Rec[3][0]
r4y = Rec[3][1]

Line = [[-0.2, -0.9], [0.6, 0.7]]
p1x = Line[0][0]
p1y = Line[0][1]
p2x = Line[1][0]
p2y = Line[1][1]

flag = True
show = False

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
    glutIdleFunc(loop)
    glutMainLoop()
    return

def loop1():
    global show
    show = True


def display():
    glClear(GL_COLOR_BUFFER_BIT )
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glPushMatrix()
    #glRotatef(45,0,0,1)
    glBegin(GL_POLYGON)
    for i in range(Rec.__len__()):
        glVertex2f(Rec[i][0], Rec[i][1])
    glEnd()
    glPopMatrix()

    if show:
        glPushMatrix()
        glBegin(GL_LINES)
        glVertex2f(p1x, p1y)
        glVertex2f(p2x, p2y)
        glEnd()
        glPopMatrix()

    glFlush()
    return

def loop():
    global flag, show, p1x, p1y, p2x, p2y
    m = (p1y - p2y) / (p1x - p2x)
    def case():
        if p1x<r1x:
            return 1
        elif p1x>r4x:
            return 2
        elif p1y<r1y:
            return 3
        elif p1y>r2y:
            return 4

    while flag:
        if accept():
            flag = False
            show = True
        elif reject():
            flag = False
            show = False
        else:
            if r1x<=p1x<=r4x and r1y<=p1y<=r2y:
                temp = p1x
                p1x = p2x
                p2x = temp

                temp = p1y
                p1y = p2y
                p2y = temp

            if case() == 1:
                p1y += m * abs(p1x - r1x)
                p1x = r1x
            if case() == 2:
                p1y -= m * abs(p1x - r4x)
                p1x = r4x

            if case() == 3:
                p1x += abs(p1y - r1y) / m
                p1y = r1y
            if case() == 4:
                p1x -= abs(p1y - r2y) / m
                p1y = r2y
    glutPostRedisplay()

def accept():
    if r1x<=p1x<=r4x and r1y<=p1y<=r2y  and  r1x<=p2x<=r4x and r1y<=p2y<=r2y:
        return True
    else:
        return False

def reject():
    if p1x<r1x and p2x<r1x  or  p1x>r4x and p2x>r4x  or  p1y<r1y and p2y<r1y  or  p1y>r2y and p2y>r2y:
        return True
    else:
        return False

main()