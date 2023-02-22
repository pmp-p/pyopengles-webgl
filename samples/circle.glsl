#ifdef GL_ES
precision mediump float;
#endif

#extension GL_OES_standard_derivatives : enable

uniform vec2 resolution;

void main( void ) {
	// 1
	vec2 center = vec2(resolution.x/2.0, resolution.y/2.0);
 
	// 2
	float radius = resolution.x/2.0;
 
	// 3
	vec2 position = gl_FragCoord.xy - center;
 
	float z = sqrt(radius*radius - position.x*position.x - position.y*position.y);
	z /= radius;
	
	if(z < 0.6)
	{
		gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);		
	}
	if(z > 0.6)
	{
		gl_FragColor = vec4(0.0, 1.0, 0.0, 1.0);		
	}
	if(z > 0.8)
	{
		gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);		
	}

}
