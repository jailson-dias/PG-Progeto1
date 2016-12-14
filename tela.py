from OpenGL.GL import *
from OpenGL.GL.exceptional import glEnd
from OpenGL.GLUT import *

z_buffer = []
width,height = 600, 500

pontos_tela = []
triangulos = []


class Ponto2D(object):

    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __add__(self,segundo):
        return Ponto2D(self.x + segundo.x,
                    self.y + segundo.y)

    def __sub__(self,segundo):
        return Ponto2D(self.x - segundo.x,
                    self.y - segundo.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __mul__(self, a):
        return Ponto2D(self.x*a,self.y*a)

    def normalizado(self):
        tam = self.norma()
        self.x = self.x/tam
        self.y = self.y/tam

    def norma(self):
        return pow(pow(self.x,2) + pow(self.y,2),0.5)

    def prod_escalar(self, segundo):
        return self.x*segundo.x + self.y*segundo.y

class TriangulosNormal3D(object):

    def __init__(self,p1,p2,p3,normal):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.normal = normal

    def ponto(self):
        global pontos_tela
        if((pontos_tela[self.p1].x == pontos_tela[self.p2].x and pontos_tela[self.p1].y == pontos_tela[self.p2].y) and (pontos_tela[self.p1].x == pontos_tela[self.p3].x and pontos_tela[self.p1].y == pontos_tela[self.p3].y)):
            return True
        return False

    def reta(self):
        global pontos_tela
        if ((pontos_tela[self.p1].x == pontos_tela[self.p2].x and pontos_tela[self.p1].y == pontos_tela[self.p2].y) or (pontos_tela[self.p1].x == pontos_tela[self.p3].x and pontos_tela[self.p1].y == pontos_tela[self.p3].y) or (pontos_tela[self.p2].x == pontos_tela[self.p3].x and pontos_tela[self.p2].y == pontos_tela[self.p3].y)):
            return True
        elif (pontos_tela[self.p1].y == pontos_tela[self.p2].y and pontos_tela[self.p1].y == pontos_tela[self.p3].y):
            return True
        return False

    def pintar_reta(self):
        global pontos_tela
        if ((pontos_tela[self.p1].x == pontos_tela[self.p2].x and pontos_tela[self.p1].y == pontos_tela[self.p2].y)):
            draw_line(self.p1, self.p3)
        elif (pontos_tela[self.p1].x > pontos_tela[self.p2].x and pontos_tela[self.p1].x == pontos_tela[self.p3].x and pontos_tela[self.p2].x > pontos_tela[self.p3].x):
            draw_line(self.p1,self.p3)
        else:
            draw_line(self.p1, self.p2)

    def igual(self):
        global pontos_tela
        if ((pontos_tela[self.p1].x == pontos_tela[self.p2].x and pontos_tela[self.p1].y == pontos_tela[self.p2].y) or (pontos_tela[self.p1].x == pontos_tela[self.p3].x and pontos_tela[self.p1].y == pontos_tela[self.p3].y) or (pontos_tela[self.p2].x == pontos_tela[self.p3].x and pontos_tela[self.p2].y == pontos_tela[self.p3].y)):
            return True
        elif (pontos_tela[self.p1].y == pontos_tela[self.p2].y or pontos_tela[self.p1].y == pontos_tela[self.p3].y or pontos_tela[self.p2].y == pontos_tela[self.p3].y):
            return True
        return False

    def sort_asc_y(self):
        global pontos_tela
        if (pontos_tela[self.p1].y > pontos_tela[self.p2].y):
            vTmp = self.p1
            self.p1 = self.p2
            self.p2 = vTmp
        if (pontos_tela[self.p1].y > pontos_tela[self.p3].y):
            vTmp = self.p1
            self.p1 = self.p3
            self.p3 = vTmp
        if (pontos_tela[self.p2].y > pontos_tela[self.p3].y):
            vTmp = self.p2
            self.p2 = self.p3
            self.p3 = vTmp

    def pintar(self):
        global pontos_tela, pontos_camera
        if (pontos_tela[self.p2].y == pontos_tela[self.p3].y):
            # print (pontos_tela[self.p1],pontos_tela[self.p2],
            # pontos_tela[self.p3])
            bottom_triangulo(self.p1, self.p2, self.p3)
        elif (pontos_tela[self.p1].y == pontos_tela[self.p2].y):
            top_triangulo(self.p1, self.p2, self.p3)
        else:
            # dividindo o triangulo em 2
            p4_tela = Ponto2D(int(pontos_tela[self.p1].x + (float(pontos_tela[self.p2].y - pontos_tela[self.p1].y) / float(pontos_tela[self.p3].y - pontos_tela[self.p1].y)) * (pontos_tela[self.p3].x - pontos_tela[self.p1].x)),
            pontos_tela[self.p2].y)

            # print (pontos_tela[self.p1],pontos_tela[self.p2],
            # pontos_tela[self.p3],p4_tela)

            # encontrando o a,b e c

            pontos_tela.append(p4_tela)

            # pintando os trinagulos
            bottom_triangulo(self.p1, self.p2, len(pontos_tela)-1)
            top_triangulo(self.p2, len(pontos_tela)-1, self.p3)

    def __str__(self):
        global pontos_camera
        return "["+str(pontos_camera[self.p1].p)+" " + str(pontos_camera[self.p2].p) + " "+str(pontos_camera[self.p3].p) +"]"


def into(p):
    global width, height
    return (p.x <= width and p.x >= 0 and p.y <= height and p.y >= 0)

def get_into_tela():
    global pontos_tela, triangulos
    # glBegin(GL_POINTS)
    for i in range(0,len(triangulos)):
        # if (not triangulos[i].igual()):
        p1 = pontos_tela[triangulos[i].p1]
        p2 = pontos_tela[triangulos[i].p2]
        p3 = pontos_tela[triangulos[i].p3]
        if(into(p1) and into(p2) and into(p3)):
            if (triangulos[i].ponto()):
                draw_point(triangulos[i].p1)
            elif (triangulos[i].reta()):
                triangulos[i].pintar_reta()
            else:
                triangulos[i].sort_asc_y()
                triangulos[i].pintar()
    # glEnd()


def top_triangulo(p1,p2,p3):
    global pontos_tela
    slope1 = (float(pontos_tela[p3].x - pontos_tela[p1].x)/ float(pontos_tela[p3].y - pontos_tela[p1].y))
    slope2 = (float(pontos_tela[p3].x - pontos_tela[p2].x) /        float(pontos_tela[p3].y - pontos_tela[p2].y))

    x1 = pontos_tela[p3].x
    x2 = pontos_tela[p3].x + 0.5

    sline = pontos_tela[p3].y
    while(sline > pontos_tela[p1].y):
        x_aux = x1
        # string =""
        while(x_aux <= x2):
            glVertex2f(x_aux,sline)
            x_aux += 1
        sline-=1
        x1 -= slope1
        x2 -= slope2
        # print (x1,x2,sline)
        # print (string)
    # print()

def get_ab(p1,p2,p3):
    b = 0
    if(p2.x-p1.x == 0):
        b = (p3.y-p1.y)/(p2.y-p1.y)
    else :
        b = (p3.x-p1.x)/(p2.x-p1.x)
    a = 1 - b
    return (a,b)

def draw_point(p1):
    global pontos_tela
    # pc = pontos_camera[p1]
    pt = pontos_tela[p1]
    glVertex2f(pt.x,pt.y)

def draw_line(p1,p2):
    global pontos_tela

    x1 = pontos_tela[p1].x
    sline = pontos_tela[p1].y

    print ("aqui")

    if (pontos_tela[p2].y - pontos_tela[p1].y == 0):
        x2 = pontos_tela[p2].x
        if (x1 < x2):
            while(x1 <= x2):
                glVertex2f(x1,sline)
                x1 += 1
        else :
            while(x1 >= x2):
                glVertex2f(x1,sline)
                x1 -= 1
    else:
        slope1 = (float(pontos_tela[p2].x - pontos_tela[p1].x)/ float(pontos_tela[p2].y - pontos_tela[p1].y))
        if (sline < pontos_tela[p2].y):
            while(sline <= pontos_tela[p2].y):
                glVertex2f(x1,sline)
                sline+=1
                x1 += slope1
        else:
            while(sline >= pontos_tela[p2].y):
                glVertex2f(x1,sline)
                sline-=1
                x1 -= slope1

def bottom_triangulo(p1,p2,p3):
    global pontos_tela
    slope1 = (float(pontos_tela[p2].x - pontos_tela[p1].x)/ float(pontos_tela[p2].y - pontos_tela[p1].y))
    slope2 = (float(pontos_tela[p3].x - pontos_tela[p1].x) / float(pontos_tela[p3].y - pontos_tela[p1].y))

    x1 = pontos_tela[p1].x
    x2 = pontos_tela[p1].x + 0.5

    sline = pontos_tela[p1].y

    while(sline <= pontos_tela[p2].y):
        x_aux = x1
        # string = ""
        while(x_aux <= x2):
            glVertex2f(x_aux,sline)
            x_aux += 1
        sline+=1
        x1 += slope1
        x2 += slope2




def display():
    global width ,height
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0,0,0)
    # ordenar_triangulos()
    get_into_tela()

    glEnd()
    glFlush()


def reshape(width_v, height_v):
    global width,height
    glViewport(0, 0, width_v, height_v)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, height, 0.0, -5.0, 5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    global width, height, pontos_tela, triangulos
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("PG - 2016.2")

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glLineWidth(3.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    # init()
    pontos_tela.append(Ponto2D(300,100))
    pontos_tela.append(Ponto2D(100,200))
    pontos_tela.append(Ponto2D(300,100))
    triangulos.append(TriangulosNormal3D(0,1,2,0))
    glutMainLoop()

if __name__ == '__main__':
    main()
