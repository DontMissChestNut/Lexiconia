#include "Graphics/Camera.hpp"
#include <iostream>

Camera::Camera(glm::vec3 position, glm::vec3 target, glm::vec3 up,
               float fov, float aspectRatio, float nearPlane, float farPlane)
    : m_Position(position)
    , m_WorldUp(up)
    , m_Yaw(-90.0f)     // 标准FPS相机初始值
    , m_Pitch(0.0f)
    , m_FOV(fov)
    , m_AspectRatio(aspectRatio)
    , m_NearPlane(nearPlane)
    , m_FarPlane(farPlane) {
    
    // 计算初始朝向
    glm::vec3 direction = glm::normalize(target - position);
    m_Pitch = glm::degrees(asin(direction.y));
    m_Yaw = glm::degrees(atan2(direction.z, direction.x));
    
    UpdateVectors();
}

void Camera::UpdateVectors() {
    // 计算新的前向量
    glm::vec3 front;
    front.x = cos(glm::radians(m_Yaw)) * cos(glm::radians(m_Pitch));
    front.y = sin(glm::radians(m_Pitch));
    front.z = sin(glm::radians(m_Yaw)) * cos(glm::radians(m_Pitch));
    m_Front = glm::normalize(front);
    
    // 重新计算右向量和上向量
    m_Right = glm::normalize(glm::cross(m_Front, m_WorldUp));
    m_Up = glm::normalize(glm::cross(m_Right, m_Front));
}

glm::mat4 Camera::GetViewMatrix() const {
    return glm::lookAt(m_Position, m_Position + m_Front, m_Up);
}

glm::mat4 Camera::GetProjectionMatrix() const {
    return glm::perspective(glm::radians(m_FOV), m_AspectRatio, m_NearPlane, m_FarPlane);
}

void Camera::SetPosition(const glm::vec3& position) {
    m_Position = position;
}

void Camera::SetTarget(const glm::vec3& target) {
    glm::vec3 direction = glm::normalize(target - m_Position);
    m_Pitch = glm::degrees(asin(direction.y));
    m_Yaw = glm::degrees(atan2(direction.z, direction.x));
    UpdateVectors();
}

void Camera::SetAspectRatio(float aspectRatio) {
    m_AspectRatio = aspectRatio;
}

void Camera::MoveForward(float distance) {
    m_Position += m_Front * distance;
}

void Camera::MoveRight(float distance) {
    m_Position += m_Right * distance;
}

void Camera::MoveUp(float distance) {
    m_Position += m_Up * distance;
}

void Camera::Rotate(float yaw, float pitch) {
    m_Yaw += yaw;
    m_Pitch += pitch;
    
    // 限制俯仰角，避免翻转
    if (m_Pitch > 89.0f) m_Pitch = 89.0f;
    if (m_Pitch < -89.0f) m_Pitch = -89.0f;
    
    UpdateVectors();
}