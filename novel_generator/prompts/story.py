from typing import Dict, Any

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
6. 在大纲中明确指出每个关键场景中的主要人物
7. 为每个主要人物预留成长和转变的空间

请按照以下格式输出：

## 主要人物
[列出故事中的主要人物，包括：
- 主角
- 重要配角
- 关键人物的基本特征]

## 故事大纲
1. 开篇：[简要说明，包含相关人物]
2. 发展：[简要说明，包含相关人物]
3. 高潮：[简要说明，包含相关人物]
4. 结局：[简要说明，包含相关人物]

## 人物关系
[简要说明主要人物之间的关系]
"""
    return prompt

def get_content_prompt(config: dict, outline: str, characters: str, context: str = None, current_part: str = None) -> str:
    """
    生成内容提示词
    
    Args:
        config: 配置信息
        outline: 故事大纲
        characters: 人物设定
        context: 已生成的内容（可选）
        current_part: 当前要生成的部分（开篇/发展/高潮/结局）
        
    Returns:
        内容提示词
    """
    prompt = f"""你是一位{config['author_profile']['role']}，请根据以下信息创作小说内容：

标题：{config['novel_settings']['title']}
类型：{config['novel_settings']['genre']}
主题：{config['novel_settings']['theme']}
目标读者：{config['novel_settings']['target_audience']}

写作要求：
1. 叙事视角：{config['writing_style']['narrative_perspective']}
2. 时态：{config['writing_style']['tense']}
3. 语气：{config['writing_style']['tone']}
4. 对话风格：{config['writing_style']['dialogue_style']}
5. 重点描写：{', '.join(config['writing_style']['description_focus'])}
6. 写作手法：{', '.join(config['writing_style']['narrative_technique'])}

故事大纲：
{outline}

人物设定：
{characters}"""

    if context:
        prompt += f"""

【前情提要】
{context}

【人物表现分析】
请分析前文中主要人物的表现：
1. 每个人物的性格特征展现
2. 重要的行为选择及其动机
3. 人物关系的发展变化
4. 情感状态的转变
5. 对其他人物的影响
6. 未充分展现的性格面向
7. 需要在后续补充的人物刻画

请在创作新内容时：
1. 保持人物性格的连贯性
2. 基于前文的人物关系继续发展
3. 展现人物的新面向
4. 深化人物的情感变化
5. 通过细节凸显人物特点"""
        
    if current_part:
        prompt += f"""

【当前任务】
请创作"{current_part}"部分的内容。要求：
1. 确保内容与前文自然衔接
2. 聚焦于当前部分的核心情节
3. 不要重复已经写过的内容
4. 不要透露后续剧情
5. 保持人物性格和行为的一致性
6. 通过细节描写和对话推进情节发展
7. 营造符合当前阶段的情感氛围
8. 在对话和行为中体现人物性格
9. 通过人物互动推动情节发展
10. 展现人物在当前阶段的心理变化"""

    prompt += """

请确保：
1. 情节发展符合大纲设定
2. 人物性格符合设定
3. 叙事流畅自然
4. 细节描写生动
5. 对话真实有趣
6. 感情表达到位
7. 与前文保持连贯
8. 为后续情节做好铺垫
9. 人物行为有合理动机
10. 性格特征在细节中体现"""

    return prompt 