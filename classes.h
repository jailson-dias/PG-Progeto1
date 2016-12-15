#include <bits/stdc++.h>
#include "glut.h"

using namespace std;

bool eq(float a,float b){
    if (abs(a - b)<(10 ** -12))
        return true;
    return false;
}

class Ponto3D{
    float x,y,z;
    Ponto3D(float x,float y,float z):x(x),y(y),z(z){}
    Ponto3D(const Ponto3D &p):x(p.x),y(p.y),z(p.z){}
    Ponto3D operator +(const Ponto3D &p) const {
      return Ponto3D(x+p.x,y+p.y,z+p.z);
    }
    Ponto3D operator -(const Ponto3D &p) const {
      return Ponto3D(x-p.x,y-p.y,z-p.z);
    }
    Ponto3D operator *(float a) const {
      return Ponto3D(x*a,y*a,z*a);
    }
    Ponto3D operator /(float a) const {
      return Ponto3D(x/a,y/a,z/a);
    }
    Ponto3D operator -() const {
      return Ponto3D(-x,-y,-z);
    }
    void normalizado(){
      float tam = this.norma();
      if (eq(tam,0))
          tam = 1;
      x = x/tam;
      y = y/tam;
      z = z/tam;
    }
    float norma(){
      return pow(pow(x,2) + pow(y,2) + pow(z,2),0.5);
    }

    Ponto3D prod_vetorial(v){
      return Ponto3D(y*v.z - z*v.y,z*v.x - x*v.z,x*v.y - y*v.x);
    }

    float prod_escalar(v){
      return (x*v.x + y*v.y + z*v.z);
    }
}
class PontosNormal3D{
    Ponto3D p,normal;
    PontosNormal3D(const Ponto3D &p, const Ponto3D &normal): p(p),normal(normal){}
    PontosNormal3D(const PontosNormal3D &pn):p(pn.p),normal(pn.normal){}
}
class TriangulosNormal3D{
    int p1,p2,p3;
    Ponto3D normal;
    TriangulosNormal3D(int p1, int p2, int p3, const Ponto3D &normal):p1(p1),p2(p2),p3(p3),normal(normal){}
    TriangulosNormal3D(const TriangulosNormal3D &t):p1(t.p1),p2(t.p2),p3(t.p3),normal(t.normal){}

    bool reta(){
      if (eq(abs(pontos_tela[p1].y - pontos_tela[p2].y),0) and eq(abs(pontos_tela[p1].y - pontos_tela[p3].y),0))
          return true;
      return false;
    }
    void sort_asc_y(){
        if (pontos_tela[p1].y > pontos_tela[p2].y)
            swap(p1,p2);
        if (pontos_tela[p1].y > pontos_tela[p3].y)
            swap(p1,p3);
        if (pontos_tela[p2].y > pontos_tela[p3].y)
            swap(p2,p3);
    }
    void sort_asc_x(){
        if (pontos_tela[p1].x > pontos_tela[p2].x)
            swap(p1,p2);
        if (pontos_tela[p1].x > pontos_tela[p3].x)
            swap(p1,p3);
        if (pontos_tela[p2].x > pontos_tela[p3].x)
            swap(p2,p3);
    }
    void pintar(){
        if (eq(abs(pontos_tela[p2].y - pontos_tela[p3].y),0))
            bottom_triangulo(p1, p2, p3);
        else if (eq(abs(pontos_tela[p1].y - pontos_tela[p2].y),0))
            top_triangulo(p1, p2, p3);
        else{
            //  dividindo o triangulo em 2
            Ponto2D p4_tela = Ponto2D(int(pontos_tela[p1].x + (float(pontos_tela[p2].y - pontos_tela[p1].y) / float(pontos_tela[p3].y - pontos_tela[p1].y)) * (pontos_tela[p3].x - pontos_tela[p1].x)),pontos_tela[p2].y);

            // encontrando o a,b e c
            Linha l1 = Linha(pontos_tela[p1].x,pontos_tela[p2].x, pontos_tela[p3].x,p4_tela.x);
            Linha l2 = Linha(pontos_tela[p1].y,pontos_tela[p2].y, pontos_tela[p3].y,p4_tela.y);
            Linha l3 = Linha(1,1,1,1);
            Linha esc = Escalona(l1,l2,l3).esc();

            // encontrando o novo ponto
            Ponto3D ponto = pontos_camera[p1].p*esc.a+pontos_camera[p2].p*esc.b + pontos_camera[p3].p*esc.c;
            Ponto3D normal = pontos_camera[p1].normal*esc.a + pontos_camera[p2].normal*esc.b + pontos_camera[p3].normal*esc.c;
            PontosNormal3D p4_camera = PontosNormal3D(ponto,normal);
            pontos_tela.push_back(p4_tela);
            pontos_camera.push_back(p4_camera);

            // pintando os trinagulos
            bottom_triangulo(p1, p2, pontos_tela.size()-1);
            top_triangulo(p2, pontos_tela.size()-1, p3);
        }
}
class Luz3D {
    Ponto3D pl;
    float ka,kd,ks,n;
    RGB ia,od,il;
    Luz3D(const Ponto3D &pl,float ka, const RGB &ia,float kd,const RGB &od,float ks,const RGB &il, float n):pl(pl),ka(ka),ia(ia),kd(kd),od(od),ks(ks),il(il),n(n){}
    Luz3D(const Luz3D &l):pl(l.pl),ka(l.ka),ia(l.ia),kd(l.kd),od(l.od),ks(l.ks),il(l.il),n(l.n){}
}
class RGB{
    float r,g,b;
    RGB(float r,float g,float b):r(r),g(g),b(b){}
    RGB(const RGB &r):r(r.r),g(r.g),b(r.b){}

