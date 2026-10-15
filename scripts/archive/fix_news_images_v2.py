import os
import json
import random
import re

NEWS_FILE = 'news.html'
NEWS_DATA_FILE = 'assets/data/news-data.json'

INTERIOR_KEYWORDS = [
    "interior+design", "home+renovation", "custom+furniture", 
    "modern+living+room", "kitchen+cabinets", "bedroom+wardrobe",
    "home+interior", "luxury+home", "minimalist+design",
    "house+remodeling", "furniture+design", "home+decor",
    "smart+home", "eco+friendly+home", "showroom+design"
]

def generate_interior_image_url(seed=None):
    """生成与装修设计相关的图片URL"""
    if seed:
        random.seed(seed)
    keyword1 = random.choice(INTERIOR_KEYWORDS)
    keyword2 = random.choice([k for k in INTERIOR_KEYWORDS if k != keyword1])
    return f"https://source.unsplash.com/random/800x450/?{keyword1},{keyword2}"

# 更新news-data.json
with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    old_image = item['image']
    # 使用新闻ID作为种子确保图片稳定
    new_image = generate_interior_image_url(item['id'])
    if old_image != new_image:
        item['image'] = new_image
        updated_count += 1

with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} image URLs in news-data.json")

# 更新news.html
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有非Unsplash的图片URL
old_pattern = r'https://[^/]+/[^/]+/[^/]+/[^\s>]+'

def replace_image(match):
    url = match.group(0)
    if 'unsplash.com' in url:
        return url
    # 生成新的装修相关图片URL
    return generate_interior_image_url(url)

new_content = re.sub(old_pattern, replace_image, content)

with open(NEWS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated news.html images")