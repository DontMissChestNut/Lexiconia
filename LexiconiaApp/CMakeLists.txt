# 设置项目名称
set(TARGET_NAME LexiconiaApp)

# 明确启用C和C++语言
enable_language(C)
enable_language(CXX)

# 设置编译器
if(NOT CMAKE_C_COMPILER)
    set(CMAKE_C_COMPILER /usr/bin/cc)
endif()
if(NOT CMAKE_CXX_COMPILER)
    set(CMAKE_CXX_COMPILER /usr/bin/c++)
endif()

# 明确列出源文件
set(C_SOURCES 
    src/glad.c
)

set(CXX_SOURCES
    _main.cpp
    src/Core/Application.cpp
    src/Core/Logger.cpp
    src/Core/Time.cpp
    src/Core/Window.cpp
    src/Graphics/Shader.cpp
    src/Graphics/Camera.cpp
)

# 创建可执行文件
add_executable(${TARGET_NAME}
    ${C_SOURCES}
    ${CXX_SOURCES}
)

# 设置C标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译器选项：修复GLM警告
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "AppleClang")
    target_compile_options(${TARGET_NAME} PRIVATE 
        "-Wno-register"                  # GLM使用已弃用的register关键字
        "-Wno-deprecated-register"       # GLM使用已弃用的register关键字
        "-Wno-shift-op-parentheses"      # GLM运算符优先级警告
    )
endif()

# 包含目录
target_include_directories(${TARGET_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/include/Core
    ${CMAKE_CURRENT_SOURCE_DIR}/include/glad
    ${CMAKE_CURRENT_SOURCE_DIR}/include/GLFW
    ${CMAKE_CURRENT_SOURCE_DIR}/include/glm
    ${CMAKE_CURRENT_SOURCE_DIR}/include/KHR
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src/Core
)

target_compile_definitions(${TARGET_NAME} PRIVATE
    GL_SILENCE_DEPRECATION
)

# ========== 第三方库配置 ==========

# 1. GLFW（窗口管理）使用本地库
target_link_libraries(${TARGET_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/lib/libglfw3.a)

# macOS特定设置
if(APPLE)
    target_link_libraries(${TARGET_NAME} PRIVATE
        "-framework OpenGL"
        "-framework Cocoa"
        "-framework IOKit"
        "-framework CoreVideo"
    )
endif()

# 设置目标属性
set_target_properties(${TARGET_NAME} PROPERTIES
    OUTPUT_NAME "lexiconia"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

# 复制Assets目录
if(EXISTS ${CMAKE_SOURCE_DIR}/LexiconiaApp/Assets)
    add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/LexiconiaApp/Assets
        $<TARGET_FILE_DIR:${TARGET_NAME}>/Assets
        COMMENT "Copying Assets directory"
    )
endif()