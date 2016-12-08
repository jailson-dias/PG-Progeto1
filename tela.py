

z_buffer = []

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
