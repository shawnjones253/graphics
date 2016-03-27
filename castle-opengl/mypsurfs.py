"""
Shawn Jones
CSCI 480
Assignment 3 - Castle in OpenGL
"""

import numpy as N
from noise import *

# Module to create vertex arrays for parametric surfaces.
# point is a function(s,t) -> (x,y,z,1)
# normal is a function(s,t) -> (x,y,z,0)
# tangent is a function(s,t) -> (x,y,z,0)
# binormal is computed assuming normal and tangent are orthonormal
# texture is a function(s,t) -> (u,v)
# s and t use N.linspace to generate num points min <= x <= max


def reflectedSurface(verts, elements):
    """
    reflects the pSurface about the y=0 plane
    by negating all position.y values in the vertex array
    and reversing the triangle windings in the elements array
    """
    for i in xrange(1, verts.size, 18):
        verts[i] = -verts[i]

    for i in xrange(1, elements.size, 3):
        elements[i], elements[i+1] = elements[i+1], elements[i]

    return verts, elements


# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# x,y,z,0,    # tangent
# x,y,z,0,    # bitangent = normal x tangent
# u,v,        # texture
# and the elements array with each quad forming two
# triangles with correct winding
def pSurface(point, normal, tangent, 
             texture, smin, smax, snum, tmin, tmax, tnum,
             indexmin=0):
    """from gmtutorials/utilities/psurfaces.py"""
    snum += 1
    tnum += 1
    verts = []
    for s in N.linspace(smin, smax, snum):
        for t in N.linspace(tmin, tmax, tnum):
            p00 = point(s,t)            
            n00 = normal(s,t)
            t00 = tangent(s,t)
            b00 = list(N.cross(N.array(n00[0:3],dtype=N.float32), 
                               N.array(t00[0:3],dtype=N.float32))) + [0]
            uv00 = texture(s,t)           
            verts.extend(p00+n00+t00+b00+uv00)
    jump = tnum
    indices = []
    for row in range(snum-1):
        for col in range(tnum-1):
            index = indexmin + row*jump + col
            i00 = index
            i01 = index+1
            i10 = index+jump
            i11 = index+jump+1
            indices.extend([i00,i10,i01,i10,i11,i01])
    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint32))

def cylinderPoint(radius, s, t):
    cs = N.cos(s)
    ss = N.sin(s)
    # find point on circle:
    cp = N.array((radius*cs, t, -(radius*ss)), dtype=N.float32)
    # return homogeneous point
    return list(cp) + [1.0] 

def cylinderNormal(s, t):
    cs = N.cos(s)
    ss = N.sin(s)
    # find curve normal
    n = N.array((cs, 0.0, -ss), dtype=N.float32)
    n /= N.linalg.norm(n)
    return list(n) + [0.0]

def cylinderTangent(s, t):
    v = [0.0, 1.0, 0.0, 0.0]
    return v

def cylinderTexture(s, t):
    return [0.5*s/N.pi,t]

def cylinder(radius, height, narcs):
    """
    Returns a cylinder pSurface of specified radius and height,
    standing on XZ plane and centered at +y-axis.
    The cylinder is made up of narcs number of squares.
    """
    twopi = 2.0*N.pi
    verts,elements = pSurface(lambda s,t:cylinderPoint(radius, s, t),
                              cylinderNormal,
                              cylinderTangent,
                              cylinderTexture,
                              0.0, twopi, narcs,
                              0.0, height, 1)

    return verts, elements

def cylinderTopPoint(s, t):
    cs = N.cos(s)
    ss = N.sin(s)
    # find point on circle:
    cp = N.array((t*cs, 0, -(t*ss)), dtype=N.float32)
    # return homogeneous point
    return list(cp) + [1.0]

def cylinderTopNormal(s, t):
    n = N.array((0, 1, 0), dtype=N.float32)
    return list(n) + [0.0]

def cylinderTopTangent(s, t):
    v = [1.0, 0.0, 0.0, 0.0]
    return v

def cylinderTop(radius, thickness, narcs):
    """
    Returns a top for a cylinder with inner radius (radius-thickness)
    and outer radius (radius), made up of n arcs.
    """
    twopi = 2.0*N.pi
    verts,elements = pSurface(lambda s,t:cylinderTopPoint(s, t),
                              cylinderTopNormal,
                              cylinderTopTangent,
                              cylinderTexture,
                              0.0, twopi, narcs,
                              radius-thickness, radius, 1)
    return verts, elements
                              

