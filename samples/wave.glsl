#ifdef GL_ES
precision mediump float;
#endif

#extension GL_OES_standard_derivatives : enable

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

#define t time
#define r resolution.xy

void main(){
	vec3 c;
	float l,z=t;

	for(int i=0;i<3;i++) {
		vec2 uv,p = gl_FragCoord.xy/r;

		p -= 0.5;
		p.x *= r.x/r.y;

		z += abs(cos(t/2.0));
		l = length(p);

		uv += p/l * (sin(t*z*0.0005) * 3.00) * sin(l*abs(sin(t/8.0))*33.0 - z*2.0);
		c[i] = 0.10/length(abs(uv - 0.2));
	}

	gl_FragColor = vec4(c, 1.0);
}
