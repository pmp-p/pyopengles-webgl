#ifdef GL_ES
precision mediump float;
#endif

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

// rosace3:  original see https://www.shadertoy.com/view/Md3XWM
void main( void ) 
{
        vec2 O = gl_FragColor.xy;
	vec2 U =  gl_FragCoord.xy;
	gl_FragColor = abs(sin(time/1.0)) / abs( cos(time/1.0)*length(U+=U-(O=resolution.xy))/O.y 
                 - sin ( 7.*atan(U.x,U.y)  - time*0.5 ) 
                 - .5*vec4(1,3,4,1) );;

}

