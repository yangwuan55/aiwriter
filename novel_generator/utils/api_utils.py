import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger
from typing import Dict, Any

class OllamaAPI:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化Ollama API客户端
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.base_url = f"{config['ai_settings']['host']}:{config['ai_settings']['port']}"
        
        # 创建带有重试机制的会话
        self.session = requests.Session()
        retries = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        logger.debug("已配置重试机制：最大重试3次，间隔1秒")
        
    def generate(self, system_prompt: str, user_prompt: str = "") -> str:
        """
        调用Ollama API生成内容
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词（可选）
            
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