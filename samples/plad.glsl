#ifdef GL_ES
precision mediump float;
#endif

#extension GL_OES_standard_derivatives : enable
// http://glslsandbox.com/e#31734.0

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

void main( void ) {
	
	float r = sin(gl_FragCoord.x/100.0+time*4.0)/2.0+0.5;
	float g = sin(gl_FragCoord.x/50.0+time*1.0)/1.0+0.5;
	float b = sin(gl_FragCoord.y/25.0+time*2.0)/2.0+0.5;
	gl_FragColor = vec4(r, g, b, 2.0);

}
