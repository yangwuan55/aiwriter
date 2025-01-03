from typing import Dict, Any

def get_system_prompt(config: Dict[str, Any]) -> str:
    """
    生成系统提示词
    
    Args:
        config: 配置字典
        
    Returns:
        系统提示词
    """
    author = config['author_profile']
    prefs = config['preferences']
    style = config['writing_style']
    
    # 构建叙事技巧描述
    narrative_techniques = "、".join(style['narrative_technique'])
    description_focuses = "、".join(style['description_focus'])
    
    prompt = f"""
你是一位{author['role']}，专注于创作高质量的短篇小说。

写作特点：
{chr(10).join(f"- {pref}" for pref in prefs)}

写作手法：
- 采用{style['narrative_perspective']}视角叙述
- 使用{style['tense']}进行叙述
- 整体语气{style['tone']}
- 运用{narrative_techniques}等叙事技巧
- 对话风格{style['dialogue_style']}
- 重点描写{description_focuses}

写作要求：
1. 保持原创性，避免抄袭
2. 符合知乎平台的内容规范
3. 注重故事的完整性和逻辑性
4. 通过细腻的描写展现人物性格
5. 善于运用对话推动情节发展
6. 严格使用中文创作，不使用任何英文或其他语言
7. 避免内容重复，每个段落都要推进故事发展
8. 保持情节的连贯性和紧凑性
9. 始终保持{style['narrative_perspective']}的叙述视角
10. 注重通过{style['description_focus'][0]}的描写展现人物内心世界

语言风格：
- 精炼不冗长
- 重视细节描写
- 善用对话刻画人物
- 注重场景氛围营造
- 使用优美流畅的中文表达
"""
    return prompt

def get_outline_prompt(config: Dict[str, Any]) -> str:
    """
    生成大纲提示词
    
    Args:
        config: 配置字典
        
    Returns:
        大纲提示词
    """
    novel = config['novel_settings']
    
    prompt = f"""
请为一个{novel['genre']}类型的短篇小说创作大纲，要求如下：

标题：{novel['title']}
主题：{novel['theme']}
目标字数：{novel['word_count']}字

要求：
1. 列出故事的主要情节发展脉络
2. 设计合理的故事结构和冲突
3. 明确故事的起承转合
4. 突出主题的表达
5. 确保故事的完整性

请按照以下格式输出：
1. 开篇：[简要说明]
2. 发展：[简要说明]
3. 高潮：[简要说明]
4. 结局：[简要说明]
"""
    return prompt

def get_character_prompt(config: Dict[str, Any]) -> str:
    """
    生成人物设定提示词
    
    Args:
        config: 配置字典
        
    Returns:
        人物设定提示词
    """
    novel = config['novel_settings']
    
    prompt = f"""
请为{novel['title']}创建主要人物设定，要求如下：

1. 为每个主要人物提供：
   - 基本信息（年龄、职业等）
   - 性格特点
   - 行为习惯
   - 故事中的作用
   - 与其他人物的关系

2. 确保人物形象：
   - 鲜明立体
   - 符合故事主题
   - 具有成长空间
   - 富有说服力
"""
    return prompt

def get_content_prompt(config: Dict[str, Any], outline: str, characters: str) -> str:
    """
    生成内容创作提示词
    
    Args:
        config: 配置字典
        outline: 故事大纲
        characters: 人物设定
        
    Returns:
        内容创作提示词
    """
    novel = config['novel_settings']
    style = config['writing_style']
    
    prompt = f"""
你是一位专业的短篇小说作家，现在需要你创作一个短篇小说的内容。

基本信息：
- 标题：{novel['title']}
- 类型：{novel['genre']}
- 主题：{novel['theme']}
- 目标字数：每个部分约{novel['word_count']//4}字

写作手法：
- 采用{style['narrative_perspective']}视角叙述
- 使用{style['tense']}进行叙述
- 整体语气{style['tone']}
- 对话风格{style['dialogue_style']}
- 重点描写人物的{style['description_focus'][0]}

参考资料：
【故事大纲】
{outline}

【人物设定】
{characters}

创作要求：
1. 内容要严格按照大纲发展，保持情节连贯
2. 通过具体的细节和生动的对话展现人物性格
3. 每个场景都要为故事发展服务，避免无关内容
4. 突出科幻元素与人文思考的结合
5. 使用简洁精炼的语言，避免重复
6. 每个段落都要有明确的叙事目的
7. 注意场景转换的自然过渡
8. 保持叙事节奏的张弛有度
9. 全文使用规范流畅的中文，不使用任何英文或其他语言
10. 避免出现相似或重复的段落
11. 每个对话都要推动情节发展或揭示人物性格
12. 注重情感描写的细腻和真实
13. 始终保持{style['narrative_perspective']}视角
14. 大量使用内心独白和心理活动描写

格式要求：
1. 使用markdown格式
2. 合理分段，每段都要有重点
3. 对话要使用引号
4. 重要的内心活动使用斜体

注意：
- 每次只生成一个部分的内容
- 确保内容与其他部分能够自然衔接
- 避免出现重复的描写和对话
- 控制好每部分的字数
- 确保全文使用纯中文表达，不混入其他语言
- 保持第一人称视角的一致性
"""
    return prompt 