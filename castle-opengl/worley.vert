#version 330
// Shawn Jones
// modified from github.com/geofmatthews/csci480/blob/master/lectures/110opengl/gmtutorials/shaders/worley.vert
// modified to do lighting calculations in world space instead of camera space

in vec4 position;
in vec4 normal;
in vec4 tangent;
in vec4 bitangent;
in vec2 uv;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fraguv;
out vec4 fragnormal;
out vec4 fragtangent;
out vec4 fragbitangent;
out vec4 frageye;
out vec4 fragposition;
out vec4 positionworldspace;
out vec4 positionobjectspace;
out vec4 positioncameraspace;

void main()
{
  fraguv = uv;
  positionobjectspace = position;
  positionworldspace = model * position;
  positioncameraspace = view * model * position;
  // Let's do the lighting calculations in world space
  fragnormal =  model * normal;
  fragtangent = model * tangent;
  fragbitangent = model * bitangent;
  mat4 vm = view * model;
  vec4 positioncamspace  = vm * position;

  // Where is the eye in cameraspace?
  frageye = normalize(vec4(0.0,0.0,0.0,1.0) - positioncamspace);
  // Can use world position or object position for different effects
  fragposition = positioncamspace;
  gl_Position = projection * positioncamspace;
}
