#!/usr/bin/env python3
"""
批量更新现有news.html中的新闻图片，让图片与新闻标题内容相关
根据每条新闻的标题内容匹配合适的主题图片
"""

import os
import re
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_FILE = os.path.join(BASE_DIR, 'news.html')

IMAGE_API_BASE = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"


def build_image_url(prompt, size="landscape_4_3"):
    """构建图片生成URL"""
    return f"{IMAGE_API_BASE}?prompt={quote(prompt)}&image_size={size}"


# 新闻标题与图片prompt的映射关系
# 根据新闻标题关键词匹配对应的图片
TITLE_IMAGE_MAP = [
    # 全屋定制类
    ("全屋定制工艺升级", "custom furniture workshop with precision cutting machine, craftsman working on wood panels, modern manufacturing technology, professional craftsmanship"),
    ("小户型全屋定制", "small apartment with space-saving custom furniture, multi-functional storage solutions, built-in wardrobes and foldable desk, compact modern design"),
    ("全屋定制预算", "home renovation budget planning, cost breakdown chart, calculator and blueprint, financial planning for interior design"),
    ("书房全屋定制", "modern home office study room with custom bookshelf, built-in desk, tatami area, organized workspace with natural light"),
    ("全屋定制订单", "professional design team meeting in modern office, signing contract with client, business handshake, happy customer service"),
    ("新增.*订单", "professional design team meeting in modern office, signing contract with client, business handshake, happy customer service"),

    # 装修设计类
    ("装修流行趋势", "interior design style trends comparison, five different room styles showcase, modern minimalist luxury Nordic Chinese wabi-sabi"),
    ("装修避坑", "home renovation checklist, ten important tips for decoration, warning signs and notes, construction site inspection"),
    ("室内设计培训", "interior design training class, professional designers learning new skills, design workshop with presentation, modern education setting"),

    # 公司动态类
    ("智能家居项目", "smart home control panel on wall, modern living room with automation system, smartphone controlling home devices, futuristic interior"),
    ("优秀室内设计企业", "interior design award ceremony, golden award trophy, elegant stage with spotlight, professional recognition event"),
    ("荣获.*设计", "interior design award ceremony, golden award trophy, elegant stage with spotlight, professional recognition event"),

    # 行业资讯类
    ("环保材料", "eco friendly building materials certification, green environmental protection standard, sustainable wood panels with leaf symbol"),
    ("环保装修材料", "eco friendly renovation materials display, zero formaldehyde boards, water-based paint cans, natural stone samples, green building products"),
    ("环保板材", "eco friendly wood panels stacked in warehouse, E0 grade environmental protection boards, green leaf symbol on packaging, sustainable materials"),
]


def get_image_prompt_for_title(title):
    """根据新闻标题获取对应的图片prompt"""
    for pattern, prompt in TITLE_IMAGE_MAP:
        if re.search(pattern, title):
            return prompt
    # 默认图片：现代室内设计
    return "modern interior design living room with elegant furniture, professional home decoration, warm lighting"


def update_news_images():
    """更新news.html中所有新闻卡片的图片"""
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配新闻卡片中的图片标签
    # 格式: <img src="..." alt="标题">
    pattern = r'<img src="assets/images/news-bg-\d+\.svg" alt="([^"]+)">'

    def replace_image(match):
        title = match.group(1)
        # 获取对应的图片prompt
        image_prompt = get_image_prompt_for_title(title)
        # 生成图片URL
        image_url = build_image_url(image_prompt)
        return f'<img src="{image_url}" alt="{title}">'

    # 替换所有匹配的图片
    new_content = re.sub(pattern, replace_image, content)

    # 统计替换数量
    original_count = len(re.findall(pattern, content))
    print(f"共更新 {original_count} 条新闻的图片")

    # 写回文件
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("所有新闻图片已更新为与内容相关的主题图片")


if __name__ == '__main__':
    print("=== 开始更新现有新闻图片 ===")
    update_news_images()
    print("=== 更新完成 ===")
