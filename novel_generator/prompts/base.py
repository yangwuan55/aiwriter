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
    novel = config['novel_settings']
    
    # 构建叙事技巧描述
    narrative_techniques = "、".join(style['narrative_technique'])
    description_focuses = "、".join(style['description_focus'])
    
    prompt = f"""
你是一位{author['role']}，{author['description']}

写作特点：
{chr(10).join(f"- {pref}" for pref in prefs)}

写作手法：
- 采用{style['narrative_perspective']}视角叙述
- 使用{style['tense']}进行叙述
- 整体语气{style['tone']}
- 运用{narrative_techniques}等叙事技巧
- 对话风格{style['dialogue_style']}
- 重点描写{description_focuses}

参考风格：
{novel.get('style_reference', '无')}的写作特点：
- 善用华丽唯美的文字
- 擅长描写年轻人的情感世界
- 注重细节和氛围的营造
- 多用意象和象征手法
- 情节设计往往令人震撼

写作要求：
1. 保持原创性，避免抄袭
2. 符合目标读者的阅读习惯
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

def get_rating_prompt() -> str:
    """
    生成评分提示词
    """
    return """请对小说进行全面评分，评分标准如下：

1. 情节发展（20分）：
   - 故事结构的完整性
   - 情节发展的合理性
   - 冲突设置的合理性
   - 故事节奏的把控

2. 人物塑造（30分）：
   - 人物性格的一致性（10分）
   - 人物行为的合理性（10分）
   - 人物对话的特色（5分）
   - 人物成长的体现（5分）

3. 主题表达（20分）：
   - 主题的明确性
   - 主题的深度
   - 价值观的传达
   - 情感的感染力

4. 写作技巧（30分）：
   - 叙事视角的运用
   - 场景描写的生动性
   - 语言风格的统一
   - 细节刻画的精准

请按以下格式输出评分和分析：

## 情节发展（x/20分）
[详细分析]

## 人物塑造（x/30分）
1. 人物性格一致性（x/10分）：[分析每个主要人物的性格是否始终如一]
2. 人物行为合理性（x/10分）：[分析人物行为是否符合其性格和处境]
3. 人物对话特色（x/5分）：[分析对话是否体现人物特点]
4. 人物成长体现（x/5分）：[分析人物是否有合理的成长]

## 主题表达（x/20分）
[详细分析]

## 写作技巧（x/30分）
[详细分析]

总分：x/100"""

def get_rating_user_prompt(content: str) -> str:
    """
    生成评分用户提示词
    
    Args:
        content: 待评分的内容
        
    Returns:
        评分用户提示词
    """
    return f"""请对以下小说内容进行评分：

{content}""" 