    RGB operator *(float a) const {
      return RGB(r*a,g*a,b*a);
    }
    RGB operator *(const RGB &a) const {
      return RGB(r*a.r,g*a.g,b*a.b);
    }
    RGB operator +(const RGB &a) const {
      return RGB(min(r+a.r,255),min(g+a.g,255),min(b+a.b,255));
    }
    RGB operator /(float a) const {
      return RGB(r*a,g*a,b*a);
    }
}
class Camera3D{
    Ponto3D c,u,v,n;
    float d,hx,hy;

    Camera3D(const Ponto3D &c,const Ponto3D &u,const Ponto3D &v,const Ponto3D &n,float d,float hx,float hy):c(c),u(u),v(v),n(n),d(d),hx(hx),hy(hy){}
    Camera3D(const Camera3D &c)::c(c.c),u(c.u),v(c.v),n(c.n),d(c.d),hx(c.hx),hy(c.hy){}
}

// utilizado para calcular a formula (I = Ia.ka + Ip*Op.kd.(N.L) + Ipm.ks.(R.V)^q)
RGB get_cor(Ponto3D ponto, Ponto3D normal){
    RGB ia = luz_camera.ia*luz_camera.ka;
    Ponto3D l = (luz_camera.pl-ponto);
    l.normalizado();
    normal.normalizado();
    RGB id = RGB(0,0,0);
    RGB ie = RGB(0,0,0);
    if (normal.prod_escalar(l)>=0){
        id = (luz_camera.od%luz_camera.il)*luz_camera.kd*(normal.prod_escalar(l));
        v = ( - ponto);
        v.normalizado();
        if (normal.prod_escalar(v)<0)
            normal = -normal;
        r = (normal*2)*(normal.prod_escalar(l)) - l;
        r.normalizado();
        if (v.prod_escalar(r)>=0)
            ie =(luz_camera.il)*luz_camera.ks*(pow(r.prod_escalar(v), luz_camera.n));
    }
    return (ia + id + ie);
}

void ler_objeto(string path){
    ifstream arquivo(path);
    // mn = arquivo.readline().split(' ');
    int i,j;
    arquivo >>i>>j;
    while (i-- > 0){
        // xyz = arquivo.readline().split(' ')
        float x,y,z;
        arquivo >>x>>y>>z;
        pontos.push_back(PontosNormal3D(Ponto3D(x,y,z),Ponto3D(0,0,0)))
    }
    while (j-- > 0){
        // t = arquivo.readline().split(' ')
        // while (t[0] == '\n'):
        //     t = arquivo.readline().split(' ')
        int a,b,c;
        arquivo >>a>>b>>c;
        Ponto3D p1,p2,p3,normal;
        p1 = pontos[a-1].p;
        p2 = pontos[b-1].p;
        p3 = pontos[c-1].p;
        normal = (p2-p1).prod_vetorial(p3-p1); // normal do triangulo
        normal.normalizado();
        triangulos.push_back(TriangulosNormal3D(a-1,b-1,c-1,normal));
        pontos[a-1].normal += normal; // calcula a normal do ponto
        pontos[b-1].normal += normal;
        pontos[c-1].normal += normal;
    }

    for (int i = 0;i<pontos.size();i++){
        pontos[i].normal.normalizado(); // normalizando a normal dos pontos
    }
}
void ler_luz(string path){
    ifstream arquivo(path);
    // arquivo = open(path,'r')
    // p = arquivo.readline().split(' ')
    float x,y,z;
    arquivo >>x>>y>>z;
    luz.pl = Ponto3D(x,y,z);
    arquivo>>luz.ka;
    arquivo>>x>>y>>z;
    luz.ia = RGB(x,y,z);
    arquivo >>luz.kd;
    // od = arquivo.readline().split(' ')
    arquivo >>x>>y>>z;
    luz.od = RGB(x,y,z);
    arquivo>>luz.ks;
    // il = arquivo.readline().split(' ')
    arquivo>>x>>y>>z;
    luz.il = RGB(x,y,z);
    arquivo>>luz.n;
}
void ler_camera(string path){
    ifstream arquivo(path);
    // arquivo = open(path,'r')
    // camera = arquivo.readline().split(' ')
    float x,y,z;
    Ponto3D n,v,c,vl;
    arquivo >>x>>y>>z;
    c = Ponto3D(x,y,z);
    // v1 = arquivo.readline().split(' ')
    arquivo>>x>>y>>z;
    n = Ponto3D(x,y,z);
    // v2 = arquivo.readline().split(' ')
    arquivo>>x>>y>>z;
    v = Ponto3D(x,y,z);
    // inteiros = arquivo.readline().split(' ')
    arquivo>>d;
    arquivo>>hx;
    arquivo>>hy;
    vl = gramschmidt(v,n)
    vl.normalizado()
    n.normalizado()
    Camera3D camera = Camera3D(c,n.prod_vetorial(vl),vl,n,d,hx,hy)
}
void ler_pontos(string path){
    ifstream arquivo(path);
    // arquivo = open(path,'r')
    // m = int(arquivo.readline())
    // i = int(arquivo.readline())
    int i;
    arquivo>>m>>i;
    while (i-->0){
        // ponto = arquivo.readline().split(' ')
        float x,y,z;
        arquivo>>x>>y>>z;
        bezier.push_back(Ponto3D(x,y,z));
    }
}
// void init(){
//     pontos;
//     triangulos = [];
//     bezier = [];
//     luz = Luz3D(0,0,0,0,0,0,0,0);
//     camera = Camera3D(0,0,0,0,0,0,0);
// }
Ponto3D mult_matriz(Ponto3D u,Ponto3D v,Ponto3D n,Ponto3D p){
    return Ponto3D(u.x*p.x+u.y*p.y+u.z*p.z,
                    v.x*p.x+v.y*p.y+v.z*p.z,
                    n.x*p.x+n.y*p.y+n.z*p.z);
}

// utilizados para passar os pontos da base mundo para a base camera
void get_pontos_camera(){

    for (int i =0;i<pontos.size();i++){
        Ponto3D a = mult_matriz(camera.u, camera.v,camera.n, pontos[i].p - camera.c);
        Ponto3D b = mult_matriz(camera.u, camera.v,camera.n, (pontos[i].normal + pontos[i].p) - camera.c);
        pontos_camera.push_back(PontosNormal3D(a,b-a));
    }
    luz_camera = luz;
    luz_camera.pl = mult_matriz(camera.u, camera.v,camera.n, luz.pl - camera.c);
}
class Ponto2D{
    float x,y;
    Ponto2D(float x,float y):x(x),y(y){}
    Ponto2D(const Ponto2D &p):x(p.x),y(p.y){}
    Ponto2D operator +(const Ponto2D &p) const{
      Ponto2D(x + p.x,y + p.y);
    }
    Ponto2D operator -(const Ponto2D &p) const{
      Ponto2D(x - p.x,y - p.y);
    }
    Ponto2D operator *(float a) const{
      Ponto2D(x*a,y*a);
    }
    void normalizado(){
        float tam = this.norma();
        x = x/tam;
        y = y/tam;
    }
    float norma(){
        return (pow(pow(x,2) + pow(y,2),0.5));
    }
    float prod_escalar(const Ponto2D &p){
        return (x*p.x + y*p.y);
    }
}
void init_z_buffer(){
    for(int i = 0;i<width;i++){
      for(int j=0;i<height;i++){
        z_buffer[i][j] = INT_MAX;
      }
    }
}

void get_ponto_tela(){
    for (int i=0; i<pontos_camera.size();i++){
        float x = -50, y = -50;
        if (pontos_camera[i].p.z > 0){
            x = (camera.d/camera.hx)* (pontos_camera[i].p.x/pontos_camera[i].p.z);
            y = (camera.d/camera.hy) *(pontos_camera[i].p.y / pontos_camera[i].p.z);
        }
        pontos_tela.push_back(Ponto2D((x + 1)*width/2, (1-y)*height/2));
    }
}
class Linha{

