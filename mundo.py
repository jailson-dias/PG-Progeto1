

# tamanho da tela

height, width = 400, 600

pontos_tela = []
pontos = []
triangulos = []
luz = 0
camera = 0

def gramschmidt(v,n):
    return v - (n * (v.prod_escalar(n)/n.prod_escalar(n)))

def eq(a,b):
    if (abs(a - b)<(10 ** -12)):
        return True
    return False

class Ponto3D(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self,segundo):
        return Ponto3D(self.x + segundo.x,
                    self.y + segundo.y,
                    self.z + segundo.z)

    def __sub__(self,segundo):
        return Ponto3D(self.x - segundo.x,
                    self.y - segundo.y,
                    self.z - segundo.z)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def __mul__(self, a):
        return Ponto3D(self.x*a,self.y*a,self.z*a)

    def __neg__(self):
        return self*-1

    def normalizado(self):
        tam = self.norma()
        if (eq(tam,0)):
            tam = 1
        self.x = self.x/tam
        self.y = self.y/tam
        self.z = self.z/tam

    def norma(self):
        return pow(pow(self.x,2) + pow(self.y,2) + pow(self.z,2),0.5)

    def prod_vetorial(self,segundo):
        return Ponto3D(self.y*segundo.z - self.z*segundo.y,
                        self.z*segundo.x - self.x*segundo.z,
                        self.x*segundo.y - self.y*segundo.x)

    def prod_escalar(self, segundo):
        return self.x*segundo.x + self.y*segundo.y + self.z*segundo.z

class PontosNormal3D(object):

    def __init__(self,p,normal,cor):
        self.p = p
        self.normal = normal
        self.cor = cor

class TriangulosNormal3D(object):

    def __init__(self,p1,p2,p3,normal):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.normal = normal

class Luz3D(object):

    def __init__(self,pl,ka,ia,kd,od,ks,il,n):
        self.pl = pl # Coordenadas do ponto de luz
        self.ka = ka # reflexao ambiental
        self.ia = ia # vetor cor ambiental
        self.kd = kd # constante difusa
        self.od = od # vetor difuso
        self.ks = ks # parte especular
        self.il = il # cor da fonte de luz
        self.n = n # constante de rugosidade

class Camera3D(object):

    def __init__(self,c,u,v,n,d,hx,hy):
        self.c = c # Ponto da camera
        self.u = u # Vetor U
        self.v = v # Vetor V
        self.n = n # Vetor N
        self.d = d  # distancia
        self.hx = hx
        self.hy = hy

