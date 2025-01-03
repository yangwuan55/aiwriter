import yaml
from typing import Dict, Any
from loguru import logger

def load_config(config_path: str) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 验证必要的配置项
        required_sections = ['ai_settings', 'author_profile', 'novel_settings', 'output_settings']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"配置文件缺少必要的配置项：{section}")
                
        return config
        
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        raise 