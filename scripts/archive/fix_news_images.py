import os
import json

NEWS_FILE = 'news.html'
NEWS_DATA_FILE = 'assets/data/news-data.json'

# 替换内部API地址为公开图片服务
def fix_image_url(url):
    if 'trae-api-cn.mchost.guru' in url:
        # 提取prompt参数
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        prompt = params.get('prompt', ['default'])[0]
        return f"https://picsum.photos/seed/{prompt}/800/450"
    return url

# 更新news-data.json
with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    old_image = item['image']
    new_image = fix_image_url(old_image)
    if old_image != new_image:
        item['image'] = new_image
        updated_count += 1

with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} image URLs in news-data.json")

# 更新news.html
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

import re
old_pattern = r'https://trae-api-cn\.mchost\.guru/api/ide/v1/text_to_image\?prompt=([^&]+)&image_size=landscape_16_9'

def replace_image(match):
    prompt = match.group(1)
    return f"https://picsum.photos/seed/{prompt}/800/450"

new_content = re.sub(old_pattern, replace_image, content)

with open(NEWS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

updated_html = len(re.findall(old_pattern, content))
print(f"Updated {updated_html} image URLs in news.html")