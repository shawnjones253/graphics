#version 330
// Shawn Jones
// modified from github.com/geofmatthews/csci480/blob/master/lectures/110opengl/gmtutorials/shaders/flattextured.frag
// added fog, added discard of reflected surfaces

uniform sampler2D sampler;
uniform float fade;
uniform bool useFog;
uniform vec4 fogColor;
uniform float fogStart;
uniform float fogEnd;

in vec2 fraguv;
in vec4 fragposobjectspace;
in vec4 fragposcameraspace;
out vec4 outputColor;

// from http://www.mbsoftworks.sk/index.php?page=tutorials&series=1&tutorial=15
float getFogFactor(float fogCoord)
{
	float result = 0.0;
	result = (fogEnd-fogCoord)/(fogEnd-fogStart);
	result = 1.0-clamp(result, 0.0, 1.0);
	
	return result;
}

void main()
{
  // discard terrain with positive elevation
  if (fragposobjectspace.y >= 0) {
      discard;
  }

  outputColor = fade*texture2D(sampler, fraguv);
  
  // add fog
  if (useFog) {
      float fogCoord = abs(fragposcameraspace.z);
      outputColor = mix(outputColor, fogColor, getFogFactor(fogCoord));
  }
}
