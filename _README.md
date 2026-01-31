# Lexiconia - 言灵王权

## Web
**Related Packages**

conda activate lexiconia

conda install flask nunmpy pandas bs4 requests lxml
- flask
- numpy
- pandas
- bs4
- requests
- lxml


FileOrganization
Lexiconia/
├── .vscode/
│   ├── tasks.json         # VSCode任务
│   └── launch.json        # 调试配置
├── build/                  # 构建目录（CMake生成）
├── LexiconiaApp/
│   ├── include/
│   │   ├── glad/
│   │   └── KHR/
│   └── src/
│       ├── _main.cpp
│       └── glad.cpp
└── CMakeLists.txt          # CMake配置