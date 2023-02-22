#ifdef GL_ES
precision mediump float;
#endif
// http://glslsandbox.com/e#31735.0
#extension GL_OES_standard_derivatives : enable

#define M_PI 3.14159265358979323846

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;


// Simplex 2D noise
//
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }

float snoise(vec2 v){
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
           -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy) );
  vec2 x0 = v -   i + dot(i, C.xx);
  vec2 i1;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 ))
  + i.x + vec3(0.0, i1.x, 1.0 ));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
    dot(x12.zw,x12.zw)), 0.0);
  m = m*m ;
  m = m*m ;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}


void main( void ) {

	vec2 seed1 = vec2(gl_FragCoord.x + (50.0 * time), gl_FragCoord.y) / 300.0;
	vec2 seed2 = vec2(gl_FragCoord.x + (12.0 * time), gl_FragCoord.y + (-64.0 * time)) / 300.0;
	vec2 seed3 = vec2(gl_FragCoord.x, gl_FragCoord.y + (25.0 * time)) / 300.0;
	
	
	float r = (snoise(seed1) + snoise(seed2)) + 1.0;
	float g = (snoise(seed2) + snoise(seed3)) + 2.0;
	float b = (snoise(seed3) + snoise(seed1)) + 1.0;
	
	vec3 normalmap = normalize(vec3(r,g,b));
	
	vec3 l = vec3(abs(mouse.xy - 0.5), 0.9);
	
	float cosTheta = clamp(dot(normalmap,l) , 0.0, 1.0);
	
	vec3 product = mix(vec3(0.0,0.2,0.6),vec3(0.4,0.2,0.4),cosTheta);
	product = mix(product, vec3(0.8,0.6,0.1), pow(cosTheta,5.0));
	product = mix(product, vec3(1.0,1.0,0.0), pow(cosTheta,12.0));

	
	gl_FragColor = vec4(product.rgb,1.0);
}