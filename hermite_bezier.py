from OpenGL.GL import *
from OpenGL.GL.exceptional import glEnd
from OpenGL.GLUT import *
from ui import add, remove

window_w, window_h = 800,600 # tamanho da tela

pontos = [] # array com os pontos que o usuário inseriu
vetores = [] # array com os vetores que o usuário inseriu
i_pontos = 0 # indece do pont que está sendo clicado ou está sendo inserido
i_vetores = 0 # indece do vetor que está sendo clicado ou está sendo inserido
point_size = 13.0 # tamanho do quadrado desenhado para um ponto
vector_size = 10.0 # tamanho do quadrado desenhado para um vetor
parameter = []  # vetor com os paramentros inseridos pelo usuário

quant_t = 50 # quantidade de subdivisões do valor t para desenhar a curva de bezier


PROMPT = ("F1 - Curva de Bezier On/Off", "F2 - Linhas entre pontos de controle On/Off", "F3 - Vetores On/Off", "F4 - Pontos de controle On/Off",
"F5 - Pontos dos vetores de controle On/Off", "F6 - Pontos gerados da curva de Bezier On/Off", "F7 - Limpar a tela",
          "Left Click - Inserir ponto ou vetor", "Right Click - Remover Ponto ou vetor")

# funções do sistema
curva = True # utilizado para exibir a curva de bezier
linhas_pontos = True # utilizado para exibir as linhas geradas entre os pontos de controle
linhas_vetores = True # utilizado para exibir as linhas geradas entre os pontos de controle e seus respectivos vetores de controle
pontos_pontos = True # utilizado para exibir os pontos de controle
pontos_vetores = True # utilizado para exibir os vetores de controle
pontos_bezier = True # utilizado para exibir os pontos da curva de bezier gerados


click_number = 1 # numero de pontos inseridos
p_or_v = True # utilizado para saber se o objeto que está sendo clicado é um ponto ou um vetor


# colors
color_point = (0.0, 1.0, 0.0) # cor que vai ser pintado os pontos de controle
color_vector = (0.0, 0.0, 1.0) # cor que vai ser pintado os vetores de controle
color_line_pontos = (0.0, 1.0, 0.0) # cor que vai ser pintada as linhas entre os pontos de controle
color_line_vector = (1.0, 1.0, 0.0) # cor que vai ser pintada as linhas do vetores de controle
color_point_bezier = (1.0, 1.0, 0.5) # cor que vai ser pintado os pontos de bezier gerados
color_curve = (1.0, 0.5, 1.0) # cor que vai ser denhada a curva de bezier

# utilizado para atualizar a curva com os paramentros alterados pelo usuário
def paramentros(p):
    global parameter
    parameter = p
    glutPostRedisplay()

# utilizado para excluir todos os dados da tela
def reset():
    global pontos,vetores,i_pontos,i_vetores, click_number, parameter
    for i in range(0,len(pontos)-1):
        remove(0)
    parameter = []
    pontos = []
    vetores = []
    i_pontos = 0
    i_vetores = 0
    click_number = 1
    glutPostRedisplay()


# utilizado para densenhar a curva e os pontos na tela
def display():
    global vetores, pontos, color_point, color_vector, linhas_pontos, linhas_vetores, pontos_pontos, pontos_vetores
    global color_line_pontos,color_line_vector
    glClear(GL_COLOR_BUFFER_BIT)

    # colocar texto de ajuda na tela
    y = 20
    for s in PROMPT:
        glRasterPos(10.0, y)
        y += 20
        for c in s:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    if (len(pontos) > 0) or (len(vetores)>0):

        if (pontos_pontos):
            # colocar os pontos de controle na tela
            glPointSize(point_size)
            glBegin(GL_POINTS)
            glColor3fv(color_point)
            for p in pontos:
                glVertex2f(p['x'], p['y'])
            glEnd()

        if (pontos_vetores):
            # colocar os vetores de controle na tela
            glPointSize(vector_size)
            glBegin(GL_POINTS)
            glColor3fv(color_vector)
            for p in vetores:
                glVertex2f(p['x'], p['y'])

            glEnd()

        if len(pontos) > 1:

            if(linhas_pontos):
                # Desenha as linhas entre os pontos de controle
                glBegin(GL_LINE_STRIP)
                glColor3fv(color_line_pontos)
                for p in pontos:
                    glVertex2f(p['x'], p['y'])
                glEnd()
            hermite()

        if len(vetores)>0 and linhas_vetores:
            # Desenha as linhas ligando os pontos de controle aos pontos finais de cada vetor
            glBegin(GL_LINES)
            glColor3fv(color_line_vector)
            i = 0
            while (i < len(vetores) and i < len(pontos)):
                glVertex2f(pontos[i]['x'], pontos[i]['y'])
                glVertex2f(vetores[i]['x'], vetores[i]['y'])
                i += 1
            glEnd()

    glFlush()

