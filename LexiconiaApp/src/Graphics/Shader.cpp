#include "Graphics/Shader.hpp"

#include <filesystem>

// 构造函数 - 从文件加载
Shader::Shader(const std::string& vertexPath, const std::string& fragmentPath)
    : m_ID(0)
    , m_IsValid(false)
    , m_VertexPath(vertexPath)
    , m_FragmentPath(fragmentPath) {
    
    // 读取着色器源码
    m_VertexSource = ReadFile(vertexPath);
    m_FragmentSource = ReadFile(fragmentPath);
    
    if (m_VertexSource.empty() || m_FragmentSource.empty()) {
        std::cerr << "ERROR::SHADER::Failed to load shader files" << std::endl;
        return;
    }
    
    // 编译和链接着色器
    unsigned int vertexShader = CompileShader(GL_VERTEX_SHADER, m_VertexSource);
    if (vertexShader == 0) return;
    
    unsigned int fragmentShader = CompileShader(GL_FRAGMENT_SHADER, m_FragmentSource);
    if (fragmentShader == 0) {
        glDeleteShader(vertexShader);
        return;
    }
    
    m_IsValid = LinkProgram(vertexShader, fragmentShader);
    
    // 删除着色器对象（已链接到程序中）
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
}

// 构造函数 - 从源码字符串加载
Shader::Shader(const std::string& vertexSource, const std::string& fragmentSource, bool fromString)
    : m_ID(0)
    , m_IsValid(false)
    , m_VertexPath("")
    , m_FragmentPath("") {
    
    m_VertexSource = vertexSource;
    m_FragmentSource = fragmentSource;
    
    // 编译和链接着色器
    unsigned int vertexShader = CompileShader(GL_VERTEX_SHADER, m_VertexSource);
    if (vertexShader == 0) return;
    
    unsigned int fragmentShader = CompileShader(GL_FRAGMENT_SHADER, m_FragmentSource);
    if (fragmentShader == 0) {
        glDeleteShader(vertexShader);
        return;
    }
    
    m_IsValid = LinkProgram(vertexShader, fragmentShader);
    
    // 删除着色器对象
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
}

// 析构函数
Shader::~Shader() {
    Clear();
}

// 移动构造函数
Shader::Shader(Shader&& other) noexcept
    : m_ID(other.m_ID)
    , m_IsValid(other.m_IsValid)
    , m_VertexPath(std::move(other.m_VertexPath))
    , m_FragmentPath(std::move(other.m_FragmentPath))
    , m_VertexSource(std::move(other.m_VertexSource))
    , m_FragmentSource(std::move(other.m_FragmentSource))
    , m_UniformLocationCache(std::move(other.m_UniformLocationCache)) {
    
    other.m_ID = 0;
    other.m_IsValid = false;
}

// 移动赋值运算符
Shader& Shader::operator=(Shader&& other) noexcept {
    if (this != &other) {
        Clear();
        
        m_ID = other.m_ID;
        m_IsValid = other.m_IsValid;
        m_VertexPath = std::move(other.m_VertexPath);
        m_FragmentPath = std::move(other.m_FragmentPath);
        m_VertexSource = std::move(other.m_VertexSource);
        m_FragmentSource = std::move(other.m_FragmentSource);
        m_UniformLocationCache = std::move(other.m_UniformLocationCache);
        
        other.m_ID = 0;
        other.m_IsValid = false;
    }
    return *this;
}

// 清理资源
void Shader::Clear() {
    if (m_ID != 0) {
        glDeleteProgram(m_ID);
        m_ID = 0;
    }
    m_UniformLocationCache.clear();
    m_IsValid = false;
}

// 读取文件内容
std::string Shader::ReadFile(const std::string& filepath) {
    std::string content;
    std::ifstream file;
    
    // 确保可以抛出异常
    file.exceptions(std::ifstream::failbit | std::ifstream::badbit);
    
    try {
        // 打开文件
        file.open(filepath);
        std::stringstream stream;
        stream << file.rdbuf();
        file.close();
        content = stream.str();
    } catch (std::ifstream::failure& e) {
        std::cerr << "ERROR::SHADER::FILE_NOT_SUCCESSFULLY_READ: " 
                  << filepath << std::endl;
        std::cerr << "Exception: " << e.what() << std::endl;
        return "";
    }
    
    return content;
}

