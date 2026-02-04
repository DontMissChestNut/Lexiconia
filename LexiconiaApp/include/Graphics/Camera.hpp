#ifndef CAMERA_HPP
#define CAMERA_HPP

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

class Camera {
public:
    Camera(glm::vec3 position = glm::vec3(0.0f, 0.0f, 3.0f),
           glm::vec3 target = glm::vec3(0.0f, 0.0f, 0.0f),
           glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f),
           float fov = 45.0f, float aspectRatio = 16.0f/9.0f,
           float nearPlane = 0.1f, float farPlane = 100.0f);
    
    // 获取矩阵
    glm::mat4 GetViewMatrix() const;
    glm::mat4 GetProjectionMatrix() const;
    glm::vec3 GetPosition() const { return m_Position; }
    
    // 相机控制
    void SetPosition(const glm::vec3& position);
    void SetTarget(const glm::vec3& target);
    void SetAspectRatio(float aspectRatio);
    
    // 移动相机
    void MoveForward(float distance);
    void MoveRight(float distance);
    void MoveUp(float distance);
    
    // 旋转相机
    void Rotate(float yaw, float pitch); // 偏航角和俯仰角
    
private:
    void UpdateVectors();
    
    glm::vec3 m_Position;
    glm::vec3 m_Front;
    glm::vec3 m_Up;
    glm::vec3 m_Right;
    glm::vec3 m_WorldUp;
    
    float m_Yaw;        // 偏航角
    float m_Pitch;      // 俯仰角
    
    float m_FOV;        // 视野角度
    float m_AspectRatio;// 宽高比
    float m_NearPlane;  // 近平面
    float m_FarPlane;   // 远平面
};

#endif // CAMERA_HPP