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
{context}"""
        
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
7. 营造符合当前阶段的情感氛围"""

    prompt += """

请确保：
1. 情节发展符合大纲设定
2. 人物性格符合设定
3. 叙事流畅自然
4. 细节描写生动
5. 对话真实有趣
6. 感情表达到位
7. 与前文保持连贯
8. 为后续情节做好铺垫"""

    return prompt

def get_rating_prompt() -> str:
    """
    生成评分提示词
    
    Returns:
        评分提示词
    """
    prompt = """你是一位专业的文学评论家，擅长对小说进行全面的评价和打分。
请从以下几个维度对小说进行评分和点评：
1. 情节设计 (25分)：故事的完整性、逻辑性和吸引力
2. 人物塑造 (25分)：角色的丰满度、真实性和成长性
3. 主题表达 (20分)：主题的深度和表达效果
4. 语言风格 (20分)：文字的流畅性和表现力
5. 创新性 (10分)：故事和表达方式的创新程度

请给出总分(满分100分)和详细的评分理由。
输出格式：
总分：XX/100

各项得分：
- 情节设计：XX/25
- 人物塑造：XX/25
- 主题表达：XX/20
- 语言风格：XX/20
- 创新性：XX/10

详细点评：
[具体分析各个维度的优缺点]

建议改进：
[列出2-3点具体的改进建议]"""
    return prompt

def get_rating_user_prompt(content: str) -> str:
    """
    生成评分用户提示词
    
    Args:
        content: 小说内容
        
    Returns:
        评分用户提示词
    """
    return f"请对以下小说进行评分和点评：\n\n{content}" 

def get_rewrite_feedback_prompt() -> str:
    """
    生成重写反馈提示词
    
    Returns:
        重写反馈提示词
    """
    prompt = """你是一位资深的文学编辑，请对以下内容进行分析并提供建设性的修改建议。

分析要求：
1. 找出内容中需要改进的地方
2. 提供具体的修改方向和建议
3. 指出可以进一步发展和深化的部分
4. 注意保持原有内容的优点

请按照以下格式输出：
## 优点
[列出2-3个主要优点]

## 需要改进的地方
[列出2-3个需要改进的具体问题]

## 修改建议
[为每个问题提供具体的改进建议]

## 深化建议
[提供1-2个可以进一步深化和发展的方向]"""
    return prompt

def get_rewrite_user_prompt(content_type: str, content: str) -> str:
    """
    生成重写用户提示词
    
    Args:
        content_type: 内容类型（outline/characters/content）
        content: 具体内容
        
    Returns:
        重写用户提示词
    """
    type_desc = {
        'outline': '故事大纲',
        'characters': '人物设定',
        'content': '小说内容'
    }
    return f"请对以下{type_desc[content_type]}进行分析并提供修改建议：\n\n{content}" 

def get_dedup_prompt() -> str:
    """
    生成去重提示词
    
    Returns:
        去重提示词
    """
    prompt = """你是一位专业的文学编辑，请仔细检查以下小说内容中的重复部分。

检查要求：
1. 找出内容实质重复的段落（不只是相似，而是表达同样的内容）
2. 找出重复的描写和对话
3. 找出重复的场景和情节
4. 注意检查不同段落之间可能存在的重复

输出格式：
## 重复内容列表
[列出所有发现的重复内容，每项包含：
- 重复内容的位置（通过引用内容的前几个字来标识位置）
- 重复的具体内容
- 建议保留哪个版本
- 如何处理被删除部分的上下文衔接]

## 去重建议
[提供具体的去重建议，包括：
- 如何合并或删除重复内容
- 如何保持文章的流畅性
- 如何处理段落之间的过渡]"""
    return prompt

def get_dedup_user_prompt(content: str) -> str:
    """
    生成去重用户提示词
    
    Args:
        content: 小说内容
        
    Returns:
        去重用户提示词
    """
    return f"请检查以下小说内容中的重复部分：\n\n{content}"