def hermite():
    global pontos, vetores, parameter,quant_t, pontos_bezier,color_point_bezier,color_curve, curva
    inc = 1/quant_t
    i = 0
    while (i<len(vetores)-1):
        t = 0

        # calcula os pontos de bezier
        point = []
        point.append({'x':pontos[i]['x'],'y':pontos[i]['y']})
        point.append({'x':pontos[i]['x'] + (vetores[i]['x']-pontos[i]['x'])/3*parameter[i],'y':pontos[i]['y'] + (vetores[i]['y']-pontos[i]['y'])/3*parameter[i]})
        point.append({'x':pontos[i+1]['x'] - (vetores[i+1]['x']-pontos[i+1]['x'])/3*parameter[i],'y':pontos[i+1]['y'] - (vetores[i+1]['y']-pontos[i+1]['y'])/3*parameter[i]})
        point.append({'x':pontos[i+1]['x'],'y':pontos[i+1]['y']})

        if(pontos_bezier):
            glPointSize(point_size)
            glBegin(GL_POINTS)
            glColor3fv(color_point_bezier)
            for a in point:
                glVertex2d(a['x'],a['y'])

            glEnd()

        if (curva):
            # desenha a curva de bezier
            glBegin(GL_LINE_STRIP)
            glColor3fv(color_curve)
            while (t<=1):
                bezier_casteljau(point,t)
                t += inc
            glVertex2d(pontos[i+1]['x'],pontos[i+1]['y'])
            glEnd()
        i += 1


# calcula a curva de bezier utilizando o algoritmo de casteljau
def bezier_casteljau(points, t):
    while(len(points)>1):
        point = points
        points = []
        for i in range(0,len(point) - 1):
            points.append({'x':(1-t)*point[i]['x']+t*point[i+1]['x'],'y':(1-t)*point[i]['y']+t*point[i+1]['y']})
    glVertex2d(points[0]['x'],points[0]['y'])


# atualiza a tela do opengl
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_w, window_h, 0.0, -5.0, 5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# utilizado para algumas funções do sistema
def hadleSpecialKeyboard(key, x, y):
    global curva, linhas_pontos, linhas_vetores, pontos_pontos,pontos_vetores, pontos_bezier
    if key == GLUT_KEY_F1:
        curva = not curva
    elif key == GLUT_KEY_F2:
        linhas_pontos = not linhas_pontos
    elif key == GLUT_KEY_F3:
        linhas_vetores = not linhas_vetores
    elif key == GLUT_KEY_F4:
        pontos_pontos = not pontos_pontos
    elif key == GLUT_KEY_F5:
        pontos_vetores = not pontos_vetores
    elif key == GLUT_KEY_F6:
        pontos_bezier = not pontos_bezier
    elif key == GLUT_KEY_F7:
        reset()
        return
    glutPostRedisplay()

# utilizado para pegar ação do mouse para adicionar e remover pontos e vetores
def handleMouseClick(button, state, x, y):
    global i_pontos,i_vetores,click_number,pontos, vetores, point_size, vector_size,p_or_v, paramenter
    exit_ponto = False
    exit_vetor = False
    tam_pontos = len(pontos)
    tam_vetor = len(vetores)

    # Verifica se existe ponto
    for p in range(0, tam_pontos):
        if (x >= pontos[p]['x'] - point_size / 2) and (x <= pontos[p]['x'] + point_size / 2):
            if (y >= pontos[p]['y'] - point_size / 2) and (y <= pontos[p]['y'] + point_size / 2):
                exit_ponto = True
                i_pontos = p
                p_or_v = True
                break

    # Verifica se existe vetor
    for p in range(0, tam_vetor):
        if (x >= vetores[p]['x'] - vector_size/ 2) and (x <= vetores[p]['x'] + vector_size / 2):
            if (y >= vetores[p]['y'] - vector_size / 2) and (y <= vetores[p]['y'] + vector_size / 2):
                exit_vetor = True
                i_vetores = p
                p_or_v = False
                break

    # Adiciona pontos e vetores
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN and (not exit_ponto and not exit_vetor):
            p = {'x': float(x), 'y': float(y)}
            if (click_number&1):
                pontos.append(p)
                i_pontos = len(pontos) - 1
                if(i_pontos>0):
                    parameter.append(1)
                    add()
            else:
                vetores.append(p)
                i_vetores = len(vetores) - 1
            click_number += 1
            glutPostRedisplay()

    # Deleta pontos e vetores
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN and (exit_ponto or exit_vetor):
            if(exit_ponto):
                pontos.pop(0 + i_pontos)
                if(len(pontos)>0):
                    parameter.pop(max(i_pontos-1,0))
                    remove(max(i_pontos-1,0))
                if(i_pontos + 1 <= len(vetores)):
                    vetores.pop(0 + i_pontos)
                else:
                    click_number -= 1
            elif (exit_vetor):
                vetores.pop(0 + i_vetores)
                pontos.pop(0 + i_vetores)
                if(len(pontos)>0):
                    parameter.pop(max(i_vetores-1,0))
                    remove(max(i_vetores - 1,0))

            glutPostRedisplay()


# movimentacao dos pontos e vetores
def move_point(x, y):
    global i_vetores, i_pontos, p_or_v,pontos, vetores
    if p_or_v:
        pontos[i_pontos]['x'] = x
        pontos[i_pontos]['y'] = y
    else:
        vetores[i_vetores]['x'] = x
        vetores[i_vetores]['y'] = y
    glutPostRedisplay()


def main_hermite():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_w, window_h)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("PG - 2016.2")

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLineWidth(3.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Starting settings
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(handleMouseClick)
    glutMotionFunc(move_point)
    glutSpecialUpFunc(hadleSpecialKeyboard)
    glutMainLoop()

if __name__ == "__main__":
    main_hermite()