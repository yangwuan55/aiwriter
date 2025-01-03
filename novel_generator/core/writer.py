from typing import Dict, Any, Tuple
from loguru import logger
from ..utils.api_utils import OllamaAPI
from ..utils.file_utils import save_content, get_unique_filename
from .. import prompts

class NovelWriter:
    def __init__(self, config: Dict[str, Any], api_client: OllamaAPI):
        """
        初始化小说写作器
        
        Args:
            config: 配置字典
            api_client: API客户端
        """
        self.config = config
        self.api_client = api_client
        
    def _get_rewrite_feedback(self, content_type: str, content: str) -> str:
        """
        获取重写反馈
        
        Args:
            content_type: 内容类型（outline/characters/content）
            content: 需要获取反馈的内容
            
        Returns:
            反馈内容
        """
        try:
            logger.info(f"正在获取{content_type}的重写反馈...")
            system_prompt = prompts.rewrite.get_rewrite_feedback_prompt(content_type)
            user_prompt = prompts.rewrite.get_rewrite_user_prompt(content_type, content)
            feedback = self.api_client.generate(system_prompt, user_prompt)
            return feedback
        except Exception as e:
            logger.error(f"获取重写反馈时发生错误: {str(e)}")
            return ""

    def _evaluate_feedback(self, feedback: str) -> float:
        """评估反馈的质量分数"""
        try:
            # 分析反馈中的关键部分
            sections = {
                "优点": 0.3,      # 权重0.3
                "需要改进": 0.3,  # 权重0.3
                "修改建议": 0.3,  # 权重0.3
                "深化建议": 0.1   # 权重0.1
            }
            
            score = 0.0
            for section, weight in sections.items():
                if section in feedback:
                    # 计算该部分的有效内容（去除标题和空行）
                    section_content = feedback.split(section)[1].split("##")[0].strip()
                    content_lines = [line.strip() for line in section_content.split('\n') if line.strip()]
                    
                    # 根据内容的具体性和深度评分
                    content_score = min(len(content_lines) * 0.2, 1.0)  # 每点0.2分，最高1分
                    score += content_score * weight
            
            logger.debug(f"反馈质量评分：{score:.2f}")
            return score
            
        except Exception as e:
            logger.error(f"评估反馈质量时发生错误: {str(e)}")
            return 0.0
            
    def generate_outline(self) -> str:
        """生成故事大纲"""
        logger.info("开始生成故事大纲...")
        
        best_outline = ""
        best_feedback = ""
        best_score = 0.0
        max_rewrites = self.config.get('rewrite_settings', {}).get('outline_rewrites', 0)
        logger.info(f"大纲重写次数设置为：{max_rewrites}次")
        
        for i in range(max_rewrites + 1):
            if i == 0:
                logger.info("生成初始版本大纲...")
            else:
                logger.info(f"开始第{i}/{max_rewrites}次重写大纲...")
                logger.info("上一版本反馈：")
                for line in best_feedback.split('\n'):
                    logger.info(f"  {line}")
            
            system_prompt = prompts.story.get_outline_prompt(self.config)
            if i > 0:  # 在提示词中加入上一次的反馈
                system_prompt += f"\n\n参考以下修改建议：\n{best_feedback}"
            
            outline = self.api_client.generate(system_prompt, "")
            logger.info(f"第{i if i > 0 else '初始'}版本大纲生成完成，长度: {len(outline)} 字符")
            
            if i < max_rewrites:  # 获取反馈用于下一次重写
                feedback = self._get_rewrite_feedback('outline', outline)
                current_score = self._evaluate_feedback(feedback)
                
                if not best_outline or current_score > best_score:
                    logger.info(f"发现更好的版本（评分：{current_score:.2f} > {best_score:.2f}），更新最佳大纲...")
                    best_outline = outline
                    best_feedback = feedback
                    best_score = current_score
                else:
                    logger.info(f"当前版本评分（{current_score:.2f}）未超过最佳版本（{best_score:.2f}），保留之前的最佳版本")
            else:
                best_outline = outline
                logger.info("完成所有重写，使用最终版本")
        
        # 获取不重复的大纲文件路径
        outline_base_path = os.path.join(self.config['output_settings']['save_path'], 'outline.md')
        outline_path = get_unique_filename(outline_base_path)
        
        # 保存最终版本
        save_content(best_outline, outline_path)
        
        return best_outline
        
    def generate_characters(self, outline: str) -> str:
        """生成人物设定"""
        logger.info("开始生成人物设定...")
        
        best_characters = ""
        best_feedback = ""
        best_score = 0.0
        max_rewrites = self.config.get('rewrite_settings', {}).get('character_rewrites', 0)
        logger.info(f"人物设定重写次数设置为：{max_rewrites}次")
        
        for i in range(max_rewrites + 1):
            if i == 0:
                logger.info("生成初始版本人物设定...")
            else:
                logger.info(f"开始第{i}/{max_rewrites}次重写人物设定...")
                logger.info("上一版本反馈：")
                for line in best_feedback.split('\n'):
                    logger.info(f"  {line}")
            
            system_prompt = prompts.character.get_character_prompt(self.config, outline)
            if i > 0:  # 在提示词中加入上一次的反馈
                system_prompt += f"\n\n参考以下修改建议：\n{best_feedback}"
            
            characters = self.api_client.generate(system_prompt, "")
            logger.info(f"第{i if i > 0 else '初始'}版本人物设定生成完成，长度: {len(characters)} 字符")
            
            if i < max_rewrites:  # 获取反馈用于下一次重写
                feedback = self._get_rewrite_feedback('characters', characters)
                current_score = self._evaluate_feedback(feedback)
                
                if not best_characters or current_score > best_score:
                    logger.info(f"发现更好的版本（评分：{current_score:.2f} > {best_score:.2f}），更新最佳人物设定...")
                    best_characters = characters
                    best_feedback = feedback
                    best_score = current_score
                else:
                    logger.info(f"当前版本评分（{current_score:.2f}）未超过最佳版本（{best_score:.2f}），保留之前的最佳版本")
            else:
                best_characters = characters
                logger.info("完成所有重写，使用最终版本")
        
        # 获取不重复的人物设定文件路径
        characters_base_path = os.path.join(self.config['output_settings']['save_path'], 'characters.md')
        characters_path = get_unique_filename(characters_base_path)
        
        # 保存最终版本
        save_content(best_characters, characters_path)
        
        return best_characters
        
    def generate_content(self, outline: str, characters: str) -> str:
        """生成小说内容"""
        logger.info("开始生成小说内容...")
        
        # 分四个部分生成
        parts = ['开篇', '发展', '高潮', '结局']
        content = ""
        temp_path = os.path.join(self.config['output_settings']['save_path'], f'{self.config["novel_settings"]["title"]}_temp.md')
        max_rewrites = self.config.get('rewrite_settings', {}).get('content_rewrites', 0)
        logger.info(f"内容重写次数设置为：{max_rewrites}次")
        
        for part_index, part_name in enumerate(parts, 1):
            logger.info(f"正在生成第{part_index}/4部分：{part_name}...")
            
            best_part = ""
            best_feedback = ""
            best_score = 0.0
            all_versions = []  # 存储所有生成的版本
            
            for i in range(max_rewrites + 1):
                if i == 0:
                    logger.info(f"生成初始版本{part_name}...")
                else:
                    logger.info(f"开始第{i}/{max_rewrites}次重写{part_name}...")
                    logger.info("上一版本反馈：")
                    for line in best_feedback.split('\n'):
                        logger.info(f"  {line}")
                
                # 构建提示词，包含已生成的内容作为上下文
                system_prompt = prompts.story.get_content_prompt(
                    self.config,
                    outline,
                    characters,
                    content if content else None,  # 传递已生成的内容作为上下文
                    part_name  # 传递当前部分名称
                )
                if i > 0:  # 在提示词中加入上一次的反馈
                    system_prompt += f"\n\n参考以下修改建议：\n{best_feedback}"
                
                current_part = self.api_client.generate(system_prompt, "")
                logger.info(f"第{i if i > 0 else '初始'}版本{part_name}生成完成，长度: {len(current_part)} 字符")
                
                # 存储当前版本
                all_versions.append({
                    'content': current_part,
                    'feedback': '',
                    'score': 0.0
                })
                
                if i < max_rewrites:  # 获取反馈用于下一次重写
                    feedback = self._get_rewrite_feedback('content', current_part)
                    current_score = self._evaluate_feedback(feedback)
                    all_versions[-1]['feedback'] = feedback
                    all_versions[-1]['score'] = current_score
                    
                    if not best_part or current_score > best_score:
                        logger.info(f"发现更好的{part_name}版本（评分：{current_score:.2f} > {best_score:.2f}），更新...")
                        best_part = current_part
                        best_feedback = feedback
                        best_score = current_score
                    else:
                        logger.info(f"当前{part_name}版本评分（{current_score:.2f}）未超过最佳版本（{best_score:.2f}），保留之前的最佳版本")
            
            # 从所有版本中选择最佳的
            best_version = max(all_versions, key=lambda x: x['score'])
            logger.info(f"选择评分最高的{part_name}版本（评分：{best_version['score']:.2f}）作为最终版本")
            content += best_version['content'] + "\n\n"
            
            # 保存临时文件
            save_content(content, temp_path)
        
        logger.success(f"小说内容生成完成！总长度: {len(content)} 字符")
        
        return content
        
    def final_rewrite(self, outline: str, characters: str, content: str) -> Tuple[str, float]:
        """
        最终重写并评分
        
        Returns:
            tuple: (最终内容, 评分)
        """
        try:
            logger.info("开始进行最终重写分析...")
            max_rewrites = self.config.get('rewrite_settings', {}).get('final_rewrites', 0)
            min_score = self.config.get('rewrite_settings', {}).get('final_rewrite_min_score', 0.8)
            
            if max_rewrites == 0:
                logger.info("未配置最终重写，直接进行评分...")
                # 对原文进行评分
                system_prompt = prompts.base.get_rating_prompt()
                user_prompt = prompts.base.get_rating_user_prompt(content)
                rating_result = self.api_client.generate(system_prompt, user_prompt)
                try:
                    score = float(rating_result.split('总分：')[1].split('/')[0])
                except:
                    score = 0
                    logger.warning("解析评分失败，设置为0分")
                return content, score
            
            logger.info(f"最终重写次数设置为：{max_rewrites}次，最低评分要求：{min_score}")
            
            best_content = content
            best_score = 0.0
            best_analysis = ""
            
            for i in range(max_rewrites):
                logger.info(f"开始第{i+1}/{max_rewrites}次最终重写...")
                
                # 获取分析结果
                system_prompt = prompts.rewrite.get_final_rewrite_prompt()
                user_prompt = prompts.rewrite.get_final_rewrite_user_prompt(outline, characters, best_content)
                analysis = self.api_client.generate(system_prompt, user_prompt)
                
                logger.info("获取到的分析结果：")
                for line in analysis.split('\n'):
                    logger.info(f"  {line}")
                
                # 评估分析质量
                current_score = self._evaluate_feedback(analysis)
                logger.info(f"当前分析评分：{current_score:.2f}")
                
                if current_score < min_score:
                    logger.info(f"分析质量（{current_score:.2f}）未达到最低要求（{min_score}），跳过本次重写")
                    continue
                    
                # 根据分析结果重写
                logger.info("开始根据分析结果重写...")
                system_prompt = prompts.rewrite.get_final_rewrite_fix_prompt(best_content, analysis)
                new_content = self.api_client.generate(system_prompt, "")
                
                # 对重写结果进行评分
                system_prompt = prompts.base.get_rating_prompt()
                user_prompt = prompts.base.get_rating_user_prompt(new_content)
                rating_result = self.api_client.generate(system_prompt, user_prompt)
                try:
                    new_score = float(rating_result.split('总分：')[1].split('/')[0])
                except:
                    new_score = 0
                    logger.warning("解析评分失败，设置为0分")
                
                logger.info(f"重写后的评分：{new_score:.2f}")
                
                if new_score > best_score:
                    logger.info(f"发现更好的版本（评分：{new_score:.2f} > {best_score:.2f}），更新...")
                    best_content = new_content
                    best_score = new_score
                    best_analysis = analysis
                else:
                    logger.info(f"当前版本（{new_score:.2f}）未超过最佳版本（{best_score:.2f}），保持不变")
            
            if best_score > 0:
                logger.success(f"最终重写完成，最终评分：{best_score:.2f}")
                return best_content, best_score
            else:
                # 如果没有找到更好的版本，对原文进行评分
                system_prompt = prompts.base.get_rating_prompt()
                user_prompt = prompts.base.get_rating_user_prompt(content)
                rating_result = self.api_client.generate(system_prompt, user_prompt)
                try:
                    score = float(rating_result.split('总分：')[1].split('/')[0])
                except:
                    score = 0
                    logger.warning("解析评分失败，设置为0分")
                logger.warning(f"未能生成更好的版本，使用原文（评分：{score:.2f}）")
                return content, score
            
        except Exception as e:
            logger.error(f"最终重写过程中发生错误: {str(e)}")
            logger.exception("详细错误信息：")
            # 发生错误时对原文进行评分
            try:
                system_prompt = prompts.base.get_rating_prompt()
                user_prompt = prompts.base.get_rating_user_prompt(content)
                rating_result = self.api_client.generate(system_prompt, user_prompt)
                score = float(rating_result.split('总分：')[1].split('/')[0])
            except:
                score = 0
                logger.warning("解析评分失败，设置为0分")
            return content, score 

    def _parse_rating(self, rating_result: str) -> float:
        """
        解析评分结果
        
        Args:
            rating_result: 评分结果文本
            
        Returns:
            总分（0-1之间的浮点数）
        """
        try:
            # 解析总分
            total_score = 0.0
            
            # 解析情节发展分数
            if '情节发展（' in rating_result:
                plot_score = float(rating_result.split('情节发展（')[1].split('/')[0])
                total_score += plot_score
                
            # 解析人物塑造分数
            if '人物塑造（' in rating_result:
                character_section = rating_result.split('人物塑造（')[1].split('##')[0]
                
                # 解析各个子项分数
                if '人物性格一致性（' in character_section:
                    consistency_score = float(character_section.split('人物性格一致性（')[1].split('/')[0])
                    total_score += consistency_score
                    
                if '人物行为合理性（' in character_section:
                    behavior_score = float(character_section.split('人物行为合理性（')[1].split('/')[0])
                    total_score += behavior_score
                    
                if '人物对话特色（' in character_section:
                    dialogue_score = float(character_section.split('人物对话特色（')[1].split('/')[0])
                    total_score += dialogue_score
                    
                if '人物成长体现（' in character_section:
                    growth_score = float(character_section.split('人物成长体现（')[1].split('/')[0])
                    total_score += growth_score
                
            # 解析主题表达分数
            if '主题表达（' in rating_result:
                theme_score = float(rating_result.split('主题表达（')[1].split('/')[0])
                total_score += theme_score
                
            # 解析写作技巧分数
            if '写作技巧（' in rating_result:
                technique_score = float(rating_result.split('写作技巧（')[1].split('/')[0])
                total_score += technique_score
                
            # 返回归一化的分数（0-1之间）
            return total_score / 100.0
            
        except Exception as e:
            logger.error(f"解析评分结果失败: {str(e)}")
            logger.error(f"评分结果内容: {rating_result}")
            return 0.0 