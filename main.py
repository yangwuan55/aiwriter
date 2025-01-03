#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import yaml
from loguru import logger
from novel_generator import NovelGenerator

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='小说生成器')
    parser.add_argument('-c', '--config', required=True, help='配置文件路径')
    args = parser.parse_args()
    
    try:
        # 读取配置文件
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 初始化生成器
        generator = NovelGenerator(config)
        
        # 生成小说
        generator.generate()
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        logger.exception("详细错误信息：")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 