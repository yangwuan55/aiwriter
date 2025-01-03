from typing import Dict, Any

def get_character_prompt(config: Dict[str, Any], outline: str = None) -> str:
    """
    生成人物设定提示词
    
    Args:
        config: 配置字典
        outline: 故事大纲（可选）
        
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
   - 人物成长轨迹

2. 确保人物形象：
   - 鲜明立体
   - 符合故事主题
   - 具有成长空间
   - 富有说服力
   - 符合人设的行为模式
   - 合理的性格缺陷

3. 人物关系：
   - 明确各个人物之间的关系
   - 设计合理的关系互动
   - 为关系发展预留空间
   - 确保关系推动情节发展"""

    if outline:
        prompt += f"""

请基于以下大纲中的人物进行详细设定：
{outline}

注意：
1. 人物设定必须与大纲中的人物完全对应
2. 性格特点要能够解释大纲中的行为
3. 人物关系要符合大纲中的互动
4. 成长轨迹要与大纲中的情节发展相匹配"""
    
    return prompt 