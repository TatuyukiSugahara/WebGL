attribute vec3 position;
uniform mat4 wvpMatrix;

void main(void)
{
	gl_Position = wvpMatirx * vec4(position,1.0);
}