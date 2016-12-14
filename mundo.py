from OpenGL.GL import *
from OpenGL.GL.exceptional import glEnd
from OpenGL.GLUT import *

# tamanho da tela

width,height = 600, 400
pontos_camera = []
z_buffer = []
cores = []

pontos_tela = []
pontos = []
triangulos = []
luz = 0
luz_camera = 0
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

    def __truediv__(self, a):
        return Ponto3D(self.x/a,self.y/a,self.z/a)

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

    def __init__(self,p,normal):
        self.p = p
        self.normal = normal

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
            l1 = Linha(pontos_tela[self.p1].x,pontos_tela[self.p2].x,
            pontos_tela[self.p3].x,p4_tela.x)
            l2 = Linha(pontos_tela[self.p1].y,pontos_tela[self.p2].y,
            pontos_tela[self.p3].y,p4_tela.y)
            l3 = Linha(1,1,1,1)
            a,b,c = Escalona(l1,l2,l3).esc()

            # encontrando o novo ponto
            ponto = pontos_camera[self.p1].p*a+pontos_camera[self.p2].p*b + pontos_camera[self.p3].p*c
            normal = pontos_camera[self.p1].normal*a + pontos_camera[self.p2].normal*b + pontos_camera[self.p3].normal*c
            p4_camera = PontosNormal3D(ponto,normal)
            pontos_tela.append(p4_tela)
            pontos_camera.append(p4_camera)

            # pintando os trinagulos
            bottom_triangulo(self.p1, self.p2, len(pontos_tela)-1)
            top_triangulo(self.p2, len(pontos_tela)-1, self.p3)

    def __str__(self):
        global pontos_camera
        return "["+str(pontos_camera[self.p1].p)+" " + str(pontos_camera[self.p2].p) + " "+str(pontos_camera[self.p3].p) +"]"

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

    def __truediv__(self, a):
        return RGB(self.r/a,self.g/a,self.b/a)

    def __str__(self):
        return "("+str(self.r)+", "+str(self.g)+", "+str(self.b)+")"

# utilizado para calcular a formula (I = Ia.ka + Ip*Op.kd.(N.L) + Ipm.ks.(R.V)^q)
def get_cor(ponto, normal):
    global camera, luz_camera
    ia = luz_camera.ia*luz_camera.ka
    l = (luz_camera.pl-ponto)
    l.normalizado()
    normal.normalizado()
    id = RGB(0,0,0)
    ie = RGB(0,0,0)
    if (normal.prod_escalar(l)>=0):
        id = (luz_camera.od%luz_camera.il)*luz_camera.kd*(normal.prod_escalar(l))
        v = (camera.c - ponto)
        v.normalizado()
        if (normal.prod_escalar(v)<0):
            normal = -normal
        r = (normal*2)*(normal.prod_escalar(l)) - l
        r.normalizado()
        if (v.prod_escalar(r)>=0):
            ie =(luz_camera.il)*luz_camera.ks*(pow(r.prod_escalar(v), luz_camera.n))
    return ia + id + ie

def ler_objeto(path):
    global pontos, triangulos
    arquivo = open(path,'r')
    mn = arquivo.readline().split(' ')
    i = int(mn[0])
    j = int(mn[1])
    while (i > 0):
        i -= 1
        xyz = arquivo.readline().split(' ')
        pontos.append(PontosNormal3D(Ponto3D(float(xyz[0]),float(xyz[1]),float(xyz[2])),Ponto3D(0,0,0)))
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
        pontos[i].cor = get_cor(pontos[i].p, pontos[i].normal)

def mult_matriz(u,v,n,p):
    return Ponto3D(u.x*p.x+u.y*p.y+u.z*p.z,
                    v.x*p.x+v.y*p.y+v.z*p.z,
                    n.x*p.x+n.y*p.y+n.z*p.z)

# utilizados para passar os pontos da base mundo para a base camera
def get_pontos_camera():
    global pontos, pontos_camera, camera, luz, luz_camera, triangulos

    # for i in range(0,len(pontos)):
    #     print (pontos[i].normal)

    for i in range(0,len(pontos)):
        a = mult_matriz(camera.u, camera.v,camera.n, pontos[i].p - camera.c)
        b = mult_matriz(camera.u, camera.v,camera.n, (pontos[i].normal + pontos[i].p) - camera.c)
        pontos_camera.append(PontosNormal3D(a,b-a))
    luz_camera = luz
    luz_camera.pl = mult_matriz(camera.u, camera.v,camera.n, luz.pl - camera.c)

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
    global z_buffer, cores,width,height

    b = []
    c = []
    for j in range(0,height):
        b.append(999999999)
        c.append(RGB(255,255,255))

    for i in range(0,width):
        z_buffer.append(b)
        cores.append(c)