def cylinderCrenellations(radius, height, narcs, crenWidth, crenHeight):
    """
    Returns a list of pSurfaces, each representing crenellations
    for a cylinder of specified radius, height, and narcs.
    Crenellations are crenWidth arcs wide and crenHeight units tall.
    They need to be moved up.
    """
    vertsList = []
    elementsList = []
    s = N.linspace(0.0, 2.0*N.pi, narcs+1)
    #create a list of indexes into s that mark edges of crenellations
    si = [x for x in range(narcs+1) if x%crenWidth == 0]
    for arc in si:
        #every other index but not the last
        if (si.index(arc)%2 == 0) and (arc != si[-1]):
            av,ae = pSurface(lambda s,t:cylinderPoint(radius, s, t),
                             cylinderNormal,
                             cylinderTangent,
                             cylinderTexture,
                             s[arc], s[arc+crenWidth], crenWidth,
                             0.0, crenHeight, 1)
            vertsList.append(av)
            elementsList.append(ae)

    return vertsList, elementsList


def islandAndMoatPoint(islandHeight,
                       surroundingLandHeight,
                       moatDepth,
                       islandTopRadius,
                       islandTopRadiusSq,
                       moatInnerRadius,
                       moatInnerRadiusSq,
                       moatOuterRadius,
                       moatOuterRadiusSq,
                       outerShoreRadius,
                       outerShoreRadiusSq,
                       noiseY,
                       noiseVariance,
                       noiseScale,
                       s, t):

    if (abs(s) > outerShoreRadius) or (abs(t) > outerShoreRadius):
        p = N.array((s, surroundingLandHeight, t), dtype=N.float32)

    else:
        rSq = N.square(s) + N.square(t)

        if rSq <= islandTopRadiusSq:
            p = N.array((s, islandHeight, t), dtype=N.float32)
        elif rSq <= moatInnerRadiusSq:
            pct = (N.sqrt(rSq) - islandTopRadius)/(moatInnerRadius - islandTopRadius)
            p = N.array((s, smerp(pct, islandHeight-moatDepth, 0)+moatDepth, t), dtype=N.float32)
        elif rSq <= moatOuterRadiusSq:
            p = N.array((s, moatDepth, t), dtype=N.float32)
        elif rSq <= outerShoreRadiusSq:
            pct = (N.sqrt(rSq) - moatOuterRadius)/(outerShoreRadius - moatOuterRadius)
            p = N.array((s, smerp(pct, 0, surroundingLandHeight-moatDepth)+moatDepth, t), dtype=N.float32)
        else:
            p = N.array((s, surroundingLandHeight, t), dtype=N.float32)

    if noiseY:
        p[1] += noiseVariance * pinkNoise2(s*noiseScale, t*noiseScale)
    
    return list(p) + [1.0]

def islandAndMoatNormal(s, t):
    #not used
    return [0.0, 1.0, 0.0, 0.0]

def islandAndMoatTangent(s, t):
    #not used
    return [1.0, 0.0, 0.0, 0.0]

def islandAndMoatTexture(s, t):
    return [s, t]

def islandAndMoat(islandHeight,
                  surroundingLandHeight,
                  moatDepth,
                  islandTopRadius,
                  moatInnerRadius,
                  moatOuterRadius,
                  outerShoreRadius,
                  terrainXZMax, 
                  nsamples,
                  noiseY = False,
                  noiseVariance = 1.0,
                  noiseScale = 0.2):
    """
    returns a surface such that:
    -island in middle of height islandHeight and radius islandTopRadius
    -island drops to height of moatDepth at moatInnerRadius and stays until moatOuterRadius
    -rises back to height of surroundingLandHeight at outerShoreRadius
    -there are nsamples*nsamples points
    -if noiseY = true, all points will have between 0 and noiseVariance added to their y-value
    -noiseScale changes s,t into lattice space
    """

    r0 = N.square(islandTopRadius)
    r1 = N.square(moatInnerRadius)
    r2 = N.square(moatOuterRadius)
    r3 = N.square(outerShoreRadius)

    verts,elements =  pSurface(lambda s,t:islandAndMoatPoint(islandHeight,
                                                  surroundingLandHeight,
                                                  moatDepth,
                                                  islandTopRadius,
                                                  r0,
                                                  moatInnerRadius,
                                                  r1,
                                                  moatOuterRadius,
                                                  r2,
                                                  outerShoreRadius,
                                                  r3,
                                                  noiseY,
                                                  noiseVariance,
                                                  noiseScale,
                                                  s, t),
                    islandAndMoatNormal,
                    islandAndMoatTangent,
                    lambda s,t:islandAndMoatTexture(float(s/terrainXZMax),
                                                    float(t/terrainXZMax)),
                    -terrainXZMax, terrainXZMax, nsamples,
                    terrainXZMax, -terrainXZMax, nsamples)

    return (verts, elements)
