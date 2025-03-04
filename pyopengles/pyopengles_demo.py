
from .pyopengles import *

from . import pymouse

class demo():

    def showlog(self,shader):
        """Prints the compile log for a shader"""
        N=1024
        log=(ctypes.c_char*N)()
        loglen=ctypes.c_int()
        opengles.glGetShaderInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
        print(log.value)

    def showprogramlog(self,shader):
        """Prints the compile log for a shader"""
        N=1024
        log=(ctypes.c_char*N)()
        loglen=ctypes.c_int()
        opengles.glGetProgramInfoLog(shader,N,ctypes.byref(loglen),ctypes.byref(log))
        print(log.value)
            
    def __init__(self):
        self.vertex_data = eglfloats((-1.0,-1.0,1.0,1.0,
                         1.0,-1.0,1.0,1.0,
                         1.0,1.0,1.0,1.0,
                         -1.0,1.0,1.0,1.0))
        self.vshader_source = ctypes.c_char_p(
              "attribute vec4 vertex;"
              "varying vec2 tcoord;"
              "void main(void) {"
              "  vec4 pos = vertex;"
              "  pos.xy*=0.9;"
              "  gl_Position = pos;"
              "  tcoord = vertex.xy*0.5+0.5;"
              "}")
      
        self.fshader_source = ctypes.c_char_p(
              "uniform vec4 color;"
              "void main(void) {"
              "   gl_FragColor = color;"
              "}")

        # Mandelbrot
        mandelbrot_fshader_source = ctypes.c_char_p("""
	uniform vec4 color;
	uniform vec2 scale;
	varying vec2 tcoord;
	void main(void) {
		float intensity;
		vec4 color2;
		float cr=(gl_FragCoord.x-810.0)*scale.x; //0.0005;
		float ci=(gl_FragCoord.y-540.0)*scale.y; //0.0005;

		float ar=cr;
		float ai=ci;

		float tr,ti;
		float col=0.0;
                float p=0.0;
                int i=0;
                
                for(int i2=1;i2<16;i2++)
                {
                        tr=ar*ar-ai*ai+cr;
                        ti=2.0*ar*ai+ci;
                        p=tr*tr+ti*ti;
                        ar=tr;
                        ai=ti;
                        if (p>16.0)
                        {
                          i=i2;
                          break;
                        }
                        
                }
	        color2 = vec4(float(i)*0.0625,0,0,1);
		gl_FragColor = color2;
	}""")

        # Julia
        julia_fshader_source = ctypes.c_char_p("""
	uniform vec4 color;
	uniform vec2 scale;
	uniform vec2 offset;
	varying vec2 tcoord;
	uniform sampler2D tex;
	void main(void) {
		float intensity;
		vec4 color2;
		float ar=(gl_FragCoord.x-810.0)*scale.x;
		float ai=(gl_FragCoord.y-540.0)*scale.y;

		float cr=(offset.x-810.0)*scale.x;
		float ci=(offset.y-540.0)*scale.y;

		float tr,ti;
		float col=0.0;
                float p=0.0;
                int i=0;
                int j=0;
                vec2 t2;

                t2.x=tcoord.x+(offset.x-810.0)*(1.0/1920.0);
                t2.y=tcoord.y+(offset.y-540.0)*(1.0/1080.0);
                
                for(int i2=1;i2<16;i2++)
                {
                        tr=ar*ar-ai*ai+cr;
                        ti=2.0*ar*ai+ci;
                        p=tr*tr+ti*ti;
                        ar=tr;
                        ai=ti;
                        if (p>16.0)
                        {
                          i=i2;
                          break;
                        }
                }

                col=float(j)*(0.005);
	        color2 = vec4(col,float(i)*0.0625,0,1);
	        color2 = color2+texture2D(tex,t2);
		gl_FragColor = color2;
	}""")

        vshader = opengles.glCreateShader(GL_VERTEX_SHADER);
        opengles.glShaderSource(vshader, 1, ctypes.byref(self.vshader_source), 0)
        opengles.glCompileShader(vshader);

        if verbose:
            self.showlog(vshader)
            
        fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER);
        opengles.glShaderSource(fshader, 1, ctypes.byref(julia_fshader_source), 0);
        opengles.glCompileShader(fshader);

        if verbose:
            self.showlog(fshader)

        mshader = opengles.glCreateShader(GL_FRAGMENT_SHADER);
        opengles.glShaderSource(mshader, 1, ctypes.byref(mandelbrot_fshader_source), 0);
        opengles.glCompileShader(mshader);

        if verbose:
            self.showlog(mshader)

        program = opengles.glCreateProgram();
        opengles.glAttachShader(program, vshader);
        opengles.glAttachShader(program, fshader);
        opengles.glLinkProgram(program);

        if verbose:
            self.showprogramlog(program)
            
        self.program = program
        self.unif_color = opengles.glGetUniformLocation(program, "color");
        self.attr_vertex = opengles.glGetAttribLocation(program, "vertex");
        self.unif_scale = opengles.glGetUniformLocation(program, "scale");
        self.unif_offset = opengles.glGetUniformLocation(program, "offset");
        self.unif_tex = opengles.glGetUniformLocation(program, "tex");
        

        program2 = opengles.glCreateProgram();
        opengles.glAttachShader(program2, vshader);
        opengles.glAttachShader(program2, mshader);
        opengles.glLinkProgram(program2);

        if verbose:
            self.showprogramlog(program2)
            
        self.program2 = program2
        self.attr_vertex2 = opengles.glGetAttribLocation(program2, "vertex");
        self.unif_scale2 = opengles.glGetUniformLocation(program2, "scale");
        self.unif_offset2 = opengles.glGetUniformLocation(program2, "offset");
   
        opengles.glClearColor ( eglfloat(0.0), eglfloat(1.0), eglfloat(1.0), eglfloat(1.0) );
        
        self.buf=eglint()
        opengles.glGenBuffers(1,ctypes.byref(self.buf))

        self.check()

        # Prepare a texture image
        self.tex=eglint()
        self.check()
        opengles.glGenTextures(1,ctypes.byref(self.tex))
        self.check()
        opengles.glBindTexture(GL_TEXTURE_2D,self.tex)
        self.check()
        # opengles.glActiveTexture(0)
        #test_tex=(eglshort*(1920*1080))(*([3567]*20000))
        #test_tex_p = ctypes.pointer(test_tex)
        #self.store=[test_tex,test_tex_p]
        opengles.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,1920,1080,0,GL_RGB,GL_UNSIGNED_SHORT_5_6_5,0)
        #opengles.glTexImage2D(GL_TEXTURE_2D,0,1920,1080,0,GL_RGB,GL_UNSIGNED_BYTE,0)
        self.check()
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, eglfloat(GL_NEAREST))
        opengles.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, eglfloat(GL_NEAREST))
        self.check()
        # Prepare a framebuffer for rendering
        self.tex_fb=eglint()
        opengles.glGenFramebuffers(1,ctypes.byref(self.tex_fb))
        self.check()
        opengles.glBindFramebuffer(GL_FRAMEBUFFER,self.tex_fb)
        self.check()
        opengles.glFramebufferTexture2D(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0,GL_TEXTURE_2D,self.tex,0)
        self.check()
        opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
        self.check()
        # Prepare viewport
        opengles.glViewport ( 0, 0, egl.width, egl.height );
        self.check()
        
        # Upload vertex data to a buffer
        opengles.glBindBuffer(GL_ARRAY_BUFFER, self.buf);
        opengles.glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(self.vertex_data),
                             ctypes.byref(self.vertex_data), GL_STATIC_DRAW);
        opengles.glVertexAttribPointer(self.attr_vertex, 4, GL_FLOAT, 0, 16, 0);
        opengles.glEnableVertexAttribArray(self.attr_vertex);
        self.check()

    def draw_mandelbrot_to_texture(self,scale):
        # Draw the mandelbrot to a texture
        opengles.glBindFramebuffer(GL_FRAMEBUFFER,self.tex_fb)
        self.check()
        opengles.glBindBuffer(GL_ARRAY_BUFFER, self.buf);
        
        opengles.glUseProgram ( self.program2 );
        self.check()

        opengles.glUniform2f(self.unif_scale2, eglfloat(scale), eglfloat(scale));
        self.check()
        #opengles.glUniform2f(self.unif_offset2, eglfloat(offset[0]), eglfloat(offset[1]));
        #self.check()
        opengles.glDrawArrays ( GL_TRIANGLE_FAN, 0, 4 );
        self.check()
               
        opengles.glFlush()
        opengles.glFinish()
        self.check()
        
    def draw_triangles(self,scale=0.0005,offset=(0.2,0.3)):

        # Now render to the main frame buffer
        opengles.glBindFramebuffer(GL_FRAMEBUFFER,0)
        # Clear the background (not really necessary I suppose)
        opengles.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
        self.check()
        
        opengles.glBindBuffer(GL_ARRAY_BUFFER, self.buf);
        self.check()
        opengles.glUseProgram ( self.program );
        self.check()
        opengles.glBindTexture(GL_TEXTURE_2D,self.tex)
        self.check()
        opengles.glUniform4f(self.unif_color, eglfloat(0.5), eglfloat(0.5), eglfloat(0.8), eglfloat(1.0));
        self.check()
        opengles.glUniform2f(self.unif_scale, eglfloat(scale), eglfloat(scale));
        self.check()
        opengles.glUniform2f(self.unif_offset, eglfloat(offset[0]), eglfloat(offset[1]));
        self.check()
        opengles.glUniform1i(self.unif_tex, 0); # I don't really understand this part, perhaps it relates to active texture?
        self.check()
        
        opengles.glDrawArrays ( GL_TRIANGLE_FAN, 0, 4 );
        self.check()

        opengles.glBindBuffer(GL_ARRAY_BUFFER, 0);

        opengles.glFlush()
        opengles.glFinish()
        self.check()
        
        openegl.eglSwapBuffers(egl.display, egl.surface);
        self.check()      
        
    def check(self):
        e=opengles.glGetError()
        if e:
            print(hex(e))
            raise ValueError
        
def showerror():
    e=opengles.glGetError()
    print(hex(e))
    
if __name__ == "__main__":
    egl = EGL()
    d = demo()
    d.draw_mandelbrot_to_texture(0.003)
    m=pymouse.start_mouse()
    while 1:
        #offset=(400,600)
        offset=(m.x,m.y)
        d.draw_triangles(0.003,offset)
        time.sleep(0.01)
        if m.finished:
            break
    showerror()


        
    
