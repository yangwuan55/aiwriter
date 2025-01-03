"""
知乎盐选小说生成器
"""

from .core.generator import NovelGenerator
from .core.writer import NovelWriter
from .utils.api_utils import OllamaAPI
from .utils.file_utils import ensure_dir, save_content, delete_file, get_unique_filename

__all__ = [
    'NovelGenerator',
    'NovelWriter',
    'OllamaAPI',
    'ensure_dir',
    'save_content',
    'delete_file',
    'get_unique_filename'
]

__version__ = "0.1.0" 