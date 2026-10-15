import os
import json
import random
import re

NEWS_FILE = 'news.html'
NEWS_DATA_FILE = 'assets/data/news-data.json'

INTERIOR_IMAGES = [
    "https://images.unsplash.com/photo-1521791136064-7986c292026c?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1514674116507-95ac68373442?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1524678714210-9917a6c619c2?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&h=450&fit=crop",
    "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&h=450&fit=crop"
]

def generate_interior_image_url(seed=None):
    """生成与装修设计相关的图片URL"""
    if seed:
        random.seed(seed)
    return random.choice(INTERIOR_IMAGES)

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

# 更新news.html
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换新闻卡片中的图片URL
old_pattern = r'<div class="news-card-image">\s*<img src="https://[^"]+" alt="([^"]+)">'

img_index = 0
def replace_image(match):
    global img_index
    alt = match.group(1)
    image_url = INTERIOR_IMAGES[img_index % len(INTERIOR_IMAGES)]
    img_index += 1
    return f'<div class="news-card-image">\n              <img src="{image_url}" alt="{alt}">'

new_content = re.sub(old_pattern, replace_image, content)

with open(NEWS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

updated_count = len(re.findall(old_pattern, content))
print(f"Fixed {updated_count} image URLs in news.html")