"""
modified from
github.com/geofmatthews/csci480/tree/master/lectures/110opengl/gmtutorials/utilities/meshes.py
flatTexturedMesh modified to support fog
"""

# Classes to make constructing and drawing many objects simpler

# We will assume that all vertex arrays have 18 components of 32 bit floats
# whether or not they are all used:
# 4 floats position
# 4 floats normal
# 4 floats tangent (positive s texture coordinate direction "right")
# 4 floats bitangent (positive t texture coordinate direction "up")
# 2 floats texture coordinates

# Also assuming we're using 32 bit ints for elements

sizeOfFloat = 4
sizeOfShort = 2
sizeOfInt = 4
vertexSize = 18*sizeOfFloat

from OpenGL.GL import *
import numpy as N
from ctypes import c_void_p
from frames import Frame

def getBuffer(arr, type):
    buff = glGenBuffers(1)
    glBindBuffer(type, buff)
    glBufferData(type, arr, GL_STATIC_DRAW)
    glBindBuffer(type, 0)
    return buff

def getArrayBuffer(verts):
    return getBuffer(verts, GL_ARRAY_BUFFER)

def getElementBuffer(elements):
    return getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)

def vertexPointer(attrib, size, components, offset):
    if attrib >= 0:
        sizeOfFloat = 4
        glEnableVertexAttribArray(attrib)
        glVertexAttribPointer(attrib,
                              components,
                              GL_FLOAT,
                              GL_FALSE,
                              size,
                              c_void_p(offset*sizeOfFloat))
    
def bindTextureUnit(unit, texture, samplerUnif):
    glActiveTexture(GL_TEXTURE0 + unit)
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(samplerUnif, unit)

class coloredMesh(Frame):
    """Use phong.vert and phong.frag"""
    def __init__(self,
                 color,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader):
        Frame.__init__(self)
        self.color = color
        self.shader = shader
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorUnif = glGetUniformLocation(shader, "color")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniform4fv(self.colorUnif, 1, self.color)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)

class coloredTextureMesh(Frame):
    """Use textured.vert and textured.frag"""
    def __init__(self,
                 colortexture,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader):
        Frame.__init__(self)
        self.useNormals = 1
        self.texture = colortexture
        self.shader = shader
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.normalSamplerUnif = glGetUniformLocation(shader, "normalsampler")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.useNormalsUnif = glGetUniformLocation(shader, "usenormals")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1i(self.useNormalsUnif, self.useNormals)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib,vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib,vertexSize, 4, 12)
        vertexPointer(self.uvAttrib,vertexSize, 2, 16)
        # bind our color texture unit
        bindTextureUnit(0, self.texture, self.colorSamplerUnif)
        # draw
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)

class texturedMesh(Frame):
    """Use textured.vert and textured.frag"""
    def __init__(self,
                 colortexture,
                 normaltexture,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader):
        Frame.__init__(self)
        self.useNormals = 1
        self.colorTexture = colortexture
        self.normalTexture = normaltexture
        self.shader = shader
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.normalSamplerUnif = glGetUniformLocation(shader, "normalsampler")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.useNormalsUnif = glGetUniformLocation(shader, "usenormals")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1i(self.useNormalsUnif, self.useNormals)
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        # bind our texture units
        bindTextureUnit(0, self.colorTexture, self.colorSamplerUnif)
        bindTextureUnit(1, self.normalTexture, self.normalSamplerUnif)
        # draw
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)

class flatTexturedMesh(Frame):
    """Use flattextured.vert and flattextured.frag"""
    def __init__(self,
                 texture,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader,
                 scaleuv= N.array((1,1),dtype=N.float32),
                 useFog = False,
                 fogColor = N.array((1,1,1,1),dtype=N.float32),
                 fogStart = 1000.0,
                 fogEnd = 1000.0,
                 fade = 1.0):
        Frame.__init__(self)
        self.texture = texture
        self.shader = shader
        self.scaleuv = scaleuv
        self.useFog = useFog
        self.fogColor = fogColor
        self.fogStart = fogStart
        self.fogEnd = fogEnd
        self.fade = fade
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.scaleuvUnif = glGetUniformLocation(shader, "scaleuv")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.fadeUnif = glGetUniformLocation(shader, "fade")
        self.useFogUnif = glGetUniformLocation(shader, "useFog")
        self.fogColorUnif = glGetUniformLocation(shader, "fogColor")
        self.fogStartUnif = glGetUniformLocation(shader, "fogStart")
        self.fogEndUnif = glGetUniformLocation(shader, "fogEnd")
        

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniform1f(self.fadeUnif, self.fade)
        glUniform1f(self.fogStartUnif, self.fogStart),
        glUniform1f(self.fogEndUnif, self.fogEnd),
        glUniform1i(self.useFogUnif, self.useFog),
        glUniform2fv(self.scaleuvUnif, 1, self.scaleuv)
        glUniform4fv(self.fogColorUnif, 1, self.fogColor)
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        # bind our color texture unit
        bindTextureUnit(0, self.texture, self.colorSamplerUnif)
        # draw
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)

