// test_path.cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::string paths[] = {
        "assets/shaders/basic.vert",
        "Assets/shaders/basic.vert",
        "../assets/shaders/basic.vert",
        "./assets/shaders/basic.vert",
        "build/assets/shaders/basic.vert",
        "build/Assets/shaders/basic.vert"
    };
    
    for (const auto& path : paths) {
        std::ifstream file(path);
        if (file.is_open()) {
            std::cout << "✓ Found: " << path << std::endl;
            file.close();
        } else {
            std::cout << "✗ Not found: " << path << std::endl;
        }
    }
    
    // 当前工作目录
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd))) {
        std::cout << "Current working directory: " << cwd << std::endl;
    }
    
    return 0;
}