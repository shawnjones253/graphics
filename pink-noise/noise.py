"""
Shawn Jones
CSCI 480
Assignment 1 - Pink Noise
noise.py
"""
from __future__ import division
from math import floor, sqrt
from random import shuffle
from settings import m, n, nexpr

#initialization
noiseTable = [(i/(n-1)) for i in range(n)]
hashTable = range(n)
shuffle(hashTable)

def smerp(pct, a, b):
    """
    Smooth interpolation between points a and b.
    Uses the portion of a cubic function between the first and second inflection points.

    Keyword arguments:
    a   -- the first point
    b   -- the second point
    pct -- pertentage distance away from point a to b
    """
    return a + (-2*pct*pct*pct + 3*pct*pct)*(b-a)

def latticeNoise2(x, y):
    """
    Retrieves the noise value (between 0 and 1) of the point at (x, y) in lattice space.
    No interpolation is done here.

    Keyword arguments:
    x -- the (integer) x-coordinate of the point in lattice space
    y -- the (integer) y-coordinate of the point in lattice space
    """
    return noiseTable[hashTable[(x + hashTable[y%m])%m]]

def smerpNoise2(x, y):
    """
    Calculates the noise value (between 0 and 1) of the point at (x, y) in lattice space.
    Uses latticeNoise2() to retrieve the value of the surrounding integer points in
    lattice space, then uses smerp() to interpolate the value at the actual point.

    Keyword arguments:
    x -- the (float) x-coordinate of the point in lattice space
    y -- the (float) y-coordinate of the point in lattice space
    """
    intx = int(floor(x))
    inty = int(floor(y))
    pctx = x - intx
    pcty = y - inty
    aa = latticeNoise2(intx, inty)
    ab = latticeNoise2(intx, inty+1)
    ba = latticeNoise2(intx+1, inty)
    bb = latticeNoise2(intx+1, inty+1)
    xa = smerp(pctx, aa, ba)
    xb = smerp(pctx, ab, bb)
    return smerp(pcty, xa, xb)

def pinkNoise2(x, y, persistence = float(1/2), numOctaves=5):
    """
    Uses smerpNoise2() to generate pink noise.

    Keyword arguments:
    x           -- the (float) x-coordinate of the point in lattice space
    y           -- the (float) y-coordinate of the point in lattice space
    persistence -- changes the amplitude of successive frequencies such that:
                   amplitude = persistence**i (i from 0 -> numOctaves-1)
    numOctaves  -- the number of octaves to add up
    """
    total = 0
    amplitudeSum = 0

    for i in range(numOctaves):
        frequency = 2**i
        amplitude = persistence**i
        total += (smerpNoise2(x*frequency, y*frequency) * amplitude)
        amplitudeSum += amplitude

    rval = (total / amplitudeSum)
    rval = nexpr(rval, x, y)
    if rval > 1.0:
        rval = 1.0
        print "pinkNoise2 clamped return value to 1.0"

    return rval
