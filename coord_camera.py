from leitura import *

pontos_cam = 0
triangulos_cam = 0
luz_cam = 0
camera_cam = 0

def get_valores():
    global pontos_cam, triangulos_cam, luz_cam, camera_cam
    pontos_cam, triangulos_cam, luz_cam, camera_cam = get_dados()

def m_base():
    global pontos_cam, triangulos_cam, luz_cam, camera_cam
    for i in range(0,len(pontos_cam)):
        pontos_cam[i].p = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,pontos_cam[i].p)
        pontos_cam[i].normal = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,pontos_cam[i].normal)

    for i in range(0,len(luz_cam)):
        luz_cam[i].p = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,luz_cam[i].p)

    for i in range(0,len(triangulos_cam)):
        triangulos_cam[i].p1 = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,triangulos_cam[i].p1)
        triangulos_cam[i].p2 = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,triangulos_cam[i].p2)
        triangulos_cam[i].p3 = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,triangulos_cam[i].p3)
        triangulos_cam[i].normal = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,triangulos_cam[i].normal)

    camera_cam.c = mult_matriz(camera_cam.u,camera_cam.v,camera_cam.n,camera_cam.c)

def mult_matriz(u,v,n,p):
    return Ponto3D(u.x*p.x+u.y*p.y+u.z*p.z,
                    v.x*p.x+v.y*p.y+v.z*p.z,
                    n.x*p.x+n.y*p.y+n.z*p.z)


main()
get_valores()
m_base()
for i in range(0,100):
    print (camera_cam.c)
    ler_camera('camera.txt')
    get_valores()
    m_base()
