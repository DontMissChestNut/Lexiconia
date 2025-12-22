# 设置项目名称
set(TARGET_NAME LexiconiaApp)

# 收集源文件
file(GLOB_RECURSE SRC_FILES 
    "src/*.cpp" 
    "src/*/*.cpp"
)

# 创建可执行文件
add_executable(${TARGET_NAME}
    _main.cpp
    ${SRC_FILES}
)

# 包含目录
target_include_directories(${TARGET_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_compile_definitions(${TARGET_NAME} PRIVATE
    GL_SILENCE_DEPRECATION
)

# ========== 第三方库配置 ==========

# 1. GLFW（窗口管理）
if(NOT TARGET glfw)
    include(FetchContent)
    FetchContent_Declare(
        glfw
        GIT_REPOSITORY https://github.com/glfw/glfw.git
        GIT_TAG 3.3.8
    )
    FetchContent_MakeAvailable(glfw)
    set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
    set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
    set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
endif()
target_link_libraries(${TARGET_NAME} PRIVATE glfw)

# 2. GLAD（OpenGL加载器）
# if(NOT TARGET glad)
#     include(FetchContent)
#     FetchContent_Declare(
#         glad
#         GIT_REPOSITORY https://github.com/Dav1dde/glad.git
#         GIT_TAG v0.1.36
#     )
#     FetchContent_GetProperties(glad)
#     if(NOT glad_POPULATED)
#         FetchContent_Populate(glad)
#         add_library(glad STATIC ${glad_SOURCE_DIR}/src/glad.c)
#         target_include_directories(glad PUBLIC ${glad_SOURCE_DIR}/include)
#     endif()
# endif()
# target_link_libraries(${TARGET_NAME} PRIVATE glad)
# target_include_directories(${TARGET_NAME} PRIVATE ${glad_SOURCE_DIR}/include)

# 3. glm（数学库）
# if(NOT TARGET glm)
#     include(FetchContent)
#     FetchContent_Declare(
#         glm
#         GIT_REPOSITORY https://github.com/g-truc/glm.git
#         GIT_TAG 0.9.9.8
#     )
#     FetchContent_MakeAvailable(glm)
# endif()

# 4. spdlog（日志系统 - 可选）
# if(BUILD_WITH_SPDLOG)
#     if(NOT TARGET spdlog)
#         include(FetchContent)
#         FetchContent_Declare(
#             spdlog
#             GIT_REPOSITORY https://github.com/gabime/spdlog.git
#             GIT_TAG v1.11.0
#         )
#         FetchContent_MakeAvailable(spdlog)
#     endif()
#     target_link_libraries(${TARGET_NAME} PRIVATE spdlog::spdlog)
#     target_compile_definitions(${TARGET_NAME} PRIVATE USE_SPDLOG)
# endif()

# 5. Dear ImGui（调试UI - 可选）
# if(BUILD_WITH_IMGUI)
#     if(NOT TARGET imgui)
#         include(FetchContent)
#         FetchContent_Declare(
#             imgui
#             GIT_REPOSITORY https://github.com/ocornut/imgui.git
#             GIT_TAG v1.89.7
#         )
#         FetchContent_MakeAvailable(imgui)
        
#         # 创建ImGui的GLFW+OpenGL3后端
#         add_library(imgui_impl STATIC
#             ${imgui_SOURCE_DIR}/backends/imgui_impl_glfw.cpp
#             ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp
#         )
#         target_include_directories(imgui_impl PUBLIC ${imgui_SOURCE_DIR})
#         target_link_libraries(imgui_impl PUBLIC glfw imgui)
#     endif()
#     target_link_libraries(${TARGET_NAME} PRIVATE imgui imgui_impl)
#     target_compile_definitions(${TARGET_NAME} PRIVATE USE_IMGUI)
# endif()

# 链接OpenGL库
# if(APPLE)
#     find_library(OPENGL_LIBRARY OpenGL)
#     target_link_libraries(${TARGET_NAME} PRIVATE ${OPENGL_LIBRARY})
# elseif(UNIX)
#     target_link_libraries(${TARGET_NAME} PRIVATE GL)
# elseif(WIN32)
#     target_link_libraries(${TARGET_NAME} PRIVATE opengl32)
# endif()

# 设置目标属性
# - 设置输出文件名
# - 设置运行时输出目录
set_target_properties(${TARGET_NAME} PROPERTIES
    OUTPUT_NAME "lexiconia"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

# 复制Assets目录
add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_SOURCE_DIR}/Assets
    $<TARGET_FILE_DIR:${TARGET_NAME}>/Assets
    COMMENT "Copying Assets directory"
)

