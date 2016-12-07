

pontos = []
triangulos = []
luz = []
camera = 0

def gramschmidt(v,n):
    n.mult(v.prod_escalar(n)/n.prod_escalar(n))
    return v - n

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

    def mult(self, a):
        self.x = self.x*a
        self.y = self.y*a
        self.z = self.z*a

    def normalizado(self):
        tam = self.norma()
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

class Luz3D(object):

    def __init__(self,p,ip):
        self.p = p
        self.ip = ip

class Camera3D(object):

    def __init__(self,c,u,v,n,d,hx,hy):
        self.c = c
        self.u = u
        self.v = v
        self.n = n
        self.d = d
        self.hx = hx
        self.hy = hy

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
        p1 = pontos[int(t[0])-1].p
        p2 = pontos[int(t[1])-1].p
        p3 = pontos[int(t[2])-1].p
        normal = (p2-p1).prod_vetorial(p3-p1)
        triangulos.append(TriangulosNormal3D(p1,p2,p3,normal))
        pontos[int(t[0])-1].normal += normal
        pontos[int(t[1])-1].normal += normal
        pontos[int(t[2])-1].normal += normal

    for i in range(0,len(pontos)):
        pontos[i].normal.normalizado()

def ler_luz(path):
    global luz
    arquivo = open(path,'r')
    i = int(arquivo.readline())
    while(i>0):
        i -= 1
        l = arquivo.readline().split(' ')
        luz.append(Luz3D(Ponto3D(float(l[0]),float(l[1]),float(l[2])),float(arquivo.readline())))

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
    luz = []
    camera = Camera3D(0,0,0,0,0,0,0)

def get_dados():
    global pontos,triangulos, luz, camera
    return (pontos, triangulos, luz, camera)

def main():
    global pontos
    init()
    ler_objeto('objeto.txt')
    ler_luz('luz.txt')
    ler_camera('camera.txt')

if __name__ == '__main__':
    main()
