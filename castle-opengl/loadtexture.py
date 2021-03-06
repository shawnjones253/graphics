"""
imported from
github.com/geofmatthews/csci480/blob/master/lectures/110opengl/gmtutorials/utilities/loadtexture.py
"""

import pygame
import os
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *

# This must be done after the opengl context is active

def loadTexture(filename,
                minFilter = GL_LINEAR,
                magFilter = GL_NEAREST,
                genMipmap = True,
                useAniso = True,
                wrapMode = GL_REPEAT):
    surf = pygame.image.load(os.path.join("textures", filename))
    data = pygame.image.tostring(surf, "RGBA", 1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    # wrapmode            
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrapMode)
    # how to scale things
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
    # send the data to the hardware
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 surf.get_width(),
                 surf.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    if genMipmap:
        glGenerateMipmap(GL_TEXTURE_2D)
    if useAniso:
        aniso = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        glTexParameterf(GL_TEXTURE_2D,
                        GL_TEXTURE_MAX_ANISOTROPY_EXT,
                        aniso)        

    glBindTexture(GL_TEXTURE_2D, 0)
    return textureID