def get_dedup_fix_prompt(content: str, duplicates: str) -> str:
    """
    生成去重修复提示词
    
    Args:
        content: 原始内容
        duplicates: 重复内容分析
        
    Returns:
        去重修复提示词
    """
    prompt = f"""请根据以下重复内容分析，对小说进行修改：

原文：
{content}

重复内容分析：
{duplicates}

要求：
1. 删除或合并重复的内容
2. 保持文章的连贯性和流畅性
3. 确保段落之间的过渡自然
4. 保持故事的完整性
5. 维持人物和情节的一致性

请直接输出修改后的完整内容。"""
    return prompt 

def get_final_rewrite_prompt() -> str:
    """
    生成最终重写提示词
    
    Returns:
        最终重写提示词
    """
    prompt = """你是一位资深的文学编辑，请对整部小说进行全面分析并提供重写建议。

分析要求：
1. 检查内容是否与大纲一致
2. 检查人物性格是否符合设定
3. 检查情节发展是否连贯
4. 检查各部分之间的过渡是否自然
5. 检查主题表达是否充分
6. 检查细节描写是否生动
7. 检查是否存在重复内容
8. 分析当前写作风格的特点
9. 推荐一位适合这个主题的知名作家的写作风格

请按照以下格式输出：
## 大纲一致性分析
[分析内容是否符合大纲的各个部分，列出不一致的地方]

## 人物塑造分析
[分析人物性格是否前后一致，是否符合设定]

## 情节连贯性分析
[分析故事发展是否流畅，是否存在逻辑问题]

## 过渡衔接分析
[分析各部分之间的过渡是否自然]

## 主题表达分析
[分析主题是否得到充分展现]

## 重复内容分析
[列出所有重复的内容，包括：
- 重复的段落或句子
- 重复的描写或对话
- 重复的场景或情节]

## 写作风格分析
[分析当前写作风格的特点，包括：
- 语言特色
- 叙事方式
- 细节处理
- 情感表达
- 是否有明显的AI痕迹]

## 推荐作家风格
[推荐一位最适合这个主题和故事的知名作家，并说明：
- 作家简介
- 代表作品
- 写作风格特点
- 为什么这位作家的风格适合这个故事]

## 重写建议
[提供具体的重写建议，包括：
- 需要调整的情节
- 需要加强的描写
- 需要改进的对话
- 需要深化的主题
- 如何处理重复内容
- 如何模仿推荐作家的风格]"""
    return prompt

def get_final_rewrite_user_prompt(outline: str, characters: str, content: str) -> str:
    """
    生成最终重写用户提示词
    
    Args:
        outline: 故事大纲
        characters: 人物设定
        content: 小说内容
        
    Returns:
        最终重写用户提示词
    """
    return f"""请根据以下信息对小说进行分析：

【故事大纲】
{outline}

【人物设定】
{characters}

【小说内容】
{content}"""

def get_final_rewrite_fix_prompt(content: str, analysis: str) -> str:
    """
    生成最终重写修复提示词
    
    Args:
        content: 原始内容
        analysis: 分析结果
        
    Returns:
        最终重写修复提示词
    """
    prompt = f"""请根据以下分析结果对小说进行重写：

原文：
{content}

分析结果：
{analysis}

重写要求：
1. 保持故事的核心情节和主题不变
2. 调整不符合大纲的内容
3. 修正人物性格的不一致
4. 改善情节的连贯性
5. 优化部分之间的过渡
6. 加强主题的表达
7. 丰富细节描写
8. 删除或合并重复内容，确保：
   - 不同段落表达不同的内容
   - 避免重复的描写和对话
   - 每个场景都有独特的作用
   - 保持文章的流畅性
9. 按照推荐作家的风格重写，注意：
   - 模仿其独特的语言风格
   - 采用类似的叙事手法
   - 运用相似的细节描写方式
   - 体现其特有的情感表达方式
   - 避免明显的AI痕迹

请直接输出重写后的完整内容。"""
    return prompt 