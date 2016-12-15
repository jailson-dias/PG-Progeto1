#include <bits/stdc++.h>
#include <iostream>
#include <fstream>
#include <thread>
#include "glut.h"
//#include <unistd.h>
#include <chrono>

using namespace std;


bool eq(float a,float b){
    if (abs(a - b)<(10e-9))
        return true;
    return false;
}


class Ponto2D{
  public:
    float x,y;
    Ponto2D():x(0),y(0){}
    Ponto2D(float x,float y):x(x),y(y){}
    Ponto2D(const Ponto2D &p):x(p.x),y(p.y){}
    Ponto2D operator +(const Ponto2D &p) const{
      return Ponto2D(x + p.x,y + p.y);
    }
    Ponto2D operator -(const Ponto2D &p) const{
      return Ponto2D(x - p.x,y - p.y);
    }
    Ponto2D operator *(float a) const{
      return Ponto2D(x*a,y*a);
    }
    float norma(){
        return (pow(pow(x,2) + pow(y,2),0.5));
    }
    void normalizado(){
      float tam = this->norma();
      x = x/tam;
      y = y/tam;
    }
    float prod_escalar(const Ponto2D &p){
        return (x*p.x + y*p.y);
    }
};


class Ponto3D{
  public:
    float x,y,z;
    Ponto3D():x(0),y(0),z(0){}
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
    float norma(){
      return pow(pow(x,2) + pow(y,2) + pow(z,2),0.5);
    }
    void normalizado(){
      float tam = this->norma();
      if (eq(tam,0))
      tam = 1;
      x = x/tam;
      y = y/tam;
      z = z/tam;
    }
    Ponto3D prod_vetorial(const Ponto3D &v){
//        cout << y*v.z - z*v.y << endl;
      return Ponto3D(y*v.z - z*v.y,z*v.x - x*v.z,x*v.y - y*v.x);
    }

    float prod_escalar(const Ponto3D &v){
      return (x*v.x + y*v.y + z*v.z);
    }
    string to_string(){
        char res[150];
        sprintf(res,"(%.03f, %.03f, %.03f)",x,y,z);
        return res;
    }

};


class Linha{
public:

    float a,b,c,d;
    Linha():a(0),b(0),c(0),d(0){}
    Linha(float a,float b,float c,float d):a(a),b(b),c(c),d(d){}
    Linha(const Linha &l):a(l.a),b(l.b),c(l.c),d(l.d){}
    Linha operator /(float x) const {
      if (eq(x,0))
          x = 1.0f;
      return Linha(a/x,b/x,c/x,d/x);
    }
    Linha operator %(const Linha &x) const {
      return Linha(a-x.a*a,b-x.b*a,c-x.c*a,d-x.d*a);
    }
    Linha operator ^(const Linha &x) const {
      return Linha(a,b-x.b*b,c-x.c*b,d-x.d*b);
    }
    Linha operator +(const Linha &x) const {
      return Linha(a,b,c-x.c*c,d-x.d*c);
    }
    string to_string(){
        char res[150];
        sprintf(res,"(%.03f, %.03f, %.03f, %.03f)",a,b,c,d);
        return res;
    }
};


class Escalona{
public:

    Linha l1,l2,l3;
    Escalona():l1(0,0,0,0),l2(0,0,0,0),l3(0,0,0,0){}
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
      return Linha(l1.d,l2.d,l3.d,0);
    }

};


class PontosNormal3D{
  public:
    Ponto3D p,normal;
    PontosNormal3D():p(0,0,0),normal(0,0,0){}
    PontosNormal3D(const Ponto3D &p, const Ponto3D &normal): p(p),normal(normal){}
    PontosNormal3D(const PontosNormal3D &pn):p(pn.p),normal(pn.normal){}
};


class RGB{
  public:
    float r,g,b;
    RGB():r(0),g(0),b(0){}
    RGB(float r,float g,float b):r(r),g(g),b(b){}
    RGB(const RGB &r):r(r.r),g(r.g),b(r.b){}

