#!pygbag

import asyncio
import ctypes
import pyopengles as gl
import struct
import pygame

pygame.init()

screen = pygame.display.set_mode((1024, 1024), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
display = pygame.Surface((1024, 1024))
display.set_colorkey((0.3, 0.3, 0.3))


gles = gl.opengles
eglfloat = gl.eglfloat
eglfloats = gl.eglfloats

ctx = gl.EGL()
if 1:
    vertex_shader = ctypes.c_char_p(b"""
        attribute highp vec4 vertex_position;
        void main()
        {
            gl_Position = vertex_position;
        }
    """)

    fragment_shader = ctypes.c_char_p(b"""
        precision mediump float;
        void main()
        {
            gl_FragColor = vec4 ( 1.0, 0.0, 0.0, 1.0 );
        }
    """)


    binding = ((0, 'vPosition'),)


else:
    vertex_shader = ctypes.c_char_p(b"""#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}    """)

    fragment_shader = ctypes.c_char_p(b"""
precision mediump float;
uniform sampler2D Texture;
in vec2 v_text;

out vec3 f_color;
void main() {
  f_color = texture(Texture, v_text).rgb;
}
    """)



    texture_coordinates = [
        0, 1,  1, 1,
        0, 0,  1, 0,
    ]

    world_coordinates = [
        -1, -1,  1, -1,
        -1,  1,  1,  1,
    ]

    render_indices = [
        0, 1, 2,
        1, 2, 3,
    ]


    vbo = ctx.buffer(struct.pack('8f', *world_coordinates))
    uvmap = ctx.buffer(struct.pack('8f', *texture_coordinates))
    ibo= ctx.buffer(struct.pack('6I', *render_indices))



async def main():

    program = ctx.get_program(vertex_shader, fragment_shader, binding)
    await asyncio.sleep(0)
    print(program)

    for x in range(0,5):
        gles.glClearColor(eglfloat(0.3), eglfloat(0.3), eglfloat(0.3),eglfloat(1.0))

        triangle_vertices = eglfloats(( -0.866, -0.5, 1.0,
                                         0.0,  1.0, 1.0,
                                         0.866, -0.5, 1.0 ))

        # Clear the color buffer
        gles.glClear ( gl.GL_COLOR_BUFFER_BIT )

        # Set the Viewport: (NB openegl, not opengles)
        gl.openegl.glViewport(0,0,ctx.width, ctx.height)

        pygame.draw.rect(display, (255, 0, 0), (20, 20, 20, 20)) #Draw a red rectangle to the display at (20, 20)

        # Use the program object
        gles.glUseProgram ( program )

        # Load the vertex data
        gles.glVertexAttribPointer ( 0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, triangle_vertices )
        gles.glEnableVertexAttribArray ( 0 )

        gles.glDrawArrays ( gl.GL_TRIANGLES, 0, 3 )
        gl.openegl.eglSwapBuffers(ctx.display, ctx.surface)
        print("gles")

        await asyncio.sleep(5)


asyncio.run( main() )

