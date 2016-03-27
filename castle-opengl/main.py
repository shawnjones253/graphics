"""
Shawn Jones
CSCI 480
Assignment 3 - Castle in OpenGL
"""

#"grass.jpg" from http://ursamart.com/images/fd2/grass-texture-seamless-decorating-3.jpg

#Controls:
#Mouse: camera look
#W: Move forward
#S: Move backward
#A: Strafe left
#D: Strafe right
#Space: Move up
#C: Move down
#Shift: Move faster
#Esc: Quit

import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

from mypsurfs import cylinder, islandAndMoat, reflectedSurface, cylinderCrenellations, cylinderTop
from specials import rectangle, rectangleCrenellation
from loadtexture import loadTexture
from meshes import *
from transforms import *
from camera import Camera

def readShader(filename):
    with open(os.path.join(".",filename)) as fp:
        return fp.read()

def makeShader(vertfile, fragfile):
    return compileProgram(
        compileShader(readShader(vertfile), GL_VERTEX_SHADER),
        compileShader(readShader(fragfile), GL_FRAGMENT_SHADER)
        )

def initializeVAO():
    n = 1
    vaoArray = N.zeros(n, dtype=N.uint)
    vaoArray = glGenVertexArrays(n)
    glBindVertexArray( vaoArray )

