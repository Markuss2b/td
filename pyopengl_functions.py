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

    # Transparancy
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.size[0], text.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    text.close()
    return texture_id

# Can be used like in pygame Rect(left, top, width, height)
# FIXME: Dictionary with all textureid
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


#TODO:
def draw_quads(texture_ids_with_quads):

    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    for dict_type in texture_ids_with_quads:

        for texture_id in texture_ids_with_quads.get(dict_type):
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glBegin(GL_QUADS)
            for rectangle in texture_ids_with_quads.get(dict_type).get(texture_id):
                left = rectangle[0]
                top = rectangle[1]
                width = rectangle[2]
                height = rectangle[3]

                verts = (
                    (left + width, top + height),
                    (left + width, top),
                    (left, top),
                    (left, top + height)
                )

                for i in surf:
                    glTexCoord2f(texts[i][0], texts[i][1])
                    glVertex2f(verts[i][0], verts[i][1])
            glEnd()
                
    glDisable(GL_TEXTURE_2D)


# Clear VRAM
def unload_texture(texture_id):
    glDeleteTextures([texture_id])
        