// 编译着色器
unsigned int Shader::CompileShader(GLenum type, const std::string& source) {
    unsigned int shader = glCreateShader(type);
    const char* src = source.c_str();
    glShaderSource(shader, 1, &src, nullptr);
    glCompileShader(shader);
    
    // 检查编译错误
    CheckCompileErrors(shader, 
        (type == GL_VERTEX_SHADER) ? "VERTEX" : 
        (type == GL_FRAGMENT_SHADER) ? "FRAGMENT" : 
        "UNKNOWN");
    
    // 验证编译是否成功
    int success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        glDeleteShader(shader);
        return 0;
    }
    
    return shader;
}

// 链接着色器程序
bool Shader::LinkProgram(unsigned int vertexShader, unsigned int fragmentShader) {
    m_ID = glCreateProgram();
    glAttachShader(m_ID, vertexShader);
    glAttachShader(m_ID, fragmentShader);
    glLinkProgram(m_ID);
    
    // 检查链接错误
    CheckCompileErrors(m_ID, "PROGRAM");
    
    int success;
    glGetProgramiv(m_ID, GL_LINK_STATUS, &success);
    return success == GL_TRUE;
}

// 检查编译/链接错误
void Shader::CheckCompileErrors(unsigned int shader, const std::string& type) {
    int success;
    char infoLog[1024];
    
    if (type != "PROGRAM") {
        glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
        if (!success) {
            glGetShaderInfoLog(shader, 1024, nullptr, infoLog);
            std::cerr << "ERROR::SHADER_COMPILATION_ERROR of type: " << type << std::endl;
            std::cerr << infoLog << std::endl;
            std::cerr << "----------------------------------------" << std::endl;
        }
    } else {
        glGetProgramiv(shader, GL_LINK_STATUS, &success);
        if (!success) {
            glGetProgramInfoLog(shader, 1024, nullptr, infoLog);
            std::cerr << "ERROR::PROGRAM_LINKING_ERROR of type: " << type << std::endl;
            std::cerr << infoLog << std::endl;
            std::cerr << "----------------------------------------" << std::endl;
        }
    }
}

// 获取Uniform位置（带缓存）
int Shader::GetUniformLocation(const std::string& name) {
    // 检查缓存
    auto it = m_UniformLocationCache.find(name);
    if (it != m_UniformLocationCache.end()) {
        return it->second;
    }
    
    // 从OpenGL获取
    int location = glGetUniformLocation(m_ID, name.c_str());
    
    // 缓存结果
    m_UniformLocationCache[name] = location;
    
    // 调试信息（可选）
    #ifdef DEBUG
    if (location == -1) {
        std::cerr << "WARNING::SHADER::Uniform '" << name 
                  << "' doesn't exist in shader ID: " << m_ID << std::endl;
    }
    #endif
    
    return location;
}

// 绑定着色器程序
void Shader::Bind() const {
    if (m_IsValid) {
        glUseProgram(m_ID);
    }
}

// 解绑着色器程序
void Shader::Unbind() const {
    glUseProgram(0);
}

