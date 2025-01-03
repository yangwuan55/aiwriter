# AI 小说生成器

基于 Ollama 的中文小说生成器，支持自动生成大纲、人物设定和小说内容，并具有智能重写和评分功能。

## 功能特点

- 支持生成多篇小说并自动选择最佳版本
- 分阶段生成：大纲、人物设定、内容（开篇、发展、高潮、结局）
- 智能重写机制：每个阶段都支持多次重写优化
- 自动评分系统：对生成的内容进行打分和分析
- 最终优化：支持对完整小说进行去重和连贯性优化
- 详细的日志记录：记录生成过程中的每个步骤和决策

## 配置说明

配置文件示例 (`config.yaml`):

```yaml
ai_settings:
  host: "http://localhost"  # Ollama服务器地址
  port: 11434              # Ollama服务器端口
  model: "qwen:7b"         # 使用的模型名称
  temperature: 0.7         # 生成温度（越高越随机）
  context_size: 4096       # 上下文窗口大小
  num_predict: 2048        # 每次生成的最大token数

novel_settings:
  title: "小说标题"        # 小说标题
  genre: "科幻"           # 小说类型
  theme: "人工智能"       # 小说主题
  word_count: 5000        # 目标字数

output_settings:
  output_dir: "./output"   # 输出根目录
  novel_count: 1          # 生成小说的数量

rewrite_settings:
  outline_rewrites: 2      # 大纲重写次数
  character_rewrites: 2    # 人物设定重写次数
  content_rewrites: 1      # 内容重写次数
  final_rewrites: 1        # 最终重写次数
  final_rewrite_min_score: 0.8  # 最终重写的最低评分要求
```

## 输出目录结构

```
output/                           # 输出根目录
├── novels/                      # 所有生成的小说
│   ├── 小说标题_1/             # 第一个版本
│   │   ├── outline.md          # 大纲
│   │   ├── characters.md       # 人物设定
│   │   └── 小说标题.md         # 小说内容
│   ├── 小说标题_2/             # 第二个版本
│   │   ├── ...
│   └── ...
└── 小说标题_best.md            # 评分最高的版本
```

## 使用方法

1. 确保已安装 Ollama 并启动服务
2. 安装依赖：`pip install -r requirements.txt`
3. 修改配置文件
4. 运行程序：`python main.py -c config.yaml`

## 注意事项

- 确保 Ollama 服务正常运行
- 根据实际需求调整重写次数和评分阈值
- 生成过程可能需要较长时间，请耐心等待
- 临时文件会在生成完成后自动删除

## 日志说明

程序运行时会记录详细的日志，包括：
- 生成过程的每个步骤
- 重写的评分和选择
- 错误和警告信息
- 最终评分和结果

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

[许可证类型] 