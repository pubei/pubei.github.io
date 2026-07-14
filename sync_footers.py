#!/usr/bin/env python3
"""批量更新所有HTML页面的页脚，使其与首页完全一致"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')

# 读取首页页脚
with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_content = f.read()

# 提取首页的完整footer
footer_match = re.search(r'(<footer class="footer">.*?</footer>)', index_content, re.DOTALL)
if not footer_match:
    print("Error: Could not extract footer from index.html")
    exit(1)

index_footer = footer_match.group(1)

# 获取所有HTML文件
html_files = []
for f in os.listdir(BASE_DIR):
    if f.endswith('.html') and f != 'index.html':
        html_files.append(os.path.join(BASE_DIR, f))

print(f"Found {len(html_files)} HTML files to update")

updated = 0
for filepath in sorted(html_files):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换footer
    new_content = re.sub(
        r'<footer class="footer">.*?</footer>',
        index_footer,
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated: {filename}")
        updated += 1
    else:
        print(f"  No change: {filename}")

print(f"\nDone! Updated {updated}/{len(html_files)} files")
