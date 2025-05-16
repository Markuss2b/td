import ctypes
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *
from PIL import Image
from numpy import array, float32

"""
OpenGL documentation
https://registry.khronos.org/OpenGL-Refpages/gl4/

Stackoverflow post on PyOpenGL:
https://stackoverflow.com/questions/72684375/pyopengl-how-to-draw-2d-image

Learnopengl:
https://learnopengl.com/book/book_pdf.pdf

PyOpenGL tutorial:
https://youtu.be/mOTE_62i5ag?si=WRuQgIu8NVnQR8kL
https://youtu.be/ZK1WyCMK12E?si=-BOu338g5Xk7Ni1A
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


def draw_quad_2(left, top, width, height, texture_id, shader, vbo, alpha):

    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)
    verts = (
        xy_to_1(left + width, top + height),
        xy_to_1(left + width, top),
        xy_to_1(left, top),
        xy_to_1(left, top + height)
    )

    vertices = []

    for i in surf:
        vertices.append(verts[i][0])
        vertices.append(verts[i][1])
        vertices.append(texts[i][0])
        vertices.append(texts[i][1])

    vertices = array(vertices, dtype=float32)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
   
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glUniform1i(glGetUniformLocation(shader, "textu"), 0)
    glUniform1f(glGetUniformLocation(shader, "alpha"), alpha)
    
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)


def draw_quads_2(texture_ids_with_quads, shader, vbo, alpha):
    
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)
    glUniform1i(glGetUniformLocation(shader, "textu"), 0)
    glUniform1f(glGetUniformLocation(shader, "alpha"), alpha)

    for dict_type in texture_ids_with_quads:

        for texture_id in texture_ids_with_quads.get(dict_type):
        
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            for rectangle in texture_ids_with_quads.get(dict_type).get(texture_id):
                left = rectangle[0]
                top = rectangle[1]
                width = rectangle[2]
                height = rectangle[3]

                verts = (
                    xy_to_1(left + width, top + height),
                    xy_to_1(left + width, top),
                    xy_to_1(left, top),
                    xy_to_1(left, top + height)
                )

                vertices = []

                for i in surf:
                    vertices.append(verts[i][0])
                    vertices.append(verts[i][1])
                    vertices.append(texts[i][0])
                    vertices.append(texts[i][1])

                vertices = array(vertices, dtype=float32)

                glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)



def destroy(vao, vbo):
    glDeleteVertexArrays(1, (vao,))
    glDeleteBuffers(1, (vbo,))


def create_shader(vertex_path, fragment_path):

    with open(vertex_path, 'r') as f:
        vertex_src = f.readlines()

    with open(fragment_path, 'r') as f:
        fragment_src = f.readlines()

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    return shader

# Clear VRAM
def unload_texture(texture_id):
    glDeleteTextures([texture_id])


def xy_to_1(x, y):
    screen_width = 1600
    screen_height = 900
    return (2.0 * x / screen_width - 1.0, 1.0 - 2.0 * y / screen_height)
        