def get_ponto_tela():
    global pontos_tela, pontos, pontos_camera, camera, width,height
    # for i in range(0,len(pontos_camera)):
    #     print (pontos_camera[i].p)
    for i in range(0,len(pontos_camera)):
        x = (camera.d/camera.hx)* (pontos_camera[i].p.x/pontos_camera[i].p.z)
        y = (camera.d/camera.hy) *(pontos_camera[i].p.y / pontos_camera[i].p.z)
        # print (x,y)
        pontos_tela.append(Ponto2D(int((x + 1)*width/2), int((1-y)*height/2)))
        # print (int((x + 1)*width/2), int((1-y)*height/2))
    # print (width, height)
    # for i in range(0,len(pontos_tela)):
    #     print (pontos_tela[i])

class Linha(object):

    def __init__(self,a,b,c,d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __truediv__(self,a):
        a = (a or 1)
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

def triangulos_open_gl(p1,p2,p3):
    #  z_buffer[p1.x][p1.y] = z
    #  cor = pontos[triangulos[i].p1].cor/255.0
    #  print (p1.x,p1.y,cor)
     glColor3f(0,0,0)
     glVertex2f(p1.x, p1.y)
    #  z = (pontos_camera[triangulos[i].p2].z)
     # if (z_buffer[p2.x][p2.y] > z):
    #  z_buffer[p2.x][p2.y] = z
    #  cor = pontos[triangulos[i].p2].cor/255.0
    #  print (p2.x,p2.y,cor)
    #  glColor3f(cor.r,cor.g,cor.b)
     glVertex2f(p2.x, p2.y)
    #  z = (pontos_camera[triangulos[i].p3].z)
     # if (z_buffer[p3.x][p3.y] > z):
    #  z_buffer[p3.x][p3.y] = z
    #  cor = pontos[triangulos[i].p3].cor/255.0
    #  print (p3.x,p3.y,cor)
    #  glColor3f(cor.r,cor.g,cor.b)
     glVertex2f(p3.x, p3.y)


def into(p):
    global width, height
    return (p.x <= width and p.x >= 0 and p.y <= height and p.y >= 0)

def get_into_tela():
    global pontos_tela, triangulos, pontos_camera,z_buffer,cores

    # glBegin(GL_POINTS)
    for i in triangulos:
        p1 = pontos_tela[i.p1]
        p2 = pontos_tela[i.p2]
        p3 = pontos_tela[i.p3]
        if(into(p1) and into(p2) and into(p3)):
            if (i.ponto()):
                draw_point(i.p1)
            elif (i.reta()):
                i.pintar_reta()
            else:
                i.sort_asc_y()
                i.pintar()
            # triangulos_open_gl(p1,p2,p3)
    # glEnd()

def top_triangulo(p1,p2,p3):
    global pontos_camera, pontos_tela, z_buffer, cores
    slope1 = (float(pontos_tela[p3].x - pontos_tela[p1].x)/ float(pontos_tela[p3].y - pontos_tela[p1].y))
    slope2 = (float(pontos_tela[p3].x - pontos_tela[p2].x) /        float(pontos_tela[p3].y - pontos_tela[p2].y))

    x1 = pontos_tela[p3].x
    x2 = pontos_tela[p3].x + 0.5

    sline = pontos_tela[p3].y
    l3 = Linha(1,1,1,1)
    while(sline > pontos_tela[p1].y):
        x_aux = x1
        # string =""
        while(x_aux <= x2):
            l1 = Linha(pontos_tela[p1].x,pontos_tela[p2].x,pontos_tela[p3].x,
                x_aux)
            l2 = Linha(pontos_tela[p1].y,pontos_tela[p2].y,pontos_tela[p3].y,
                sline)
            a,b,c = Escalona(l1,l2,l3).esc()
            ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b + pontos_camera[p3].p*c
            # string += "*"
            if (z_buffer[int(x_aux)][int(sline)] > ponto.z):
                z_buffer[int(x_aux)][int(sline)] = ponto.z
                normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b + pontos_camera[p3].normal*c
                cor = get_cor(ponto,normal)
                cor = cor/255.0
                # cores[int(x_aux)][int(sline)] = cor
                glColor3f(cor.r,cor.g,cor.b)
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
    global pontos_camera, pontos_tela, z_buffer
    pc = pontos_camera[p1]
    pt = pontos_tela[p1]
    if (z_buffer[int(pt.x)][int(pt.y)] > pc.p.z):
        z_buffer[int(pt.x)][int(pt.y)] = pc.p.z
        cor = get_cor(pc.p,pc.normal)
        cor = cor/255.0
        glColor3f(cor.r,cor.g,cor.b)
        glVertex2f(pt.x,pt.y)

def draw_line(p1,p2):
    global pontos_camera, pontos_tela, z_buffer


    x1 = pontos_tela[p1].x
    sline = pontos_tela[p1].y

    if (pontos_tela[p2].y - pontos_tela[p1].y == 0):
        x2 = pontos_tela[p2].x
        if (x1 < x2):
            while(x1 <= x2):
                a,b = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline))
                ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b
                if (z_buffer[int(x1)][int(sline)] > ponto.z):
                    z_buffer[int(x1)][int(sline)] = ponto.z
                    normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b
                    cor = get_cor(ponto,normal)
                    cor = cor/255.0
                    glColor3f(cor.r,cor.g,cor.b)
                    glVertex2f(x1,sline)
                x1 += 1
        else:
            while(x1 >= x2):
                a,b = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline))
                ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b
                if (z_buffer[int(x1)][int(sline)] > ponto.z):
                    z_buffer[int(x1)][int(sline)] = ponto.z
                    normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b
                    cor = get_cor(ponto,normal)
                    cor = cor/255.0
                    glColor3f(cor.r,cor.g,cor.b)
                    glVertex2f(x1,sline)
                x1 -= 1
    else:
        slope1 = (float(pontos_tela[p2].x - pontos_tela[p1].x)/ float(pontos_tela[p2].y - pontos_tela[p1].y))

        if (sline < pontos_tela[p2].y):
            while(sline <= pontos_tela[p2].y):
                a,b = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline))
                ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b
                if (z_buffer[int(x1)][int(sline)] > ponto.z):
                    z_buffer[int(x1)][int(sline)] = ponto.z
                    normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b
                    cor = get_cor(ponto,normal)
                    cor = cor/255.0
                    glColor3f(cor.r,cor.g,cor.b)
                    glVertex2f(x1,sline)
                sline+=1
                x1 += slope1
        else:
            while(sline >= pontos_tela[p2].y):
                a,b = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline))
                ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b
                if (z_buffer[int(x1)][int(sline)] > ponto.z):
                    z_buffer[int(x1)][int(sline)] = ponto.z
                    normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b
                    cor = get_cor(ponto,normal)
                    cor = cor/255.0
                    glColor3f(cor.r,cor.g,cor.b)
                    glVertex2f(x1,sline)
                sline-=1
                x1 -= slope1

