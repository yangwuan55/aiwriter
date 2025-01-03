import os
from loguru import logger

def get_unique_filename(base_path: str) -> str:
    """
    获取不重复的文件路径
    
    Args:
        base_path: 基础文件路径
        
    Returns:
        不重复的文件路径
    """
    if not os.path.exists(base_path):
        return base_path
        
    # 分解文件路径
    directory = os.path.dirname(base_path)
    filename = os.path.basename(base_path)
    name, ext = os.path.splitext(filename)
    
    # 查找当前目录下所有相似的文件
    counter = 1
    while True:
        new_path = os.path.join(directory, f"{name}_{counter}{ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def ensure_dir(path: str):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
    """
    os.makedirs(path, exist_ok=True)
    
def save_content(content: str, filepath: str):
    """
    保存内容到文件
    
    Args:
        content: 要保存的内容
        filepath: 文件路径
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.success(f"内容已保存至: {filepath}")
    except Exception as e:
        logger.error(f"保存文件失败: {filepath}, 错误: {str(e)}")
        raise

def delete_file(filepath: str):
    """
    删除文件
    
    Args:
        filepath: 文件路径
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.debug(f"已删除文件: {filepath}")
    except Exception as e:
        logger.warning(f"删除文件失败: {filepath}, 错误: {str(e)}") 