    float a,b,c,d;
    Linha(float a,float b,float c,float d):a(a),b(b),c(c),d(d){}
    Linha(const Linha &l):a(l.a),b(l.b),c(l.c),d(l.d){}
    Linha operator /(float x) const {
      if (x == 0){
        x = 1;
      }
      return Linha(a/x,b/x,c/x,d/x);
    }
    Linha operator %(const Linha %x) const {
      return Linha(a-x.a*a,b-x.b*a,c-x.c*a,d-x.d*a);
    }
    Linha operator ^(const Linha %x) const {
      return Linha(a,b-x.b*b,c-x.c*b,d-x.d*b);
    }
    Linha operator +(const Linha %x) const {
      return Linha(a,b,c-x.c*c,d-x.d*c);
    }
}
class Escalona{

    Linha l1,l2,l3;
    Escalona(const Linha &l1,const Linha &l2,const Linha &l3):l1(l1),l2(l2),l3(l3){}
    Escalona(const Escalona &l):l1(l.l1),l2(l.l2),l3(l.l3){}

    Linha esc(){
      l1 = l1/l1.a;
      l2 = l2%l1;
      l3 = l3%l1;
      l2 = l2/l2.b;
      l1 = l1^l2;
      l3 = l3^l2;
      l3 = l3/l3.c;
      l1 = l1+l3;
      l2 = l2 + l3;
      return Linha(l1.d,l2.d,l3.d);
    }

}
bool into(Ponto2D p){
    return (p.x < width && p.x >= 0 && p.y < height && p.y >= 0);
}

void get_into_tela(){
    pontos_camera.clear();
    pontos_tela.clear();
    z_buffer.clear();
    get_pontos_camera();
    init_z_buffer();
    get_ponto_tela();
    glPointSize(2);
    glBegin(GL_POINTS);
    for (int i=0;i<triangulos.size();i++){
        Ponto2D p1,p2,p3;
        p1 = pontos_tela[triangulos[i].p1];
        p2 = pontos_tela[triangulos[i].p2];
        p3 = pontos_tela[triangulos[i].p3];
        if(into(p1) and into(p2) and into(p3)){
            if (triangulos[i].reta()){
                triangulos[i].sort_asc_x();
                draw_line(i.p1,i.p3);
            }
            else{
                triangulos[i].sort_asc_y();
                triangulos[i].pintar();
            }
        }
    }
    glEnd();
}
void top_triangulo(int p1,int p2,int p3){
    float slope1 = ((float)(pontos_tela[p3].x - pontos_tela[p1].x)/ (float)(pontos_tela[p3].y - pontos_tela[p1].y));
    float slope2 = ((float)(pontos_tela[p3].x - pontos_tela[p2].x) /(float)(pontos_tela[p3].y - pontos_tela[p2].y));
    float x1 = pontos_tela[p3].x;
    float x2 = pontos_tela[p3].x + 0.5;

    if (slope1 < slope2)
      swap(slope1,slope2);

    float sline = pontos_tela[p3].y;
    Linha l3 = Linha(1,1,1,1);
    while(sline > pontos_tela[p1].y){
        float x_aux = x1;
        while(x_aux <= x2){
            Linha l1 = Linha(pontos_tela[p1].x,pontos_tela[p2].x,pontos_tela[p3].x,
                x_aux);
            Linha l2 = Linha(pontos_tela[p1].y,pontos_tela[p2].y,pontos_tela[p3].y,
                sline);
            Linha esc = Escalona(l1,l2,l3).esc();
            Ponto3D ponto = pontos_camera[p1].p*esc.a + pontos_camera[p2].p*esc.b + pontos_camera[p3].p*esc.c;
            if (z_buffer[int(x_aux+0.5)][int(sline + 0.5)] > ponto.z){
                z_buffer[int(x_aux+0.5)][int(sline + 0.5)] = ponto.z;
                Ponto3D normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b + pontos_camera[p3].normal*c;
                RGB cor = get_cor(ponto,normal);
                cor = cor/255.0;
                glColor3f(cor.r,cor.g,cor.b);
                glVertex2i(int(x_aux+0.5),int(sline+0.5));
            }
            x_aux += 2;
        }
        sline-=2;
        x1 -= slope1;
        x2 -= slope2;
    }
}

Linha get_ab(Ponto2D p1,Ponto2D p2,Ponto2D p3){
    if (eq(abs(p2.x - p1.x),0))
        return Linha(1,0,0,0);
    b = (p3.x-p1.x)/(p2.x-p1.x);
    a = 1 - b;
    return Linha(a,b,0,0);
}

void draw_line(int p1,int p2){
    float x1 = pontos_tela[p1].x;
    float sline = pontos_tela[p1].y;

    float x2 = pontos_tela[p2].x;
    while(x1 <= x2){
        Linha esc = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline));
        Ponto3D ponto = pontos_camera[p1].p*a + pontos_camera[p2].p*b
        if (z_buffer[int(x1+0.5)][int(sline+0.5)] > ponto.z){
            z_buffer[int(x1+0.5)][int(sline+0.5)] = ponto.z;
            Ponto3D normal = pontos_camera[p1].normal*esc.a + pontos_camera[p2].normal*esc.b;
            RGB cor = get_cor(ponto,normal);
            cor = cor/255.0;
            glColor3f(cor.r,cor.g,cor.b);
            glVertex2f(x1,sline);
        }
        x1 += 1;
    }
}