    RGB operator *(float a) const {
      return RGB(r*a,g*a,b*a);
    }
    RGB operator *(const RGB &a) const {
      return RGB(r*a.r,g*a.g,b*a.b);
    }
    RGB operator +(const RGB &a) const {
      return RGB(min(r+a.r,255.0f),min(g+a.g,255.0f),min(b+a.b,255.0f));
    }
    RGB operator /(float a) const {
      return RGB(r/a,g/a,b/a);
    }
    string to_string(){
        char res[200];
        sprintf(res,"(%.4f,%.4f,%.4f)",r,g,b);
        return res;
    }
};


class Luz3D {
  public:
    Ponto3D pl;
    float ka,kd,ks,n;
    RGB ia,od,il;
    Luz3D():pl(0,0,0),ka(0.0),ia(0,0,0),kd(0.0),od(0,0,0),ks(0.0),il(0,0,0l),n(0.0){}
    Luz3D(const Ponto3D &pl,float ka, const RGB &ia,float kd,const RGB &od,float ks,const RGB &il, float n):pl(pl),ka(ka),ia(ia),kd(kd),od(od),ks(ks),il(il),n(n){}
    Luz3D(const Luz3D &l):pl(l.pl),ka(l.ka),ia(l.ia),kd(l.kd),od(l.od),ks(l.ks),il(l.il),n(l.n){}
};


class Camera3D{
  public:
    Ponto3D c,u,v,n;
    float d,hx,hy;
    Camera3D():c(0,0,0),u(0,0,0),v(0,0,0),n(0,0,0),d(0.0),hx(0.0),hy(0.0){}
    Camera3D(const Ponto3D &c,const Ponto3D &u,const Ponto3D &v,const Ponto3D &n,float d,float hx,float hy):c(c),u(u),v(v),n(n),d(d),hx(hx),hy(hy){}
    Camera3D(const Camera3D &c):c(c.c),u(c.u),v(c.v),n(c.n),d(c.d),hx(c.hx),hy(c.hy){}
};



static float width = 800,height = 600;
vector<PontosNormal3D> pontos_camera;
float **z_buffer;
vector<Ponto3D> bezier;
static int m = 0,tempo = 0;

vector<Ponto2D> pontos_tela;
vector<PontosNormal3D> pontos;
Luz3D luz;
Luz3D luz_camera;
Camera3D camera;


// utilizado para calcular a formula (I = Ia.ka + Ip*Op.kd.(N.L) + Ipm.ks.(R.V)^q)
RGB get_cor(Ponto3D ponto, Ponto3D normal){
    RGB ia = luz_camera.ia*luz_camera.ka;
    Ponto3D l = (luz_camera.pl-ponto);
    l.normalizado();
    normal.normalizado();
    RGB id = RGB(0,0,0);
    RGB ie = RGB(0,0,0);
    if (normal.prod_escalar(l)>=0){
        id = (luz_camera.od*luz_camera.il)*luz_camera.kd*(normal.prod_escalar(l));
        Ponto3D v = ( - ponto);
        v.normalizado();
        if (normal.prod_escalar(v)<0)
            normal = -normal;
        Ponto3D r = (normal*2)*(normal.prod_escalar(l)) - l;
        r.normalizado();
        if (v.prod_escalar(r)>=0)
            ie =(luz_camera.il)*luz_camera.ks*(pow(r.prod_escalar(v), luz_camera.n));
    }
    return (ia + id + ie);
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
            if (z_buffer[(int)(x_aux+0.5)][(int)(sline + 0.5)] > ponto.z){
                z_buffer[(int)(x_aux+0.5)][(int)(sline + 0.5)] = ponto.z;
                Ponto3D normal = pontos_camera[p1].normal*esc.a + pontos_camera[p2].normal*esc.b + pontos_camera[p3].normal*esc.c;
                RGB cor = get_cor(ponto,normal);
                cor = cor/255.0;
                glColor3f(cor.r,cor.g,cor.b);
                glVertex2i((int)(x_aux+0.5),(int)(sline+0.5));
            }
            x_aux += 1;
        }
        sline-=1;
        x1 -= slope1;
        x2 -= slope2;
    }
}

