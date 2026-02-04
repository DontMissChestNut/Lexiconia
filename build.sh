#!/bin/bash
# build_run.sh - 带选项的构建运行脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
CLEAN=true
BUILD=true
RUN=true
JOBS=$(sysctl -n hw.ncpu)
BUILD_TYPE="Debug"
VERBOSE=false

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -h, --help         显示此帮助信息"
    echo "  -c, --clean        清理构建目录（默认：是）"
    echo "  -n, --no-clean     不清理构建目录"
    echo "  -b, --build-only   仅构建，不运行"
    echo "  -r, --run-only     仅运行，不重新构建"
    echo "  -j NUM             指定并行编译任务数（默认：CPU核心数）"
    echo "  -d, --debug        使用Debug构建类型（默认）"
    echo "  -r, --release      使用Release构建类型"
    echo "  -v, --verbose      显示详细输出"
    echo ""
    echo "示例:"
    echo "  $0                   # 清理并构建运行"
    echo "  $0 -n -j 4          # 增量构建，4个并行任务"
    echo "  $0 -b --release     # 仅构建Release版本"
    echo "  $0 -r               # 仅运行已有构建"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -n|--no-clean)
            CLEAN=false
            shift
            ;;
        -b|--build-only)
            RUN=false
            shift
            ;;
        --run-only)
            BUILD=false
            shift
            ;;
        -j)
            JOBS="$2"
            shift 2
            ;;
        -d|--debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        --release)
            BUILD_TYPE="Release"
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            echo -e "${RED}错误：未知选项 $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 项目目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$PROJECT_DIR/build"
EXECUTABLE="$BUILD_DIR/lexiconia"

echo -e "${BLUE}Lexiconia 构建脚本${NC}"
echo "========================================"
echo "项目目录: $PROJECT_DIR"
echo "构建目录: $BUILD_DIR"
echo "构建类型: $BUILD_TYPE"
echo "并行任务: $JOBS"
echo "清理构建: $CLEAN"
echo "执行构建: $BUILD"
echo "运行程序: $RUN"
echo "========================================"

# 清理构建目录
if [ "$CLEAN" = true ] && [ "$BUILD" = true ]; then
    echo -e "${YELLOW}清理构建目录...${NC}"
    rm -rf "$BUILD_DIR"
fi

# 创建构建目录
if [ "$BUILD" = true ]; then
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
    
    # 配置项目
    echo -e "${YELLOW}运行CMake配置...${NC}"
    if [ "$VERBOSE" = true ]; then
        cmake .. -DCMAKE_BUILD_TYPE=$BUILD_TYPE -DCMAKE_VERBOSE_MAKEFILE=ON
    else
        cmake .. -DCMAKE_BUILD_TYPE=$BUILD_TYPE
    fi
    
    # 编译项目
    echo -e "${YELLOW}编译项目...${NC}"
    if [ "$VERBOSE" = true ]; then
        make -j$JOBS VERBOSE=1
    else
        make -j$JOBS
    fi
    
    # 检查是否编译成功
    if [ ! -f "$EXECUTABLE" ]; then
        echo -e "${RED}错误：编译失败，可执行文件未生成${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}构建成功！${NC}"
fi

# 运行程序
if [ "$RUN" = true ]; then
    cd "$PROJECT_DIR"
    
    if [ ! -f "$EXECUTABLE" ]; then
        echo -e "${RED}错误：可执行文件不存在${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}运行程序...${NC}"
    echo "========================================"
    
    # 运行程序
    "$EXECUTABLE"
    
    EXIT_CODE=$?
    echo "========================================"
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}程序正常退出${NC}"
    else
        echo -e "${RED}程序异常退出，代码: $EXIT_CODE${NC}"
    fi
fi