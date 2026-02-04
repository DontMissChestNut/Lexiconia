#include <iostream>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

int main() {
    glm::vec3 vec(1.0f, 2.0f, 3.0f);
    std::cout << "向量: (" << vec.x << ", " << vec.y << ", " << vec.z << ")" << std::endl;
    
    glm::mat4 trans = glm::mat4(1.0f);
    trans = glm::translate(trans, glm::vec3(1.0f, 1.0f, 0.0f));
    trans = glm::rotate(trans, glm::radians(90.0f), glm::vec3(0.0, 0.0, 1.0));
    trans = glm::scale(trans, glm::vec3(0.5, 0.5, 0.5));
    
    std::cout << "GLM配置成功!" << std::endl;
    return 0;
}