class RGB(object):

    def __init__(self, r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def __mul__(self, a):
        return RGB(self.r*a,self.g*a,self.b*a)

    def __mod__(self,a):
        return RGB(self.r*a.r,self.g*a.g,self.b*a.b)

    def __add__(self, cor):
        return RGB(min(self.r+cor.r,255),min(self.g+cor.g,255),min(self.b+cor.b,255))

    def __str__(self):
        return "("+str(self.r)+", "+str(self.g)+", "+str(self.b)+")"

# utilizado para calcular a formula (I = Ia.ka + Ip*Op.kd.(N.L) + Ipm.ks.(R.V)^q)
def get_cor(i):
    global camera, luz, pontos
    ponto = pontos[i]
    ia = luz.ia*luz.ka
    # print (ia, "ia")
    l = (luz.pl-ponto.p)
    # print (l,"l")
    l.normalizado()
    normal = ponto.normal
    normal.normalizado()
    id = RGB(0,0,0)
    ie = RGB(0,0,0)
    if (normal.prod_escalar(l)>=0):
        id = (luz.od%luz.il)*luz.kd*(normal.prod_escalar(l))
        # print (id, "id")
        v = (camera.c - ponto.p)
        v.normalizado()
        if (normal.prod_escalar(v)<0):
            normal = -normal
        # print (v, "v")
        r = (normal*2)*(normal.prod_escalar(l)) - l
        r.normalizado()
        if (v.prod_escalar(r)>=0):
            # print (r,"r")
            ie = (luz.il)*luz.ks*(pow(r.prod_escalar(v),luz.n))
            # print (ie, "ie")
    # print (ia, id, ie, "separado")
    pontos[i].cor = ia + id + ie
    # print (pontos[i].cor)

def ler_objeto(path):
    global pontos, triangulos
    arquivo = open(path,'r')
    mn = arquivo.readline().split(' ')
    i = int(mn[0])
    j = int(mn[1])
    while (i > 0):
        i -= 1
        xyz = arquivo.readline().split(' ')
        pontos.append(PontosNormal3D(Ponto3D(float(xyz[0]),float(xyz[1]),float(xyz[2])),Ponto3D(0,0,0), RGB(255,255,255)))
    while (j > 0):
        j -= 1
        t = arquivo.readline().split(' ')
        while (t[0] == '\n'):
            t = arquivo.readline().split(' ')
        p1 = pontos[int(t[0])-1].p
        p2 = pontos[int(t[1])-1].p
        p3 = pontos[int(t[2])-1].p
        normal = (p2-p1).prod_vetorial(p3-p1) # normal do triangulo
        normal.normalizado()
        triangulos.append(TriangulosNormal3D(int(t[0])-1,int(t[1])-1,int(t[2])-1,normal))
        pontos[int(t[0])-1].normal += normal # calcula a normal do ponto
        pontos[int(t[1])-1].normal += normal
        pontos[int(t[2])-1].normal += normal

    for i in range(0,len(pontos)):
        pontos[i].normal.normalizado() # normalizando a normal dos pontos

    # print (len(pontos), len(triangulos), "object")

def ler_luz(path):
    global luz
    arquivo = open(path,'r')
    p = arquivo.readline().split(' ')
    luz.pl = Ponto3D(float(p[0]),float(p[1]),float(p[2]))
    luz.ka = int(arquivo.readline())
    ia = arquivo.readline().split(' ')
    luz.ia = RGB(float(ia[0]),float(ia[1]),float(ia[2]))
    luz.kd = float(arquivo.readline())
    od = arquivo.readline().split(' ')
    luz.od = RGB(float(od[0]),float(od[1]),float(od[2]))
    luz.ks = float(arquivo.readline())
    il = arquivo.readline().split(' ')
    luz.il = RGB(float(il[0]),float(il[1]),float(il[2]))
    luz.n = float(arquivo.readline())

def ler_camera(path):
    global camera
    arquivo = open(path,'r')
    camera = arquivo.readline().split(' ')
    c = Ponto3D(float(camera[0]),float(camera[1]),float(camera[2]))
    v1 = arquivo.readline().split(' ')
    n = Ponto3D(float(v1[0]),float(v1[1]),float(v1[2]))
    v2 = arquivo.readline().split(' ')
    v = Ponto3D(float(v2[0]),float(v2[1]),float(v2[2]))
    inteiros = arquivo.readline().split(' ')
    d = float(inteiros[0])
    hx = float(inteiros[1])
    hy = float(inteiros[2])
    vl = gramschmidt(v,n)
    vl.normalizado()
    n.normalizado()
    camera = Camera3D(c,n.prod_vetorial(vl),vl,n,d,hx,hy)

def init():
    global pontos,triangulos, luz, camera
    pontos = []
    triangulos = []
    luz = Luz3D(0,0,0,0,0,0,0,0)
    camera = Camera3D(0,0,0,0,0,0,0)

def cor_pontos():
    global pontos
    for i in range(0,len(pontos)):
        get_cor(i)

# def get_dados():
#     global pontos,triangulos, luz, camera
#     return (pontos, triangulos, luz, camera)






pontos_camera = []

def mult_matriz(u,v,n,p):
    return Ponto3D(u.x*p.x+u.y*p.y+u.z*p.z,
                    v.x*p.x+v.y*p.y+v.z*p.z,
                    n.x*p.x+n.y*p.y+n.z*p.z)

# utilizados para passar os pontos da base mundo para a base camera
def get_pontos_camera():
    global pontos, pontos_camera, camera
    for i in range(0,len(pontos)):
        pontos_camera.append(mult_matriz(camera.u, camera.v,camera.n, pontos[i].p - camera.c))

    # print (len(pontos_camera), "camera")
z_buffer = []
cores = []

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


def init_z_buffer():
    global z_buffer, cores

    b = []
    c = []
    for j in range(0,400):
        b.append(999999999)
        c.append(RGB(255,255,255))

    for i in range(0,600):
        z_buffer.append(b)
        cores.append(c)


def get_ponto_tela():
    global pontos_tela, pontos, pontos_camera, camera, width,height
    for i in range(0,len(pontos_camera)):
        pontos_tela.append(Ponto2D(int(((camera.d/camera.hx)*(pontos_camera[i].x/pontos_camera[i].z) + 1)*width/2),
                                int((1 - (camera.d/camera.hy)*(pontos_camera[i].y/pontos_camera[i].z))*height/2)))

    # print (len(pontos_tela), "tela")

class Linha(object):

    def __init__(self,a,b,c,d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __div__(self,a):
        return Linha(self.a/a,self.b/a,self.c/a,self.d/a)

    def __mod__(self, a):
        return Linha(self.a - a.a*self.a,
                    self.b - a.b*self.a,
                    self.c - a.c*self.a,
                    self.d - a.d*self.a)

    def __xor__(self, a):
        return Linha(self.a,
                    self.b - a.b*self.b,
                    self.c - a.c*self.b,
                    self.d - a.d*self.b)

    def __add__(self, a):
        return Linha(self.a,
                    self.b,
                    self.c - a.c*self.c,
                    self.d - a.d*self.c)

class Escalona(object):

    def __init__(self, l1,l2,l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def esc(self):
        l1 = self.l1/self.l1.a
        l2 = self.l2%l1
        l3 = self.l3%l1
        l2 = l2/l2.b
        l1 = l1^l2
        l3 = l3^l2
        l3 = l3/l3.c
        l1 = l1+l3
        l2 = l2 + l3
        return (l1.d,l2.d,l3.d)



from hermite_bezier import *

def into(p):
    global width, height
    return (p.x <= width and p.x >= 0 and p.y <= height and p.y >= 0)

def get_into_tela():
    global pontos_tela, triangulos, pontos_camera,z_buffer,cores
    for i in range(0,len(triangulos)):

        # print (i, len(triangulos))
        # print (triangulos[i].p1,triangulos[i].p2,triangulos[i].p3, "pontos")
        p1 = pontos_tela[triangulos[i].p1]
        p2 = pontos_tela[triangulos[i].p2]
        p3 = pontos_tela[triangulos[i].p3]
        if(into(p1) and into(p2) and into(p3)):
            # p4 = Ponto2D((p1.x+p2.x+p3.x)/3.0,(p1.y+p2.y+p3.y)/3.0)
            # p4 = p1
            # if (p2.x>p4.x):
            #     p4 = p2
            # if (p3.x>p4.x):
            #     p4 = p3
            # a = Linha(p1.x,p2.x,p3.x,p4.x)
            # b = Linha(p1.y,p2.y,p3.y,p4.y)
            # c = Linha(1.0,1.0,1.0,1.0)
            # d = Escalona(a,b,c)
            # alfa, beta, gama = d.esc()
            z = (pontos_camera[triangulos[i].p1].z)
            # pontos_camera[triangulos[i].p2].z+
            # pontos_camera[triangulos[i].p3].z)/3.0
            # print (z_buffer[p1.x][p1.y],"zzzz")
            # print (p1.x,p1.y)
            # glPointSize(1)
            # glBegin(GL_POINTS)
            glShadeModel(GL_SMOOTH);
            glBegin(GL_TRIANGLES);
            # cor = pontos[triangulos[i].p1].cor
            # glColor3f(int(cor.r),int(cor.g),int(cor.b))
            # print (int(cor.r),int(cor.g),int(cor.b))
            # if (z_buffer[p1.x][p1.y] > z):
            z_buffer[p1.x][p1.y] = z
            cor = pontos[triangulos[i].p1].cor
            print (p1.x,p1.y,cor)
            glColor3f(cor.r,cor.g,cor.b)
            glVertex2f(p1.x, p1.y)
            z = (pontos_camera[triangulos[i].p2].z)
            # if (z_buffer[p2.x][p2.y] > z):
            z_buffer[p2.x][p2.y] = z
            cor = pontos[triangulos[i].p2].cor
            print (p2.x,p2.y,cor)
            glColor3f(cor.r,cor.g,cor.b)
            glVertex2f(p2.x, p2.y)
            z = (pontos_camera[triangulos[i].p3].z)
            # if (z_buffer[p3.x][p3.y] > z):
            z_buffer[p3.x][p3.y] = z
            cor = pontos[triangulos[i].p3].cor
            print (p3.x,p3.y,cor)
            glColor3f(cor.r,cor.g,cor.b)
            glVertex2f(p3.x, p3.y)


            glEnd()





def display():
    global vetores, pontos, color_point, color_vector, linhas_pontos, linhas_vetores, pontos_pontos, pontos_vetores
    global color_line_pontos,color_line_vector
    glClear(GL_COLOR_BUFFER_BIT)

    get_into_tela()

    glFlush()




def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 600, 400, 0.0, -5.0, 5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# def pintar(button, state, x, y):
#
#     display()



def main():
    # global pontos_camera
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 400)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("PG - 2016.2")

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLineWidth(3.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    init()
    ler_objeto('entradas/Objetos/camaro.byu')
    ler_luz('luz.txt')
    ler_camera('entradas/Cameras/camaro.cfg')
    cor_pontos()
    # print (pontos_camera)

    get_pontos_camera()
    init_z_buffer()
    get_ponto_tela()
    # glutMouseFunc(pintar)
    # print ("fim")
    glutMainLoop()

if __name__ == '__main__':
    main()
    # p1 = Ponto2D(1.0,0.0)
    # p2 = Ponto2D(0.0,1.0)
    # p3 = Ponto2D(1.0,1.0)
    # p4 = Ponto2D(1.0,1.0)
    # a = Linha(p1.x,p2.x,p3.x,p4.x)
    # b = Linha(p1.y,p2.y,p3.y,p4.y)
    # c = Linha(1.0,1.0,1.0,1.0)
    # d = Escalona(a,b,c)
    # print (d.esc())