Linha get_ab(Ponto2D p1,Ponto2D p2,Ponto2D p3){
    if (eq(abs(p2.x - p1.x),0))
        return Linha(1,0,0,0);
    float b = (p3.x-p1.x)/(p2.x-p1.x);
    float a = 1 - b;
    return Linha(a,b,0,0);
}

void draw_line(int p1,int p2){
    float x1 = pontos_tela[p1].x;
    float sline = pontos_tela[p1].y;

    float x2 = pontos_tela[p2].x;
    while(x1 <= x2){
        Linha esc = get_ab(pontos_tela[p1],pontos_tela[p2],Ponto2D(x1,sline));
        Ponto3D ponto = pontos_camera[p1].p*esc.a + pontos_camera[p2].p*esc.b;
        if (z_buffer[(int)(x1+0.5)][(int)(sline+0.5)] > ponto.z){
            z_buffer[(int)(x1+0.5)][(int)(sline+0.5)] = ponto.z;
            Ponto3D normal = pontos_camera[p1].normal*esc.a + pontos_camera[p2].normal*esc.b;
            RGB cor = get_cor(ponto,normal);
            cor = cor/255.0;
            glColor3f(cor.r,cor.g,cor.b);
            glVertex2i((int)(x1+0.5),(int)(sline+0.5));
        }
        x1 += 1;
    }
}

void bottom_triangulo(int p1,int p2,int p3){
    float slope1 = ((float)(pontos_tela[p2].x - pontos_tela[p1].x)/ (float)(pontos_tela[p2].y - pontos_tela[p1].y));
    float slope2 = ((float)(pontos_tela[p3].x - pontos_tela[p1].x) / (float)(pontos_tela[p3].y - pontos_tela[p1].y));

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
            if (z_buffer[(int)(x_aux+0.5)][(int)(sline + 0.5)] > ponto.z){
                z_buffer[(int)(x_aux+0.5)][(int)(sline + 0.5)] = ponto.z;
                Ponto3D normal = pontos_camera[p1].normal*esc.a + pontos_camera[p2].normal*esc.b + pontos_camera[p3].normal*esc.c;
                RGB cor = get_cor(ponto,normal);
                cor = cor/255.0;
                glColor3f(cor.r,cor.g,cor.b);
                glVertex2i((int)(x_aux+0.5),(int)(sline+0.5));
            }
            x_aux += 1;
        }
        sline+=1;
        x1 += slope1;
        x2 += slope2;
    }
}


class TriangulosNormal3D{
  public:
    int p1,p2,p3;
    Ponto3D normal;
    TriangulosNormal3D():p1(0),p2(0),p3(0),normal(0,0,0){}
    TriangulosNormal3D(int p1, int p2, int p3, const Ponto3D &normal):p1(p1),p2(p2),p3(p3),normal(normal){}
    TriangulosNormal3D(const TriangulosNormal3D &t):p1(t.p1),p2(t.p2),p3(t.p3),normal(t.normal){}

