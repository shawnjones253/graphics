"""
Shawn Jones
CSCI 480
Assignment 1 - Pink Noise
settings.py - "Water"
"""
from __future__ import division
#IMPORT THESE INTO MAIN.PY
#size in pixels of resulting image
picsize_x = 960
picsize_y = 720

#size in pixels of lattice points
latticesizex = 64
latticesizey = 16

#options for pinkNoise2
#see docstring for pinkNoise2 in noise.py for more information
persistence = float(1/2)
numOctaves = 5

#(r, g, b, noisevalue) - maps noise values to rgb colors
#see docstring for getColor in main.py for more information
colorStops = ( (82,102,101,0.0),
               (118,134,157,0.45),
               (128,143,165,0.80),
               (241,241,251,1.0) )

#IMPORT THESE IN TO NOISE.PY
#n is the number of elements in noiseTable and hashTable
n = 128
#m is the mod value used in the latticeNoise2 function
m = 64
#nexpr is the "noise expression" applied to pinkNoise values just before
#being returned
def nexpr(rval, x, y):
    return rval
