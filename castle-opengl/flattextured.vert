#version 330
// Shawn Jones
// modified from github.com/geofmatthews/csci480/blob/master/lectures/110opengl/gmtutorials/shaders/flattextured.vert

in vec4 position;
in vec2 uv;
uniform vec2 scaleuv;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fraguv;
out vec4 fragposobjectspace;
out vec4 fragposcameraspace;

void main()
{
  vec4 positioncameraspace = view * model * position;
  gl_Position = projection * positioncameraspace;

  fraguv = scaleuv * uv;
  fragposobjectspace = position;
  fragposcameraspace = positioncameraspace;
}
