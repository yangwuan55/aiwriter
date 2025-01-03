#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from loguru import logger
from novel_generator.generator import NovelGenerator
from novel_generator.config import load_config
from novel_generator import prompts
import os
import requests

def rate_novel(novel_path: str, config: dict) -> str:
    """使用LLM对小说进行评分并返回评分结果。"""
    try:
        # 读取小说内容
        logger.info(f"正在读取小说文件：{novel_path}")
        with open(novel_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.debug(f"小说内容读取成功，长度：{len(content)}字符")
        
        # 将小说内容分成多个部分
        max_content_length = 2000  # 每部分最大字符数
        parts = []
        current_part = ""
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_part) + len(paragraph) > max_content_length:
                parts.append(current_part)
                current_part = paragraph
            else:
                current_part += "\n\n" + paragraph if current_part else paragraph
        if current_part:
            parts.append(current_part)
        
        logger.info(f"小说内容已分成{len(parts)}个部分进行评分")
        
        # 对每个部分进行评分
        all_ratings = []
        for i, part in enumerate(parts, 1):
            logger.info(f"正在评分第{i}/{len(parts)}部分...")
            
            # 获取评分提示词
            system_prompt = prompts.get_rating_prompt()
            user_prompt = prompts.get_rating_user_prompt(part)
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            logger.debug(f"提示词构建完成，长度：{len(full_prompt)}字符")
            
            # 准备请求数据
            data = {
                "model": config['ai_settings']['model'],
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": config['ai_settings']['temperature'],
                    "num_ctx": config['ai_settings']['context_size'],
                    "num_predict": config['ai_settings']['num_predict']
                }
            }
            
            # 发送请求
            base_url = f"{config['ai_settings']['host']}:{config['ai_settings']['port']}"
            logger.info(f"正在发送请求到：{base_url}")
            response = requests.post(
                f"{base_url}/api/generate",
                json=data,
                timeout=300
            )
            response.raise_for_status()
            
            # 获取评分结果
            result = response.json()
            rating = result.get('response', '')
            logger.info(f"第{i}部分评分完成，长度：{len(rating)}字符")
            all_ratings.append(rating)
        
        # 合并所有评分结果
        final_rating = "# 小说评分\n\n"
        for i, rating in enumerate(all_ratings, 1):
            final_rating += f"## 第{i}部分评分\n\n{rating}\n\n---\n\n"
        
        logger.success("小说评分完成")
        return final_rating
        
    except Exception as e:
        logger.error(f"评分过程中发生错误: {str(e)}")
        logger.exception("详细错误信息：")
        return "评分失败，请检查错误日志"

@click.command()
@click.option('--config', '-c', required=True, help='配置文件路径')
@click.option('--output', '-o', default='./output', help='输出目录')
def main(config: str, output: str):
    """知乎盐选小说生成器"""
    try:
        # 加载配置
        config_data = load_config(config)
        
        # 获取要生成的小说数量
        novel_count = config_data['output_settings'].get('novel_count', 1)
        
        for i in range(novel_count):
            # 为每部小说创建单独的输出目录
            novel_output = os.path.join(output, f'novel_{i+1}')
            os.makedirs(novel_output, exist_ok=True)
            
            # 更新输出路径
            config_data['output_settings']['save_path'] = novel_output
            
            # 初始化生成器
            generator = NovelGenerator(config_data)
            
            # 生成小说
            logger.info(f"开始生成第 {i+1}/{novel_count} 部小说...")
            generator.generate()
            logger.success(f"第 {i+1}/{novel_count} 部小说生成完成！输出目录：{novel_output}")

            # 对小说进行评分
            logger.info("开始对小说进行评分...")
            novel_file = os.path.join(novel_output, '数字记忆.md')
            rating = rate_novel(novel_file, config_data)
            
            # 将评分写入小说开头
            with open(novel_file, 'r+', encoding='utf-8') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(rating + '\n\n---\n\n' + content)
            logger.success("小说评分完成并已写入文件")

        logger.success(f"所有小说生成完成！总共生成了 {novel_count} 部小说，输出目录：{output}")
        
    except Exception as e:
        logger.error(f"生成过程中发生错误: {str(e)}")
        raise

if __name__ == '__main__':
    main() 