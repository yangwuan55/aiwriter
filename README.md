# 知乎盐选小说生成器

这是一个基于Ollama的知乎盐选风格短篇小说生成器。它能够根据配置生成符合知乎盐选平台风格的短篇小说，包括故事大纲、人物设定和完整内容。

## 功能特点

- 支持自定义小说类型、主题和字数
- 自动生成故事大纲和人物设定
- 符合知乎盐选平台的写作风格
- 支持多种输出格式
- 可配置的AI参数

## 前置要求

1. 安装Ollama：
   - 访问 [Ollama官网](https://ollama.ai) 下载并安装
   - 拉取所需模型：`ollama pull llama2`（或其他模型）

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/newaiwriter.git
cd newaiwriter
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保Ollama服务正在运行：
```bash
ollama serve
```

2. 创建配置文件（参考 `config_template.yaml`）：
```yaml
# 配置文件示例
ai_settings:
  model: "llama2"
  host: "http://localhost"
  port: 11434
  temperature: 0.7
  context_size: 4096
  num_predict: 4000

author_profile:
  role: "知乎盐选短篇小说作家"
  language: "中文"
  version: "0.2"
  description: "专注于创作知乎盐选平台上的高质量短篇小说"

novel_settings:
  title: "逆时之境"
  genre: "科幻"
  word_count: 5000
  theme: "时间与爱情"
  target_audience: "知乎用户"

output_settings:
  format: "markdown"
  save_path: "./output"
  generate_outline: true
  generate_character_profiles: true
```

3. 运行生成器：
```bash
python main.py -c config.yaml -o output_directory
```

## 输出文件

生成器会在指定的输出目录中创建以下文件：
- `outline.md`: 故事大纲
- `characters.md`: 人物设定
- `{title}.md`: 小说正文

## 注意事项

- 确保Ollama服务正在运行
- 确保已安装所需的模型
- 合理设置生成参数，避免超出模型能力范围
- 建议使用较新版本的模型以获得更好的效果

## 许可证

MIT License 