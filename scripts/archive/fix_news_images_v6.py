import os
import json
import re

NEWS_FILE = 'news.html'
NEWS_DATA_FILE = 'assets/data/news-data.json'

INTERIOR_IMAGES = [
    "https://picsum.photos/id/1048/800/450",
    "https://picsum.photos/id/1049/800/450",
    "https://picsum.photos/id/1050/800/450",
    "https://picsum.photos/id/1051/800/450",
    "https://picsum.photos/id/1052/800/450",
    "https://picsum.photos/id/1053/800/450",
    "https://picsum.photos/id/1054/800/450",
    "https://picsum.photos/id/1055/800/450",
    "https://picsum.photos/id/1067/800/450",
    "https://picsum.photos/id/1068/800/450",
    "https://picsum.photos/id/1074/800/450",
    "https://picsum.photos/id/1077/800/450",
    "https://picsum.photos/id/1082/800/450",
    "https://picsum.photos/id/1084/800/450",
    "https://picsum.photos/id/1086/800/450"
]

# 更新news-data.json
with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for i, item in enumerate(data):
    old_image = item['image']
    new_image = INTERIOR_IMAGES[i % len(INTERIOR_IMAGES)]
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