# Called once at application start-up.
# Must be called after we have an OpenGL context, i.e. after the pygame
# window is created
def init():
    global theMeshes, theLight, theCamera, theScreen, skyColor
    initializeVAO()
    glEnable(GL_DEPTH_TEST)

    # Add our objects

    # LIGHT
    theLight = N.array((0.577, 0.577, 0.577, 0.0),dtype=N.float32)

    # OBJECTS
    islandHeight = 5.0
    surroundingLandHeight = 1.0
    moatDepth = -10.0
    islandRadius = 50.0
    moatInnerRadius = 65.0
    moatOuterRadius = 90.0
    outerShoreRadius = 100.0
    terrainXZMax = 400.0
    terrainNumSamples = 400

    tRadius = 6.0
    tThickness = 1.0
    height = 15.0
    crenHeight = 2.0

    wThickness = 1.0

    castleRadius = islandRadius - tRadius + 1
    
    pi = N.pi
    qtrpi = N.pi/4

    skyColor = (0.0, 0.47, 0.67, 0.0)
    
    towerList = [
        #radius, height, numArcs, crenWidth, crenHeight, moveBackUnits, moveRightUnits
        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*19/12)), castleRadius*(N.cos(pi*19/12))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*17/12)), castleRadius*(N.cos(pi*17/12))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*7/6)), castleRadius*(N.cos(pi*7/6))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*5/6)), castleRadius*(N.cos(pi*5/6))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*2/3)), castleRadius*(N.cos(pi*2/3))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi/3)), castleRadius*(N.cos(pi/3))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi/6)), castleRadius*(N.cos(pi/6))),

        (tRadius, height, 128, tThickness, 8, crenHeight,
         castleRadius*(-N.sin(pi*11/6)), castleRadius*(N.cos(pi*11/6))),

        (12.0, 35.0, 256, tThickness*2, 16, crenHeight*2, 0.0, 0.0)
        ]

    wallList = [
        #wallWidth, wallHeight, wallThickness,
        #numCren, crenHeight, moveBackUnits, moveRightUnits, yawUnits
        (castleRadius*(N.cos(pi*19/12)-N.cos(pi*17/12))-tRadius*2,
         height, wThickness, 3, crenHeight,
         (-N.sin(pi*17/12)), 0.0, 0.0),
        
        (castleRadius*(2*N.sin((pi*17/12-pi*7/6)/2))-tRadius*2,
         height, wThickness, 4, crenHeight,
         ((-N.sin(pi*17/12)-N.sin(pi*7/6))/2),
         ((N.cos(pi*17/12)+N.cos(pi*7/6))/2),
         ((pi*3/2) - ((pi*17/12)-(((pi*17/12)-(pi*7/6))/2)))/-qtrpi),

        (castleRadius*(2*N.sin((pi*7/6-pi*5/6)/2))-tRadius*2,
         height, wThickness, 5, crenHeight,
         ((-N.sin(pi*7/6)-N.sin(pi*5/6))/2),
         ((N.cos(pi*7/6)+N.cos(pi*5/6))/2),
         ((pi*3/2) - ((pi*7/6)-(((pi*7/6)-(pi*5/6))/2)))/-qtrpi),

        (castleRadius*(2*N.sin((pi*5/6-pi*2/3)/2))-tRadius*2,
         height, wThickness, 3, crenHeight,
         ((-N.sin(pi*5/6)-N.sin(pi*2/3))/2),
         ((N.cos(pi*5/6)+N.cos(pi*2/3))/2),
         ((pi*3/2) - ((pi*5/6)-(((pi*5/6)-(pi*2/3))/2)))/-qtrpi),

        (castleRadius*(2*N.sin((pi*2/3-pi/3)/2))-tRadius*2,
         height, wThickness, 5, crenHeight,
         ((-N.sin(pi*2/3)-N.sin(pi/3))/2),
         ((N.cos(pi*2/3)+N.cos(pi/3))/2),
         ((pi*3/2) - ((pi*2/3)-(((pi*2/3)-(pi/3))/2)))/-qtrpi),

        (castleRadius*(2*N.sin((pi/3-pi/6)/2))-tRadius*2,
         height, wThickness, 3, crenHeight,
         ((-N.sin(pi/3)-N.sin(pi/6))/2),
         ((N.cos(pi/3)+N.cos(pi/6))/2),
         ((pi*3/2) - ((pi/3)-(((pi/3)-(pi/6))/2)))/-qtrpi),

        (castleRadius*(1.0)-tRadius*2,
         height, wThickness, 5, crenHeight,
         ((-N.sin(pi/6)-N.sin(pi*11/6))/2),
         ((N.cos(pi/6)+N.cos(pi*11/6))/2),
         -6.0),

        (castleRadius*(2*N.sin((pi*11/6-pi*19/12)/2))-tRadius*2,
         height, wThickness, 4, crenHeight,
         ((-N.sin(pi*11/6)-N.sin(pi*19/12))/2),
         ((N.cos(pi*11/6)+N.cos(pi*19/12))/2),
         -6.0 - (2.0-((pi*3/2) - ((pi*11/6)-(((pi*11/6)-(pi*19/12))/2)))/-qtrpi))
        ]
    
    theMeshes = []

    #towers
    for tower in towerList:
        (towerRadius, towerHeight, nArcs,
         towerThickness, crenWidth, crenHeight,
         moveBackUnits, moveRightUnits) = tower

        #create tower
        verts,elements = cylinder(towerRadius,
                                  towerHeight,
                                  nArcs)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(islandHeight)
        
        verts,elements = reflectedSurface(verts,
                                          elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(-islandHeight)

        #create inside wall of tower
        verts,elements = cylinder(-towerRadius+towerThickness,
                                  towerHeight,
                                  nArcs)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(islandHeight)
        
        verts,elements = reflectedSurface(verts,
                                          elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(-islandHeight)

        #create top for tower
        verts,elements = cylinderTop(towerRadius, towerThickness, nArcs)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(towerHeight)
        theMeshes[-1].moveUp(islandHeight)

        verts,elements = reflectedSurface(verts, elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits)
        theMeshes[-1].moveRight(moveRightUnits)
        theMeshes[-1].moveUp(-towerHeight)
        theMeshes[-1].moveUp(-islandHeight)
        
        #add crenellations to tower
        vertsList, elementsList = cylinderCrenellations(towerRadius,
                                                        towerHeight,
                                                        nArcs,
                                                        crenWidth,
                                                        crenHeight)
        for verts,elements in zip(vertsList,elementsList):
            theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                            N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                            100.0,
                                            getArrayBuffer(verts),
                                            getElementBuffer(elements),
                                            len(elements),
                                            makeShader("worley.vert", "worley.frag")
                                            ))
            theMeshes[-1].moveBack(moveBackUnits)
            theMeshes[-1].moveRight(moveRightUnits)
            theMeshes[-1].moveUp(islandHeight)
            theMeshes[-1].moveUp(towerHeight-0.01)
            
            verts,elements = reflectedSurface(verts, elements)
            theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                            N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                            100.0,
                                            getArrayBuffer(verts),
                                            getElementBuffer(elements),
                                            len(elements),
                                            makeShader("worley.vert", "worleyinverted.frag")
                                            ))
            theMeshes[-1].moveBack(moveBackUnits)
            theMeshes[-1].moveRight(moveRightUnits)
            theMeshes[-1].moveUp(-islandHeight)
            theMeshes[-1].moveUp(-towerHeight+0.01)

    #walls
    for wall in wallList:
        (wallWidth, wallHeight, wallThickness, numCren, crenHeight,
         moveBackUnits, moveRightUnits, yawUnits) = wall

        #create outside wall
        verts,elements = rectangle(wallWidth, wallHeight)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack((moveBackUnits) * (castleRadius+(wallThickness/2)))
        theMeshes[-1].moveRight((moveRightUnits) * (castleRadius+(wallThickness/2)))
        theMeshes[-1].moveUp(wallHeight/2)
        theMeshes[-1].moveUp(islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)
        
        verts,elements = reflectedSurface(verts, elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack((moveBackUnits) * (castleRadius+(wallThickness/2)))
        theMeshes[-1].moveRight((moveRightUnits) * (castleRadius+(wallThickness/2)))
        theMeshes[-1].moveUp(-wallHeight/2)
        theMeshes[-1].moveUp(-islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)

        #add crenellations to wall
        verts,elements,xcenters = rectangleCrenellation(wallWidth, numCren, crenHeight)
        rverts,relements = reflectedSurface(verts, elements)
        for i in range(numCren):
            theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
            theMeshes[-1].moveBack((moveBackUnits) * (castleRadius+(wallThickness/2)))
            theMeshes[-1].moveRight((moveRightUnits) * (castleRadius+(wallThickness/2)))
            theMeshes[-1].moveUp(crenHeight/2 + wallHeight)
            theMeshes[-1].moveUp(islandHeight)
            yawCopy = yawUnits
            while (yawCopy < -1.0):
                theMeshes[-1].yaw(-1.0)
                yawCopy += 1.0
            theMeshes[-1].yaw(yawCopy)
            theMeshes[-1].moveRight(xcenters[i] - wallWidth/2)
        
            theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(rverts),
                                        getElementBuffer(relements),
                                        len(relements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
            theMeshes[-1].moveBack((moveBackUnits) * (castleRadius+(wallThickness/2)))
            theMeshes[-1].moveRight((moveRightUnits) * (castleRadius+(wallThickness/2)))
            theMeshes[-1].moveUp(-crenHeight/2 - wallHeight)
            theMeshes[-1].moveUp(-islandHeight)
            yawCopy = yawUnits
            while (yawCopy < -1.0):
                theMeshes[-1].yaw(-1.0)
                yawCopy += 1.0
            theMeshes[-1].yaw(yawCopy)
            theMeshes[-1].moveRight(xcenters[i] - wallWidth/2)

        #create top of wall
        yout = N.square(((moveBackUnits) * (castleRadius+(wallThickness/2))))
        xout = N.square(((moveRightUnits) * (castleRadius+(wallThickness/2))))
        rout = N.sqrt(yout + xout)
        yin  = N.square(((moveBackUnits) * (castleRadius-(wallThickness/2))))
        xin  = N.square(((moveRightUnits) * (castleRadius-(wallThickness/2))))
        rin  = N.sqrt(yin + xin)
        wallTopThickness = rout - rin
        verts,elements = rectangle(wallWidth, wallTopThickness)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits*castleRadius)
        theMeshes[-1].moveRight(moveRightUnits*castleRadius)
        theMeshes[-1].moveUp(wallHeight)
        theMeshes[-1].moveUp(islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)
        for i in range(2):
            theMeshes[-1].pitch(1.0)
        
        verts,elements = reflectedSurface(verts, elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack(moveBackUnits*castleRadius)
        theMeshes[-1].moveRight(moveRightUnits*castleRadius)
        theMeshes[-1].moveUp(-wallHeight)
        theMeshes[-1].moveUp(-islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)
        for i in range(2):
            theMeshes[-1].pitch(1.0)
        
        #create inside wall
        verts,elements = rectangle(wallWidth, wallHeight)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worley.frag")
                                        ))
        theMeshes[-1].moveBack((moveBackUnits) * (castleRadius-(wallThickness/2)))
        theMeshes[-1].moveRight((moveRightUnits) * (castleRadius-(wallThickness/2)))
        theMeshes[-1].moveUp(wallHeight/2)
        theMeshes[-1].moveUp(islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)
        for i in range(4):
            theMeshes[-1].yaw(-1.0)
        
        verts,elements = reflectedSurface(verts, elements)
        theMeshes.append(proceduralMesh(N.array((0.373,0.361,0.314,1.0),dtype=N.float32),
                                        N.array((0.475,0.475,0.475,1.0),dtype=N.float32),
                                        100.0,
                                        getArrayBuffer(verts),
                                        getElementBuffer(elements),
                                        len(elements),
                                        makeShader("worley.vert", "worleyinverted.frag")
                                        ))
        theMeshes[-1].moveBack((moveBackUnits) * (castleRadius-(wallThickness/2)))
        theMeshes[-1].moveRight((moveRightUnits) * (castleRadius-(wallThickness/2)))
        theMeshes[-1].moveUp(-wallHeight/2)
        theMeshes[-1].moveUp(-islandHeight)
        yawCopy = yawUnits
        while (yawCopy < -1.0):
            theMeshes[-1].yaw(-1.0)
            yawCopy += 1.0
        theMeshes[-1].yaw(yawCopy)
        for i in range(4):
            theMeshes[-1].yaw(-1.0)
       
    #add terrain
    verts,elements = islandAndMoat(islandHeight, surroundingLandHeight,
                                   moatDepth, islandRadius,
                                   moatInnerRadius, moatOuterRadius, outerShoreRadius,
                                   terrainXZMax, terrainNumSamples,
                                   noiseY = True, noiseVariance = 2.0, noiseScale = 0.2)
    theMeshes.append(flatTexturedMesh(loadTexture("grass.jpg", magFilter=GL_LINEAR),
                                      getArrayBuffer(verts),
                                      getElementBuffer(elements),
                                      len(elements),
                                      makeShader("flattextured.vert", "flattextured.frag"),
                                      scaleuv = N.array((32.0,32.0),dtype=N.float32),
                                      useFog = True,
                                      fogColor = N.array(skyColor,dtype=N.float32),
                                      fogStart = 300.0,
                                      fogEnd = 325.0
                                      ))
    verts,elements = reflectedSurface(verts, elements)
    theMeshes.append(flatTexturedMesh(loadTexture("grass.jpg", magFilter=GL_LINEAR),
                                      getArrayBuffer(verts),
                                      getElementBuffer(elements),
                                      len(elements),
                                      makeShader("flattextured.vert", "flattexturedinverted.frag"),
                                      scaleuv = N.array((32.0,32.0),dtype=N.float32),
                                      useFog = True,
                                      fogColor = N.array(skyColor,dtype=N.float32),
                                      fogStart = 300.0,
                                      fogEnd = 325.0
                                      ))
    
    # CAMERA
    width, height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 325.0
    lens = 4.0  # "longer" lenses mean more telephoto
    theCamera = Camera(lens, near, far, aspectRatio)
    
    theCamera.moveBack(180.0)
    theCamera.moveUp(40.0)
    theCamera.moveRight(-40.0)
    theCamera.yaw(-.25)
    theCamera.pitch(.20)

