#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from loguru import logger
from novel_generator.generator import NovelGenerator
from novel_generator.config import load_config

@click.command()
@click.option('--config', '-c', required=True, help='配置文件路径')
@click.option('--output', '-o', default='./output', help='输出目录')
def main(config: str, output: str):
    """知乎盐选小说生成器"""
    try:
        # 加载配置
        config_data = load_config(config)
        
        # 更新输出路径
        config_data['output_settings']['save_path'] = output
        
        # 初始化生成器
        generator = NovelGenerator(config_data)
        
        # 生成小说
        generator.generate()
        
        logger.success(f"小说生成完成！输出目录：{output}")
        
    except Exception as e:
        logger.error(f"生成过程中发生错误: {str(e)}")
        raise

if __name__ == '__main__':
    main() 