import os
from typing import Dict, Any, List
from loguru import logger
from ..utils.api_utils import OllamaAPI
from ..utils.file_utils import ensure_dir, save_content, delete_file
from .writer import NovelWriter

class NovelGenerator:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化小说生成器
        
        Args:
            config: 配置字典
        """
        self.config = config
        
        # 设置输出目录
        self.output_dir = self.config['output_settings']['output_dir']
        self.novels_dir = os.path.join(self.output_dir, 'novels')  # 存放所有小说的目录
        
        # 创建输出目录
        ensure_dir(self.output_dir)
        ensure_dir(self.novels_dir)
        logger.info(f"输出根目录: {self.output_dir}")
        logger.info(f"小说存放目录: {self.novels_dir}")
        
        # 更新配置中的路径
        self.config['output_settings']['save_path'] = self.novels_dir
        
        # 初始化API客户端
        self.api_client = OllamaAPI(config)
        
        # 初始化写作器
        self.writer = NovelWriter(config, self.api_client)
        
    def generate(self):
        """生成完整的小说"""
        logger.info(f"开始生成小说：{self.config['novel_settings']['title']}")
        logger.info(f"类型：{self.config['novel_settings']['genre']}")
        logger.info(f"主题：{self.config['novel_settings']['theme']}")
        logger.info(f"目标字数：{self.config['novel_settings']['word_count']}")
        
        try:
            # 记录所有生成的小说及其评分
            novels = []
            
            # 生成指定数量的小说
            novel_count = self.config['output_settings'].get('novel_count', 1)
            logger.info(f"计划生成{novel_count}篇小说...")
            
            for i in range(novel_count):
                logger.info(f"开始生成第{i+1}/{novel_count}篇小说...")
                
                # 为当前小说创建单独的文件夹
                current_novel_dir = os.path.join(
                    self.config['output_settings']['save_path'],
                    f'{self.config["novel_settings"]["title"]}_{i+1}'
                )
                ensure_dir(current_novel_dir)
                logger.info(f"创建小说目录: {current_novel_dir}")
                
                # 临时修改save_path为当前小说的目录
                original_save_path = self.config['output_settings']['save_path']
                self.config['output_settings']['save_path'] = current_novel_dir
                
                # 生成大纲
                outline = self.writer.generate_outline()
                
                # 生成人物设定，传入大纲
                characters = self.writer.generate_characters(outline)
                
                # 生成小说内容
                content = self.writer.generate_content(outline, characters)
                
                # 最终重写（包含去重和评分）
                content, score = self.writer.final_rewrite(outline, characters, content)
                
                # 保存小说内容
                novel_path = os.path.join(current_novel_dir, f'{self.config["novel_settings"]["title"]}.md')
                save_content(content, novel_path)
                
                # 记录小说信息
                novels.append({
                    'dir': current_novel_dir,
                    'path': novel_path,
                    'score': score,
                    'content': content
                })
                
                logger.info(f"第{i+1}篇小说生成完成，评分：{score}")
                
                # 删除临时文件
                temp_file = os.path.join(current_novel_dir, f'{self.config["novel_settings"]["title"]}_temp.md')
                delete_file(temp_file)
                
                # 恢复原始save_path
                self.config['output_settings']['save_path'] = original_save_path
            
            # 找出评分最高的小说
            if novels:
                best_novel = max(novels, key=lambda x: x['score'])
                logger.info(f"评分最高的小说：{best_novel['score']}分")
                
                # 将最佳小说拷贝到输出目录根目录
                best_novel_path = os.path.join(
                    self.config['output_settings']['save_path'],
                    f'{self.config["novel_settings"]["title"]}_best.md'
                )
                save_content(best_novel['content'], best_novel_path)
                logger.success(f"已将最佳小说保存至: {best_novel_path}")
            
            logger.success(f"所有小说生成完成！共生成{len(novels)}篇")
            
        except Exception as e:
            logger.error(f"生成过程中发生错误: {str(e)}")
            logger.exception("详细错误信息：") 