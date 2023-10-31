import pygame               #pip install pygame
import time
from pygame.locals import *
from OpenGL.GL import *     #pip install PyOpenGL
from OpenGL.GLU import *
import detect
import cv2 as cv

colors_cube = ((1,0,0),
          (0,1,0),
          (0,0,1),
          (0,1,0))

surfaces_cube = ((0,1,3,2),
            (2,3,5,4),
            (4,5,7,6),
            (0,1,7,6),
            (1,3,5,7),
            (0,2,4,6))

vert_cube = ((0.25, -0.25, -0.25),(0.25, 0.25, -0.25),
            (-0.5, 0.25, -0.25),(-0.5, -0.25, -0.25),
            (0.25, -0.25, 0.25),(0.25, 0.25, 0.25),
            (-0.5, -0.25, 0.25),(-0.5, 0.25, 0.25))

colors_tri = ((1,0,0),
          (0,1,0),
          (0,0,1),
          (0,1,0))

surfaces_tri = ((0,1,4),
            (1,2,4),
            (3,2,4),
            (0,3,4),
            (0,1,2,3))

vert_tri = ((0.5,0,0),
            (0,0,-0.5),
            (-0.5,0,0),
            (0,0,0.5),
            (0,-1,0))


def drawCube(vertices_cube):
    glBegin(GL_QUADS)
    for surface_cube in surfaces_cube:
        x = 0
        for vertex_cube in surface_cube:
            glColor3fv(colors_cube[x])
            glVertex3fv(vertices_cube[vertex_cube])
            x +=1
    glEnd()

def drawTriangle(vertices_tri):
    glBegin(GL_TRIANGLES)
    for surface_tri in surfaces_tri:
        x = 0
        for vertex_tri in surface_tri:
            glColor3fv(colors_tri[x])
            glVertex3fv(vertices_tri[vertex_tri])
            x +=1
    glEnd()


def myOpenGL():
    global vert_cube,vert_tri
    cap = cv.VideoCapture(0)
    fps_start_time = 0
    fps =0   

    pygame.init()
    display = (int(cap.get(3)), int(cap.get(4)))
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0.0, 0.0, -10)
    
    model=detect.modDel()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        ret,img_bgr = cap.read()
        
        fps_end_time=time.time()
        time_diff=fps_end_time - fps_start_time
        fps = 1/(time_diff)
        fps_start_time = fps_end_time
        
        print("++++++++++++++: ",fps)
        
        img_bgr=cv.cvtColor(img_bgr,cv.COLOR_BGR2RGB)  
        if ret == False:
            exit(1)
        
        img_result, points = detect.process(img_bgr,model)
            
        image = img_result
        textureID = glGenTextures(1);

        glBindTexture(GL_TEXTURE_2D, textureID); 
 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, cap.get(3), cap.get(4), 0, GL_RGB, GL_UNSIGNED_BYTE, image);

        glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1) #큐브나 좌표축 그릴 때 사용한 색의 영향을 안받을려면 필요

        screenW = cap.get(3)
        screenH = cap.get(4)
        
        x = screenW / 100.0;
        y = screenH / 100.0;
        
        #72~84
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 1.0); glVertex3f(-x, -y, 0.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(x, -y, 0.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(x, y, 0.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-x, y, 0.0);
        glEnd();
      
        if len(points) > 1:

            px = (points[0] - screenW/2.0)*(1.0/(screenW/2.0)) * 5
            py = -(points[1] - screenH/2.0)*(1.0/(screenH/2.0)) * 5
            
            vert_cube = ((px+0.25,py+1,0.25), (px+0.25,py+1.5,0.25),
                         (px-0.25,py+1,0.25), (px-0.25,py+1.5,0.25),
                         (px-0.25,py+1,0.75), (px-0.25,py+1.5,0.75),
                         (px+0.25,py+1,0.75), (px+0.25,py+1.5,0.75))
           
            vert_tri = ((px+0.5,py+1,0.5), (px,py+1,0),
                       (px-0.5,py+1,0) , (px,py+1,0.75),
                       (px,py,0.5))

        drawCube(vert_cube)
        drawTriangle(vert_tri)
        
        pygame.display.flip()
        
myOpenGL()