void bottom_triangulo(int p1,int p2,int p3){
    float slope1 = (float(pontos_tela[p2].x - pontos_tela[p1].x)/ float(pontos_tela[p2].y - pontos_tela[p1].y));
    float slope2 = (float(pontos_tela[p3].x - pontos_tela[p1].x) / float(pontos_tela[p3].y - pontos_tela[p1].y));

    float x1 = pontos_tela[p1].x;
    float x2 = pontos_tela[p1].x + 0.5;

    if (slope1 > slope2)
        swap(slope1,slope2);

    float sline = pontos_tela[p1].y;
    Linha l3 = Linha(1,1,1,1);
    while(sline <= pontos_tela[p2].y){
        float x_aux = x1;
        while(x_aux <= x2){
            Linha l1 = Linha(pontos_tela[p1].x,pontos_tela[p2].x,pontos_tela[p3].x,
                x_aux);
            Linha l2 = Linha(pontos_tela[p1].y,pontos_tela[p2].y,pontos_tela[p3].y,
                sline);
            Linha esc = Escalona(l1,l2,l3).esc();
            Ponto3D ponto = pontos_camera[p1].p*esc.a + pontos_camera[p2].p*esc.b + pontos_camera[p3].p*esc.c;
            if (z_buffer[int(x_aux+0.5)][int(sline + 0.5)] > ponto.z){
                z_buffer[int(x_aux+0.5)][int(sline + 0.5)] = ponto.z;
                Ponto3D normal = pontos_camera[p1].normal*a + pontos_camera[p2].normal*b + pontos_camera[p3].normal*c;
                RGB cor = get_cor(ponto,normal);
                cor = cor/255.0;
                glColor3f(cor.r,cor.g,cor.b);
                glVertex2i(int(x_aux+0.5),int(sline+0.5));
            }
            x_aux += 1;
        }
        sline+=1;
        x1 += slope1;
        x2 += slope2;
    }
}

Ponto3D bezier_casteljau(float t){
    vector<Ponto3D> points = bezier;
    while(points.size()>1){
        point = points
        points.clear();
        for (int i = 0;i<point.size() - 1;i++){
            Ponto3D p1 = point[i]*(1-t);
            Ponto3D p2 =point[i+1]*t;
            points.push_back(p1+p2);
        }
    }
    return points[0];
}
// void mov_camera(){
//     float t = 0;
//     float fator = 1.0 / m;
//
//     while (t <= 1){
//         camera.c = bezier_casteljau(t);
//         t += fator;
//         init_z_buffer();
//         glClear(GL_COLOR_BUFFER_BIT);
//         get_into_tela();
//     }
// }
void display(){
    float t = 0;
    float fator = 1.0 / m;
    while (t <= 1){
        glClear(GL_COLOR_BUFFER_BIT);
        camera.c = bezier_casteljau(t);
        t += fator;
        get_into_tela();
        glFlush();
    }
}
void reshape(GLsizei width_v, GLsizei height_v){
    glViewport(0, 0, width_v, height_v);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, width, height, 0.0, -5.0, 5.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}
