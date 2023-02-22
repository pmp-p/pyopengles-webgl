from pyopengles import *
import os.path, pyinotify

# fullscreen, alpha fixed for all pixels, PREMULT flag on
e = EGL(alpha_flags=1+1<<16, alpha_opacity=255)
#e=EGL(pref_width = 640, pref_height=480)

surface_tris = eglfloats( (  - 1.0, - 1.0, 1.0, 
                             - 1.0, 1.0, 1.0, 
                               1.0, 1.0, 1.0, 
                             - 1.0, - 1.0, 1.0, 
                               1.0, 1.0, 1.0, 
                             1.0, - 1.0, 1.0 ) ) # 2 tris

def draw(programObject,time_ms, m, r, Vbo):
  opengles.glClear ( GL_COLOR_BUFFER_BIT )

  location = opengles.glGetUniformLocation(programObject, "time")
  opengles.glUniform1f(location, eglfloat(time_ms))
  try:
    e._check_glerror()
  except GLError as error:
    print("Error setting time uniform var")
    print(error)

  location = opengles.glGetUniformLocation(programObject, "mouse")
  opengles.glUniform2f(location, eglfloat(float(m.x) / r[0].value), eglfloat(float(m.y) / r[1].value))
  try:
    e._check_glerror()
  except GLError as error:
    print("Error setting mouse uniform var")
    print(error)

  location = opengles.glGetUniformLocation(programObject, "resolution")
  opengles.glUniform2f(location, r[0], r[1])
  try:
    e._check_glerror()
  except GLError as error:
    print("Error setting resolution uniform var")
    print(error)

  opengles.glBindBuffer(GL_ARRAY_BUFFER, Vbo)

  opengles.glEnableVertexAttribArray(0);
  
  opengles.glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*4, 0)
  
  # Draws a non-indexed triangle array
  opengles.glDrawArrays ( GL_TRIANGLE_STRIP, 0, 6 )  # 2 tris
  opengles.glBindBuffer(GL_ARRAY_BUFFER, 0)
  e._check_glerror()

  openegl.eglSwapBuffers(e.display, e.surface)
  time.sleep(0.02)
  

def run_shader(frag_shader):
  class FakeM():
    def __init__(self, x,y):
      self.x = x
      self.y = y
      self.finished = False
  m = FakeM(400,300)

  _v_src = """
attribute vec3 position;
attribute vec2 surfacePosAttrib;
varying vec2 surfacePosition;
void main() {
  surfacePosition = surfacePosAttrib;
  gl_Position = vec4( position, 1.0 );
}
"""

  vertexShader = e.load_shader(_v_src, GL_VERTEX_SHADER )
  fragmentShader = e.load_shader(frag_shader, GL_FRAGMENT_SHADER)
  # Create the program object
  programObject = opengles.glCreateProgram ( )

  opengles.glAttachShader ( programObject, vertexShader )
  opengles.glAttachShader ( programObject, fragmentShader )
  e._check_glerror()

  opengles.glBindAttribLocation ( programObject, 0, "position" )
  e._check_glerror()

  # Link the program
  opengles.glLinkProgram ( programObject )
  e._check_glerror()

  # Check the link status
  if not (e._check_Linked_status(programObject)):
    print("Couldn't link the shaders to the program object. Check the bindings and shader sourcefiles.")
    raise Exception
 
  opengles.glClearColor ( eglfloat(0.3), eglfloat(0.3), eglfloat(0.5), eglfloat(1.0) )
  e._check_glerror()

  opengles.glUseProgram( programObject )
  e._check_glerror()

  # Make a VBO buffer obj
  Vbo = eglint()

  opengles.glGenBuffers(1, ctypes.byref(Vbo))
  e._check_glerror()

  opengles.glBindBuffer(GL_ARRAY_BUFFER, Vbo)
  e._check_glerror()

  # Set the buffer's data
  opengles.glBufferData(GL_ARRAY_BUFFER, 4 * 6 * 3, surface_tris, GL_STATIC_DRAW)
  e._check_glerror()

  # Unbind the VBO
  opengles.glBindBuffer(GL_ARRAY_BUFFER, 0)
  e._check_glerror()

  # render loop
  start = time.time()
  r = (eglfloat(e.width.value), eglfloat(e.height.value))
  try:
    while(1):
      draw(programObject, (time.time() - start), m, r, Vbo)
      time.sleep(0.02)
  finally:
    del programObject, vertexShader, fragmentShader
    
if __name__ == "__main__":
  import sys
  if len(sys.argv) == 2:
    glsl_file = open(sys.argv[1], "r")
    frag = glsl_file.read()
    glsl_file.close()
    run_shader(frag)


