cmake_minimum_required(VERSION 3.10)
project(Lexiconia VERSION 1.0.0 LANGUAGES CXX)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 设置输出目录
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 构建选项
option(BUILD_WITH_IMGUI "Build with Dear ImGui for debugging" ON)
option(BUILD_WITH_SPDLOG "Build with spdlog for logging" ON)

# 添加子目录（App）
add_subdirectory(LexiconiaApp)