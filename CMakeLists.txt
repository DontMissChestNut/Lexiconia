cmake_minimum_required(VERSION 3.10)
project(LexiconiaApp)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# 查找 GLFW
find_package(glfw3 REQUIRED)

# 添加可执行文件
add_executable(app 
    LexiconiaApp/src/_main.cpp
    LexiconiaApp/src/glad.cpp
)

# 包含目录
target_include_directories(app PRIVATE 
    LexiconiaApp/include
    ${GLFW_INCLUDE_DIRS}
)

# 链接库
target_link_libraries(app glfw)

# macOS 特定设置
if(APPLE)
    target_link_libraries(app "-framework OpenGL")
    target_link_libraries(app "-framework Cocoa")
    target_link_libraries(app "-framework IOKit")
    target_link_libraries(app "-framework CoreVideo")
endif()