# Called to redraw the contents of the window
def display(time):
    global theMeshes, theLight, theCamera, skyColor
    # Clear the display
    glClearColor(skyColor[0], skyColor[1], skyColor[2], skyColor[3])
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    for theMesh in theMeshes:
        theMesh.display(theCamera.view(),
                        theCamera.projection(),
                        theLight)

def main():
    global theCamera, theScreen
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    init()
    clock = pygame.time.Clock()
    time = 0.0
    while True:
        clock.tick(30)
        time += 0.01
        # Event queued input
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
        # Polling input is better for a real time camera
        pressed = pygame.key.get_pressed()

        # keys for zoom:
        if pressed[K_z]:
            theCamera.zoomIn(1.015)
        if pressed[K_x]:
            theCamera.zoomOut(1.015)

        # arrow keys for movement:
        movespeed = 0.5
        if pressed[K_LSHIFT]:
            movespeed *= 4
        if pressed[K_d] | pressed[K_RIGHT]:
            theCamera.moveRight(movespeed)
        if pressed[K_a] | pressed[K_LEFT]:
            theCamera.moveRight(-movespeed)
        if pressed[K_w] | pressed[K_UP]:
            theCamera.moveBack(-movespeed)
        if pressed[K_s] | pressed[K_DOWN]:
            theCamera.moveBack(movespeed)

        # move up with space and down with c
        if pressed[K_SPACE]:
            theCamera.moveUp(movespeed)
        if pressed[K_c]:
            theCamera.moveUp(-movespeed)
        
        # mouse for rotation
        rotspeed = 0.1
        mousespeed = 0.5*rotspeed
        x,y = pygame.mouse.get_pos()
        if (x > 0) & (y > 0):
            xDisplacement = x - 0.5*width
            yDisplacement = y - 0.5*height
            # normalize:
            xNormed = xDisplacement/width
            yNormed = -yDisplacement/height
            newx = int(x - xDisplacement*mousespeed)
            newy = int(y - yDisplacement*mousespeed)
            if (newx != x) | (newy != y):
                theCamera.pan(-xNormed * rotspeed)
                theCamera.tilt(-yNormed * rotspeed)
                pygame.mouse.set_pos((newx,newy))

        display(time)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    except RuntimeError, err:
        for s in err:
            print s
        raise RuntimeError(err)
    finally:
        pygame.quit()