def bottom_triangulo(p1,p2,p3):
    global pontos_camera, pontos_tela, z_buffer, cores
    print (pontos_tela[p1],pontos_tela[p2],pontos_tela[p3])
    slope1 = (float(pontos_tela[p2].x - pontos_tela[p1].x)/ float(pontos_tela[p2].y - pontos_tela[p1].y))
    slope2 = (float(pontos_tela[p3].x - pontos_tela[p1].x) / float(pontos_tela[p3].y - pontos_tela[p1].y))

    x1 = pontos_tela[p1].x
    x2 = pontos_tela[p1].x + 0.5

    sline = pontos_tela[p1].y
    l3 = Linha(1,1,1,1)
    while(sline <= pontos_tela[p2].y):
        x_aux = x1
        # string = ""
        while(x_aux <= x2):
            l1 = Linha(pontos_tela[p1].x,pontos_tela[p2].x,pontos_tela[p3].x,
                x_aux)
            l2 = Linha(pontos_tela[p1].y,pontos_tela[p2].y,pontos_tela[p3].y,
                sline)
            a,b,c = Escalona(l1,l2,l3).esc()
            ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b + pontos_camera[p3].p*c
            # string += "*"
            if (z_buffer[int(x_aux)][int(sline)] > ponto.z):
                z_buffer[int(x_aux)][int(sline)] = ponto.z
                normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b + pontos_camera[p3].normal*c
                cor = get_cor(ponto,normal)
                # cores[int(x_aux)][int(sline)] = cor
                cor = cor/255.0
                # print (x_aux,sline)
                glColor3f(cor.r,cor.g,cor.b)
                glVertex2f(x_aux,sline)
            x_aux += 1
        sline+=1
        x1 += slope1
        x2 += slope2
        # print (string)
    # print()

def display():
    global width ,height,cores
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_POINTS)
    # glBegin(GL_TRIANGLES)
    get_into_tela()
    # for x,i in enumerate(cores):
        # string = ""
        # for y,j in enumerate(i):
            # print (cores[i][j])
            # if (not (j.r == 255 and cor.g==255 and cor.b == 255)):
                # cor = j /255.0
                # string += " "
                # glColor3f(cor.r,cor.g,cor.b)
                # glVertex2i(x,y)
            # else:
            #     string += "*"
        # print ("\n\n\n\n\n")
        # print (string)
        # print (cores[i][50],cores[i][300], i)

    # glColor3f(0,0,0)
    # glVertex2f(50,20)
    # glVertex2f(50,21)
    # glVertex2f(50,22)
    # glVertex2f(50,23)


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
    global width, height
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

    init()
    ler_objeto('entradas/Objetos/calice2.byu')
    ler_luz('luz.txt')
    ler_camera('entradas/Cameras/calice2.cfg')

    get_pontos_camera()
    init_z_buffer()
    get_ponto_tela()
    glutMainLoop()

if __name__ == '__main__':
    main()
