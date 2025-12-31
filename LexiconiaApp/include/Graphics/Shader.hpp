#ifndef SHADER_HPP
#define SHADER_HPP

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>
#include <memory>

class Shader {
public:
    // 构造函数 - 从文件路径创建着色器
    Shader(const std::string& vertexPath, const std::string& fragmentPath);
    
    // 构造函数 - 从源码字符串创建着色器
    Shader(const std::string& vertexSource, const std::string& fragmentSource, bool fromString);
    
    // 析构函数
    ~Shader();
    
    // 禁用拷贝构造和赋值（OpenGL对象不能简单拷贝）
    Shader(const Shader&) = delete;
    Shader& operator=(const Shader&) = delete;
    
    // 移动构造和赋值
    Shader(Shader&& other) noexcept;
    Shader& operator=(Shader&& other) noexcept;
    
    // 使用着色器程序
    void Bind() const;
    void Unbind() const;
    
    // 重载编译（热重载）
    bool Recompile();
    
    // 获取着色器程序ID
    unsigned int GetID() const { return m_ID; }
    
    // 检查着色器是否有效
    bool IsValid() const { return m_IsValid; }
    
    // Uniform设置方法
    void SetBool(const std::string& name, bool value);
    void SetInt(const std::string& name, int value);
    void SetFloat(const std::string& name, float value);
    void SetVec2(const std::string& name, const glm::vec2& value);
    void SetVec2(const std::string& name, float x, float y);
    void SetVec3(const std::string& name, const glm::vec3& value);
    void SetVec3(const std::string& name, float x, float y, float z);
    void SetVec4(const std::string& name, const glm::vec4& value);
    void SetVec4(const std::string& name, float x, float y, float z, float w);
    void SetMat2(const std::string& name, const glm::mat2& mat);
    void SetMat3(const std::string& name, const glm::mat3& mat);
    void SetMat4(const std::string& name, const glm::mat4& mat);
    
    // 纹理相关
    void SetTexture(const std::string& name, int textureUnit);
    void SetTexture2D(const std::string& name, unsigned int textureID, int textureUnit);
    
    // 便捷方法 - 设置常用Uniform组
    void SetTransformMatrices(const glm::mat4& model, const glm::mat4& view, const glm::mat4& projection);
    void SetCameraPosition(const glm::vec3& position);
    void SetTime(float time);
    
    // 获取着色器信息
    const std::string& GetVertexPath() const { return m_VertexPath; }
    const std::string& GetFragmentPath() const { return m_FragmentPath; }
    
private:
    // 私有辅助方法
    std::string ReadFile(const std::string& filepath);
    unsigned int CompileShader(GLenum type, const std::string& source);
    bool LinkProgram(unsigned int vertexShader, unsigned int fragmentShader);
    void CheckCompileErrors(unsigned int shader, const std::string& type);
    int GetUniformLocation(const std::string& name);
    void Clear();
    
    // 成员变量
    unsigned int m_ID;
    bool m_IsValid;
    std::string m_VertexPath;
    std::string m_FragmentPath;
    std::string m_VertexSource;
    std::string m_FragmentSource;
    std::unordered_map<std::string, int> m_UniformLocationCache;
};

#endif // SHADER_HPP