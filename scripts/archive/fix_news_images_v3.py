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
    return f"https://source.unsplash.com/random/800x450/{keyword1},{keyword2}"

# 更新news-data.json
with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    old_image = item['image']
    new_image = generate_interior_image_url(item['id'])
    if old_image != new_image:
        item['image'] = new_image
        updated_count += 1

with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} image URLs in news-data.json")

# 更新news.html - 修复图片URL格式
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复错误的img标签格式
# 匹配: <img src="https://source.unsplash.com/random/800x450/?xxx alt="xxx">
# 替换为: <img src="https://source.unsplash.com/random/800x450/xxx" alt="xxx">
old_pattern = r'<img src="https://source\.unsplash\.com/random/800x450/\?([^"\s]+) alt="([^"]+)">'

def replace_image(match):
    keywords = match.group(1)
    alt = match.group(2)
    return f'<img src="https://source.unsplash.com/random/800x450/{keywords}" alt="{alt}">'

new_content = re.sub(old_pattern, replace_image, content)

with open(NEWS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

updated_count = len(re.findall(old_pattern, content))
print(f"Fixed {updated_count} image URLs in news.html")