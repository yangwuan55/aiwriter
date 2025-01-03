import os
from typing import Dict, Any
import requests
from loguru import logger
from . import prompts

class NovelGenerator:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化小说生成器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.base_url = f"{config['ai_settings']['host']}:{config['ai_settings']['port']}"
        
        # 创建输出目录
        os.makedirs(config['output_settings']['save_path'], exist_ok=True)
        
    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用Ollama API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            
        Returns:
            API响应内容
        """
        try:
            # 构建完整的提示词
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # 准备请求数据
            data = {
                "model": self.config['ai_settings']['model'],
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.config['ai_settings']['temperature'],
                    "num_ctx": self.config['ai_settings']['context_size'],
                    "num_predict": self.config['ai_settings']['num_predict']
                }
            }
            
            # 发送请求
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            logger.error(f"调用Ollama API失败: {str(e)}")
            raise
            
    def generate_outline(self) -> str:
        """
        生成故事大纲
        
        Returns:
            故事大纲
        """
        logger.info("正在生成故事大纲...")
        system_prompt = prompts.get_system_prompt(self.config)
        outline_prompt = prompts.get_outline_prompt(self.config)
        
        outline = self._call_ollama(system_prompt, outline_prompt)
        
        # 保存大纲
        if self.config['output_settings']['generate_outline']:
            outline_path = os.path.join(
                self.config['output_settings']['save_path'],
                'outline.md'
            )
            with open(outline_path, 'w', encoding='utf-8') as f:
                f.write(outline)
                
        return outline
        
    def generate_characters(self) -> str:
        """
        生成人物设定
        
        Returns:
            人物设定
        """
        logger.info("正在生成人物设定...")
        system_prompt = prompts.get_system_prompt(self.config)
        character_prompt = prompts.get_character_prompt(self.config)
        
        characters = self._call_ollama(system_prompt, character_prompt)
        
        # 保存人物设定
        if self.config['output_settings']['generate_character_profiles']:
            char_path = os.path.join(
                self.config['output_settings']['save_path'],
                'characters.md'
            )
            with open(char_path, 'w', encoding='utf-8') as f:
                f.write(characters)
                
        return characters
        
    def generate_content(self, outline: str, characters: str) -> str:
        """
        生成小说内容
        
        Args:
            outline: 故事大纲
            characters: 人物设定
            
        Returns:
            小说内容
        """
        logger.info("正在生成小说内容...")
        system_prompt = prompts.get_system_prompt(self.config)
        content_prompt = prompts.get_content_prompt(self.config, outline, characters)
        
        # 分段生成内容
        sections = ['开篇', '发展', '高潮', '结局']
        content_parts = []
        
        for section in sections:
            logger.info(f"正在生成{section}部分...")
            section_prompt = f"{content_prompt}\n\n当前需要生成的是故事的{section}部分。"
            section_content = self._call_ollama(system_prompt, section_prompt)
            content_parts.append(section_content)
            
        # 组合所有内容
        title = self.config['novel_settings']['title']
        full_content = f"# {title}\n\n" + "\n\n".join(content_parts)
        
        # 保存小说内容
        content_path = os.path.join(
            self.config['output_settings']['save_path'],
            f"{title}.md"
        )
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        return full_content
        
    def generate(self):
        """
        生成完整的小说
        """
        # 生成大纲
        outline = self.generate_outline()
        
        # 生成人物设定
        characters = self.generate_characters()
        
        # 生成小说内容
        self.generate_content(outline, characters) 