class proceduralMesh(Frame):
    """Use bumpmap.vert and knot.frag, e.g."""
    def __init__(self,
                 color,
                 color2,
                 scaleCoords,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader):
        Frame.__init__(self)
        self.color = color
        self.color2 = color2
        self.scaleCoords = scaleCoords
        self.shader = shader
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.scaleCoordsUnif = glGetUniformLocation(shader, "scalecoords")
        self.colorUnif = glGetUniformLocation(shader, "color")
        self.color2Unif = glGetUniformLocation(shader, "color2")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniform4fv(self.colorUnif, 1, self.color)
        glUniform4fv(self.color2Unif, 1, self.color2)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1f(self.scaleCoordsUnif, self.scaleCoords)
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib, vertexSize, 4, 12)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)
        

class reflectorMesh(Frame):
    """Use reflector.vert and reflector.frag"""
    def __init__(self,
                 posxTexture,
                 negxTexture,
                 posyTexture,
                 negyTexture,
                 poszTexture,
                 negzTexture,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader):
        Frame.__init__(self)
        self.posxTexture = posxTexture
        self.negxTexture = negxTexture
        self.posyTexture = posyTexture
        self.negyTexture = negyTexture
        self.poszTexture = poszTexture
        self.negzTexture = negzTexture
        self.shader = shader
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")

        # find the uniform locations:
        self.posxUnif = glGetUniformLocation(shader, "posxsampler")
        self.negxUnif = glGetUniformLocation(shader, "negxsampler")
        self.posyUnif = glGetUniformLocation(shader, "posysampler")
        self.negyUnif = glGetUniformLocation(shader, "negysampler")
        self.poszUnif = glGetUniformLocation(shader, "poszsampler")
        self.negzUnif = glGetUniformLocation(shader, "negzsampler")

        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.colorUnif = glGetUniformLocation(shader, "color")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib, vertexSize, 4, 12)
        # bind all those texture units
        bindTextureUnit(0, self.posxTexture, self.posxUnif)
        bindTextureUnit(1, self.negxTexture, self.negxUnif)
        bindTextureUnit(2, self.posyTexture, self.posyUnif)
        bindTextureUnit(3, self.negyTexture, self.negyUnif)
        bindTextureUnit(4, self.poszTexture, self.poszUnif)
        bindTextureUnit(5, self.negzTexture, self.negzUnif)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)
        



class motionblurMesh(Frame):
    """Use flattextured.vert and motionblur.frag"""
    def __init__(self,
                 textures,
                 arrayBuffer,
                 elementBuffer,
                 numElements,
                 shader,
                 scaleuv= N.array((1,1),dtype=N.float32),
                 fade = 1.0):
        Frame.__init__(self)
        self.textures = textures
        self.shader = shader
        self.scaleuv = scaleuv
        self.fade = fade
        # send data to opengl context:
        self.elementSize = numElements*sizeOfInt
        self.arrayBuffer = arrayBuffer
        self.elementBuffer = elementBuffer
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.s0Unif = glGetUniformLocation(shader, "s0")
        self.s1Unif = glGetUniformLocation(shader, "s1")
        self.s2Unif = glGetUniformLocation(shader, "s2")
        self.s3Unif = glGetUniformLocation(shader, "s3")
        self.s4Unif = glGetUniformLocation(shader, "s4")
        self.s5Unif = glGetUniformLocation(shader, "s5")
        self.s6Unif = glGetUniformLocation(shader, "s6")
        self.s7Unif = glGetUniformLocation(shader, "s7")
        self.scaleuvUnif = glGetUniformLocation(shader, "scaleuv")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniform2fv(self.scaleuvUnif, 1, self.scaleuv)
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        # bind our color texture units
        bindTextureUnit(0, self.textures[0], self.s0Unif)
        bindTextureUnit(1, self.textures[1], self.s1Unif)
        bindTextureUnit(2, self.textures[2], self.s2Unif)
        bindTextureUnit(3, self.textures[3], self.s3Unif)
        bindTextureUnit(4, self.textures[4], self.s4Unif)
        bindTextureUnit(5, self.textures[5], self.s5Unif)
        bindTextureUnit(6, self.textures[6], self.s6Unif)
        bindTextureUnit(7, self.textures[7], self.s7Unif)
        # draw
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_INT, c_void_p(0))
        glUseProgram(0)