// 重新编译着色器（热重载）
bool Shader::Recompile() {
    if (m_VertexPath.empty() || m_FragmentPath.empty()) {
        std::cerr << "ERROR::SHADER::Cannot recompile shader created from strings" << std::endl;
        return false;
    }
    
    // 重新读取文件
    std::string newVertexSource = ReadFile(m_VertexPath);
    std::string newFragmentSource = ReadFile(m_FragmentPath);
    
    if (newVertexSource.empty() || newFragmentSource.empty()) {
        return false;
    }
    
    // 检查源码是否改变
    if (newVertexSource == m_VertexSource && newFragmentSource == m_FragmentSource) {
        return true; // 没有改变，但返回成功
    }
    
    // 保存旧ID用于清理
    unsigned int oldID = m_ID;
    
    // 编译新的着色器
    unsigned int vertexShader = CompileShader(GL_VERTEX_SHADER, newVertexSource);
    if (vertexShader == 0) return false;
    
    unsigned int fragmentShader = CompileShader(GL_FRAGMENT_SHADER, newFragmentSource);
    if (fragmentShader == 0) {
        glDeleteShader(vertexShader);
        return false;
    }
    
    // 链接新程序
    m_ID = glCreateProgram();
    glAttachShader(m_ID, vertexShader);
    glAttachShader(m_ID, fragmentShader);
    glLinkProgram(m_ID);
    
    // 检查链接
    int success;
    glGetProgramiv(m_ID, GL_LINK_STATUS, &success);
    
    if (success) {
        // 更新源码
        m_VertexSource = std::move(newVertexSource);
        m_FragmentSource = std::move(newFragmentSource);
        
        // 清空Uniform缓存
        m_UniformLocationCache.clear();
        
        // 删除旧程序
        glDeleteProgram(oldID);
        
        // 删除着色器对象
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        
        m_IsValid = true;
        std::cout << "INFO::SHADER::Successfully recompiled shader: " 
                  << m_VertexPath << ", " << m_FragmentPath << std::endl;
        return true;
    } else {
        // 失败，恢复旧ID
        m_ID = oldID;
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        return false;
    }
}

// ================= Uniform设置方法 =================

void Shader::SetBool(const std::string& name, bool value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform1i(location, static_cast<int>(value));
    }
}

void Shader::SetInt(const std::string& name, int value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform1i(location, value);
    }
}

void Shader::SetFloat(const std::string& name, float value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform1f(location, value);
    }
}

void Shader::SetVec2(const std::string& name, const glm::vec2& value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform2f(location, value.x, value.y);
    }
}

void Shader::SetVec2(const std::string& name, float x, float y) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform2f(location, x, y);
    }
}

void Shader::SetVec3(const std::string& name, const glm::vec3& value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform3f(location, value.x, value.y, value.z);
    }
}

void Shader::SetVec3(const std::string& name, float x, float y, float z) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform3f(location, x, y, z);
    }
}

void Shader::SetVec4(const std::string& name, const glm::vec4& value) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform4f(location, value.x, value.y, value.z, value.w);
    }
}

void Shader::SetVec4(const std::string& name, float x, float y, float z, float w) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniform4f(location, x, y, z, w);
    }
}

void Shader::SetMat2(const std::string& name, const glm::mat2& mat) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniformMatrix2fv(location, 1, GL_FALSE, glm::value_ptr(mat));
    }
}

void Shader::SetMat3(const std::string& name, const glm::mat3& mat) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniformMatrix3fv(location, 1, GL_FALSE, glm::value_ptr(mat));
    }
}

void Shader::SetMat4(const std::string& name, const glm::mat4& mat) {
    int location = GetUniformLocation(name);
    if (location != -1) {
        glUniformMatrix4fv(location, 1, GL_FALSE, glm::value_ptr(mat));
    }
}

void Shader::SetTexture(const std::string& name, int textureUnit) {
    SetInt(name, textureUnit);
}

void Shader::SetTexture2D(const std::string& name, unsigned int textureID, int textureUnit) {
    // 激活纹理单元
    glActiveTexture(GL_TEXTURE0 + textureUnit);
    // 绑定纹理
    glBindTexture(GL_TEXTURE_2D, textureID);
    // 设置Uniform
    SetInt(name, textureUnit);
}

// ================= 便捷方法 =================

void Shader::SetTransformMatrices(const glm::mat4& model, const glm::mat4& view, const glm::mat4& projection) {
    SetMat4("u_Model", model);
    SetMat4("u_View", view);
    SetMat4("u_Projection", projection);
    
    // 计算并设置Model-View矩阵和法线矩阵
    glm::mat4 modelView = view * model;
    glm::mat3 normalMatrix = glm::transpose(glm::inverse(glm::mat3(model)));
    
    SetMat4("u_ModelView", modelView);
    SetMat3("u_NormalMatrix", normalMatrix);
}

void Shader::SetCameraPosition(const glm::vec3& position) {
    SetVec3("u_CameraPosition", position);
}

void Shader::SetTime(float time) {
    SetFloat("u_Time", time);
}