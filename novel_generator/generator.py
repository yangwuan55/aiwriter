import os
from typing import Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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
        logger.info(f"初始化生成器 - 模型: {config['ai_settings']['model']}, 温度: {config['ai_settings']['temperature']}")
        
        # 创建带有重试机制的会话
        self.session = requests.Session()
        retries = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        logger.debug("已配置重试机制：最大重试3次，间隔1秒")
        
        # 创建输出目录
        os.makedirs(config['output_settings']['save_path'], exist_ok=True)
        logger.info(f"输出目录: {config['output_settings']['save_path']}")
        
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
            prompt_length = len(full_prompt)
            logger.debug(f"提示词长度: {prompt_length} 字符")
            
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
            logger.debug("开始调用Ollama API...")
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=300  # 设置5分钟超时
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            response_length = len(result.get('response', ''))
            logger.debug(f"API调用成功，响应长度: {response_length} 字符")
            return result.get('response', '')
            
        except requests.exceptions.Timeout:
            logger.error("调用Ollama API超时（5分钟）")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"调用Ollama API失败: {str(e)}")
            raise
            
    def generate_outline(self) -> str:
        """
        生成故事大纲
        
        Returns:
            故事大纲
        """
        logger.info("开始生成故事大纲...")
        system_prompt = prompts.get_system_prompt(self.config)
        outline_prompt = prompts.get_outline_prompt(self.config)
        
        outline = self._call_ollama(system_prompt, outline_prompt)
        logger.info(f"大纲生成完成，长度: {len(outline)} 字符")
        
        # 保存大纲
        if self.config['output_settings']['generate_outline']:
            outline_path = os.path.join(
                self.config['output_settings']['save_path'],
                'outline.md'
            )
            with open(outline_path, 'w', encoding='utf-8') as f:
                f.write(outline)
            logger.info(f"大纲已保存至: {outline_path}")
                
        return outline
        
    def generate_characters(self) -> str:
        """
        生成人物设定
        
        Returns:
            人物设定
        """
        logger.info("开始生成人物设定...")
        system_prompt = prompts.get_system_prompt(self.config)
        character_prompt = prompts.get_character_prompt(self.config)
        
        characters = self._call_ollama(system_prompt, character_prompt)
        logger.info(f"人物设定生成完成，长度: {len(characters)} 字符")
        
        # 保存人物设定
        if self.config['output_settings']['generate_character_profiles']:
            char_path = os.path.join(
                self.config['output_settings']['save_path'],
                'characters.md'
            )
            with open(char_path, 'w', encoding='utf-8') as f:
                f.write(characters)
            logger.info(f"人物设定已保存至: {char_path}")
                
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
        logger.info("开始生成小说内容...")
        system_prompt = prompts.get_system_prompt(self.config)
        content_prompt = prompts.get_content_prompt(self.config, outline, characters)
        
        # 分段生成内容
        sections = ['开篇', '发展', '高潮', '结局']
        content_parts = []
        
        for i, section in enumerate(sections, 1):
            logger.info(f"正在生成第{i}/4部分：{section}...")
            section_prompt = f"{content_prompt}\n\n当前需要生成的是故事的{section}部分。"
            section_content = self._call_ollama(system_prompt, section_prompt)
            content_parts.append(section_content)
            logger.info(f"{section}部分生成完成，长度: {len(section_content)} 字符")
            
            # 每生成一部分就保存一次，避免丢失内容
            title = self.config['novel_settings']['title']
            current_content = f"# {title}\n\n" + "\n\n".join(content_parts)
            temp_path = os.path.join(
                self.config['output_settings']['save_path'],
                f"{title}_temp.md"
            )
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(current_content)
            logger.debug(f"已保存临时文件: {temp_path}")
        
        # 生成完成后，保存最终版本
        title = self.config['novel_settings']['title']
        full_content = f"# {title}\n\n" + "\n\n".join(content_parts)
        content_path = os.path.join(
            self.config['output_settings']['save_path'],
            f"{title}.md"
        )
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        logger.success(f"小说内容生成完成！总长度: {len(full_content)} 字符")
        logger.info(f"最终文件已保存至: {content_path}")
            
        return full_content
        
    def generate(self):
        """
        生成完整的小说
        """
        logger.info(f"开始生成小说：{self.config['novel_settings']['title']}")
        logger.info(f"类型：{self.config['novel_settings']['genre']}")
        logger.info(f"主题：{self.config['novel_settings']['theme']}")
        logger.info(f"目标字数：{self.config['novel_settings']['word_count']}")
        
        # 生成大纲
        outline = self.generate_outline()
        
        # 生成人物设定
        characters = self.generate_characters()
        
        # 生成小说内容
        self.generate_content(outline, characters)
        
        logger.success("小说生成完成！") 