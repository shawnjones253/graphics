"""
Shawn Jones
CSCI 480
Assignment 1 - Pink Noise
main.py
"""
from __future__ import division
import os, pygame
from pygame.locals import *
import numpy as np
import noise
from settings import latticesizex, latticesizey, persistence, numOctaves
from settings import colorStops, picsize_x, picsize_y

if __name__ == "__main__":
    main_dir = os.getcwd() 
else:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def getColor(value, tuples):
    """
    this function takes a value from 0 to 1 inclusive
    and a set of tuples (r,g,b,v) mapping an r,g,b color
    to a value v.
    it returns the color by linear interpolation between the values
    provided in tuples.
    ex: tuples = ( (0,0,0,0.0), (255,255,255,1.0) )
        value  = 0.5
        returns (127.5, 127.5, 127.5)
    """
    for i in range(len(tuples)):
        if value < tuples[i+1][3]:
            deltaV = (tuples[i+1][3] - tuples[i][3])
            deltaR = (tuples[i+1][0] - tuples[i][0])
            deltaG = (tuples[i+1][1] - tuples[i][1])
            deltaB = (tuples[i+1][2] - tuples[i][2])
            startV = tuples[i][3]
            startR = tuples[i][0]
            startG = tuples[i][1]
            startB = tuples[i][2]
            value = (value - startV) * (1/deltaV)
            return (deltaR * value + startR,
                    deltaG * value + startG,
                    deltaB * value + startB)

def handleInput(screen):
    #Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
            elif event.key == K_s:
                pygame.event.set_blocked(KEYDOWN|KEYUP)
                fname = raw_input("File name?  ")
                pygame.event.set_blocked(0)
                pygame.image.save(screen,fname)
    return False

def main():
    """
    this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns.
    """
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((picsize_x, picsize_y))
    pygame.display.set_caption('Pink Noise')

    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((64, 128, 255))

    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Prepare Game Objects
    going = True
    pixelsize = 16 # power of 2
    width, height = screen.get_size()

    # main loop
    while going:
        going = not(handleInput(screen))
        # start drawing loop
        while pixelsize > 0:
            print(pixelsize),"...",
            for x in range(0,width,pixelsize):
                xx = x/float(latticesizex)
                for y in range(0,height,pixelsize):
                    yy = y/float(latticesizey)
                    #nv = noiseValue
                    nv = noise.pinkNoise2(xx, yy, persistence, numOctaves)
                    # draw into background surface
                    color = np.array(getColor(nv, colorStops))
                    background.fill(color, ((x,y),(pixelsize,pixelsize)))
                    if handleInput(screen):
                        return
            #draw background into screen
            screen.blit(background, (0,0))
            pygame.display.flip()
            print "done"
            pixelsize //= 2

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
