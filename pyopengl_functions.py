from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array

"""
OpenGL documentation
https://registry.khronos.org/OpenGL-Refpages/gl4/

Stackoverflow post on PyOpenGL:
https://stackoverflow.com/questions/72684375/pyopengl-how-to-draw-2d-image
"""

# TODO: Delete all textures after stops running
def load_texture(texture):

    text = Image.open(texture).transpose(Image.FLIP_TOP_BOTTOM)
    texture_data = array(list(text.getdata()))
    texture_id = glGenTextures(1)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.size[0], text.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    text.close()
    return texture_id

# Can be used like in pygame Rect(left, top, width, height)
def draw_quad(left, top, width, height, texture_id):
    verts = (
        (left + width, top + height),
        (left + width, top),
        (left, top),
        (left, top + height)
    )
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(verts[i][0], verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

# Clear VRAM
def unload_texture(texture_id):
    glDeleteTextures([texture_id])
        