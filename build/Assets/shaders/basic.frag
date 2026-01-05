#version 330 core

// 输入
in vec3 v_Normal;
in vec3 v_FragPos;
in vec2 v_TexCoord;

// Uniform
uniform vec3 u_ObjectColor = vec3(1.0, 0.5, 0.2);
uniform sampler2D u_Texture;
uniform bool u_UseTexture = false;

// 光照Uniforms
uniform vec3 u_LightPosition = vec3(2.0, 2.0, 2.0);
uniform vec3 u_LightColor = vec3(1.0, 1.0, 1.0);
uniform float u_LightIntensity = 1.0;

// 相机位置（用于镜面高光）
uniform vec3 u_CameraPosition;

// 输出
out vec4 FragColor;

void main() {
    // 基础颜色
    vec3 color;
    if (u_UseTexture) {
        color = texture(u_Texture, v_TexCoord).rgb;
    } else {
        color = u_ObjectColor;
    }
    
    // 简单的光照计算（环境光 + 漫反射）
    vec3 ambient = 0.1 * u_LightColor;
    
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(u_LightPosition - v_FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * u_LightColor;
    
    // 镜面高光
    vec3 viewDir = normalize(u_CameraPosition - v_FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = 0.5 * spec * u_LightColor;
    
    // 最终颜色
    vec3 result = (ambient + diffuse + specular) * color * u_LightIntensity;
    FragColor = vec4(result, 1.0);
}