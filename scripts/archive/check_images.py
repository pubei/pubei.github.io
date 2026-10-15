import os
import re

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')

def find_image_references(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    bg_pattern = r'background(?:-image)?\s*:\s*url\(["\']?([^"\')]+)["\']?\)'
    images = re.findall(img_pattern, content) + re.findall(bg_pattern, content)
    return images

missing_images = {}
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        images = find_image_references(filename)
        for img_path in images:
            if any(img_path.lower().endswith(ext) for ext in image_extensions):
                full_path = os.path.join('.', img_path)
                if not os.path.exists(full_path):
                    if filename not in missing_images:
                        missing_images[filename] = []
                    missing_images[filename].append(img_path)

if missing_images:
    for page, images in missing_images.items():
        print(f"⚠️ {page}:")
        for img in images:
            print(f"   - {img}")
        print()
    print(f"共 {sum(len(v) for v in missing_images.values())} 张图片缺失")
else:
    print("✅ 所有页面的图片都能正常显示")