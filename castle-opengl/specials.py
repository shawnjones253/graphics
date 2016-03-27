"""
modified from
github.com/geofmatthews/csci480/tree/master/lectures/110opengl/gmtutorials/utilities/specials.py
added rectangleCrenellation
"""

import numpy as N

# Module to create vertex arrays for miscellaneous stuff

# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# x,y,z,0,    # tangent
# x,y,z,0,    # bitangent = normal x tangent
# u,v,        # texture
# and the elements array 

def rectangle(width, height):
    """Returns a rectangle in the x-y plane facing +z"""
    halfwidth = width*0.5
    halfheight = height*0.5
    v00 = (-halfwidth, -halfheight, 0, 1)
    v01 = (-halfwidth, halfheight, 0, 1)
    v10 = (halfwidth, -halfheight, 0, 1)
    v11 = (halfwidth, halfheight, 0, 1)
    n = (0,0,1,0)
    t = (1,0,0,0)
    b = (0,1,0,0)

    verts = N.array(
        v00 + n + t + b + (0,0) +
        v11 + n + t + b + (1,1) +
        v01 + n + t + b + (0,1) +
        v00 + n + t + b + (0,0) +
        v10 + n + t + b + (1,0) +
        v11 + n + t + b + (1,1) ,
        dtype=N.float32)

    indices = N.array((0,1,2,
                       3,4,5), dtype=N.uint32)

    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint32))

def rectangleCrenellation(rectWidth, numCren, crenHeight):
    """
    Returns a rectangle suitable for using as a crenellation
    on a wall of width rectWidth.
    Rectangle should be used to make numCren meshes.
    Also returns a list of x-positions for the center of each crenelation.
    Crenellations are crenHeight units tall.
    The width of the wall is divided up into numCren*2 points,
    where the distance between those points is the width of a crenellation.
    They need to be moved up.
    They need to be moved right so that their centers are at positions
    indicated in xcenters.
    """
    
    s = N.linspace(0.0, rectWidth, numCren*2)
    #create a list of indexes into s that mark starting edges of crenellations
    si = [x for x in range(numCren*2) if x%2 == 0]

    crenWidth = s[1]
    xcenters = [s[x]+(crenWidth/2) for x in si]

    verts,elements = rectangle(crenWidth, crenHeight)

    return verts, elements, xcenters
        