    bool reta(){
      if (eq(abs(pontos_tela[p1].y - pontos_tela[p2].y),0) && eq(abs(pontos_tela[p1].y - pontos_tela[p3].y),0))
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
};


vector<TriangulosNormal3D> triangulos;


Ponto3D gramschmidt(Ponto3D v,Ponto3D n){
    return v - (n * (v.prod_escalar(n)/n.prod_escalar(n)));
}


void ler_objeto(char *path){

    ifstream arquivo(path);
    if(arquivo.is_open()){
        int i,j;
        arquivo >>i>>j;
        while (i-- > 0){
            float x,y,z;
            arquivo >>x>>y>>z;
            pontos.push_back(PontosNormal3D(Ponto3D(x,y,z),Ponto3D(0,0,0)));
        }
        while (j-- > 0){
            int a,b,c;
            arquivo >>a>>b>>c;
            Ponto3D p1 = pontos[a-1].p;
            Ponto3D p2 = pontos[b-1].p;
            Ponto3D p3 = pontos[c-1].p;
            Ponto3D normal = (p2-p1).prod_vetorial(p3-p1); // normal do triangulo
            normal.normalizado();
            triangulos.push_back(TriangulosNormal3D(a-1,b-1,c-1,normal));
            pontos[a-1].normal = pontos[a-1].normal + normal; // calcula a normal do ponto
            pontos[b-1].normal = pontos[b-1].normal + normal;
            pontos[c-1].normal = pontos[c-1].normal + normal;
        }

        for (int i = 0;i<pontos.size();i++){
            pontos[i].normal.normalizado(); // normalizando a normal dos pontos
        }
      }
    arquivo.close();
}


void ler_luz(char *path){

    ifstream arquivo(path);
    if(arquivo.is_open()){
        float x,y,z;
        arquivo >>x>>y>>z;
        luz.pl = Ponto3D(x,y,z);
        arquivo>>luz.ka;
        arquivo>>x>>y>>z;
        luz.ia = RGB(x,y,z);
        arquivo >>luz.kd;
        arquivo >>x>>y>>z;
        luz.od = RGB(x,y,z);
        arquivo>>luz.ks;
        arquivo>>x>>y>>z;
        luz.il = RGB(x,y,z);
        arquivo>>luz.n;
      }
    arquivo.close();
}


void ler_camera(char *path){

    ifstream arquivo(path);
    if(arquivo.is_open()){
        float x,y,z,d,hx,hy;
        arquivo >>x>>y>>z;
        Ponto3D c = Ponto3D(x,y,z);
        arquivo>>x>>y>>z;
        Ponto3D n = Ponto3D(x,y,z);
        arquivo>>x>>y>>z;
        Ponto3D v = Ponto3D(x,y,z);
        arquivo>>d;
        arquivo>>hx;
        arquivo>>hy;
        Ponto3D vl = gramschmidt(v,n);
        vl.normalizado();
        n.normalizado();
        camera = Camera3D(c,n.prod_vetorial(vl),vl,n,d,hx,hy);
      }
    arquivo.close();
}


void ler_pontos(char *path){
    ifstream arquivo(path);
    if(arquivo.is_open()){
        int i;
        arquivo>>tempo>>m>>i;
        while (i-->0){
            float x,y,z;
            arquivo>>x>>y>>z;
            bezier.push_back(Ponto3D(x,y,z));
        }
    }
    arquivo.close();
}


void init(){
    pontos.clear();
    triangulos.clear();
    bezier.clear();
     z_buffer = (float**)malloc(width*sizeof(float*));
     for (int i = 0;i<width;i++){
       z_buffer[i] = (float*)malloc(height*sizeof(float));
     }
    luz = Luz3D(Ponto3D(0,0,0),0.0,RGB(0,0,0),0.0,RGB(0,0,0),0.0,RGB(0,0,0), 0.0);
    camera = Camera3D(Ponto3D(0,0,0),Ponto3D(0,0,0),Ponto3D(0,0,0),Ponto3D(0,0,0),0.0,0.0,0.0);
}


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


void init_z_buffer(){
    for(int i = 0;i<width;i++){
      for(int j=0;j<height;j++){
        z_buffer[i][j] = INT_MAX/3;
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
        pontos_tela.push_back(Ponto2D((int)((x + 1)*width/2), (int)((1-y)*height/2)));
    }
}


bool into(Ponto2D p){
    return (p.x < width && p.x >= 0 && p.y < height && p.y >= 0);
}


void get_into_tela(){
    pontos_camera.clear();
    pontos_tela.clear();
    get_pontos_camera();
    init_z_buffer();
    get_ponto_tela();
    glPointSize(2);

    glBegin(GL_POINTS);
    for (int i=0;i<triangulos.size();i++){
        Ponto2D p1 = pontos_tela[triangulos[i].p1];
        Ponto2D p2 = pontos_tela[triangulos[i].p2];
        Ponto2D p3 = pontos_tela[triangulos[i].p3];
        if(into(p1) && into(p2) && into(p3)){
            if (triangulos[i].reta()){
                triangulos[i].sort_asc_x();
                draw_line(triangulos[i].p1,triangulos[i].p3);
            }
            else{
                triangulos[i].sort_asc_y();
                triangulos[i].pintar();
            }
        }
    }
    glEnd();
}


Ponto3D bezier_casteljau(float t){
    vector<Ponto3D> points = bezier;
    while(points.size()>1){
        vector<Ponto3D> point = points;
        points.clear();
        for (int i = 0;i<point.size() - 1;i++){
            Ponto3D p1 = point[i]*(1-t);
            Ponto3D p2 =point[i+1]*t;
            points.push_back(p1+p2);
        }
    }
    return points[0];
}


void display(){
    float t = 0;
    float fator = 1.0 / m;
    while (t <= 1){
        glClear(GL_COLOR_BUFFER_BIT);
        camera.c = bezier_casteljau(t);
        t += fator;
        get_into_tela();
        glFlush();
        this_thread::sleep_for(chrono::milliseconds(tempo));
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


void loop_arquivo(){
//    cout << "Escolhar uma das opções abaixo:" << endl;
//    cout << "1 - Alterar objeto" << endl;
//    cout << "2 - Alterar camera" << endl;
//    cout << "3 - Alterar luz" << endl;
//    cout << "4 - Alterar pontos de bezier" << endl;
    cout << "Para alterar o arquivo de entrada você precisar esperar terminar a execução atual e depois informar os quatros arquivos de entrada"<< endl;
    cout << "Digite o endereço do objeto" << endl;
    char ob[250];
    scanf("%s",ob);
    cout << "Digite o endereço da camera" << endl;
    char cam[250];
    scanf("%s",cam);
    cout << "Digite o endereço da luz" << endl;
    char ll[250];
    scanf("%s",ll);
    cout << "Digite o endereço dos pontos de bezier" << endl;
    char pb[250];
    scanf("%s",pb);
    init();
    ler_objeto(ob);
    ler_camera(cam);
    ler_luz(ll);
    ler_pontos(pb);
    glutPostRedisplay();
    /*
    int comando;
    cin >>comando;
    switch (comando) {
        case 1:
            cout << "Digite o endereço do objeto" << endl;
            pontos.clear();
            char ob[250];
            scanf("%s",ob);
            ler_objeto(ob);
            cout<<pontos.size()<<endl;
            glutPostRedisplay();
            break;
        case 2:
            cout << "Digite o endereço da camera" << endl;
            camera = Camera3D(Ponto3D(0,0,0),Ponto3D(0,0,0),Ponto3D(0,0,0),Ponto3D(0,0,0),0.0,0,0);
            char cam[250];
            scanf("%s",cam);
            ler_camera(cam);
            glutPostRedisplay();
            break;
        case 3:
            cout << "Digite o endereço da luz" << endl;
            luz = Luz3D(Ponto3D(0,0,0),0,RGB(0,0,0),0,RGB(0,0,0),0,RGB(0,0,0),0);
            char ll[250];
            scanf("%s",ll);
            ler_luz(ll);
            glutPostRedisplay();
            break;
        case 4:
            cout << "Digite o endereço dos pontos de bezier" << endl;
            bezier.clear();
            char pb[250];
            scanf("%s",pb);
            ler_pontos(pb);
            glutPostRedisplay();
            break;
        default:
            cout << "Valor Inválido" << endl;
    }*/
    loop_arquivo();
}


int main(int argc, char **argv){
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(width, height);
    glutInitWindowPosition(0, 0);
    glutCreateWindow("PG - 2016.2");

    glClearColor(1.0, 1.0, 1.0, 0.0);
    glLineWidth(3.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glutDisplayFunc(display);
    glutReshapeFunc(reshape);

    init();
    char objeto_ler[150] = "entradas/Objetos/calice2.byu";
    ler_objeto(objeto_ler);
    char luz_ler[150] = "luz.txt";
    ler_luz(luz_ler);
    char camera_ler[150] = "entradas/Cameras/calice2.cfg";
    ler_camera(camera_ler);
    char pontos_bezier[150] = "bezier.txt";
    ler_pontos(pontos_bezier);
    cout << pontos.size() << endl;
    cout << luz.ka << endl;
    cout << camera.c.x << endl;
    cout << bezier.size() << endl;
    thread t(loop_arquivo);
//    t.join();
    glutMainLoop();

    return 0;
}

/*

entradas/Objetos/calice2.byu
entradas/Cameras/calice2.cfg
luz.txt
bezier.txt

*/
