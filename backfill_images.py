#!/usr/bin/env python3
"""
回填脚本 - 为所有现有新闻重新生成 SVG 图片
迁移所有 .jpg 引用到 .svg，确保图片稳定显示
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 导入 generate_news 模块中的 SVG 生成函数
sys.path.insert(0, BASE_DIR)
import generate_news as gn


def categorize_by_title(title):
    """根据标题关键词推断分类"""
    title_lower = title.lower()
    if any(k in title for k in ["全屋", "定制", "家居"]):
        return "全屋定制"
    if any(k in title for k in ["设计", "装修", "风格", "装饰", "色彩", "空间"]):
        return "装修设计"
    if any(k in title for k in ["公司", "项目", "交付", "团队", "培训", "订单", "案例"]):
        return "公司动态"
    if any(k in title for k in ["行业", "趋势", "标准", "材料", "政策", "资讯", "市场"]):
        return "行业资讯"
    return "装修设计"


def main():
    # 1. 读取 news-data.json
    data_path = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        news_data = json.load(f)

    print(f"📋 读取到 {len(news_data)} 条新闻记录")

    # 2. 为每条新闻生成 SVG 图片
    updated_data = []
    for item in news_data:
        news_id = item['id']
        title = item['title']
        category = item.get('category', '') or categorize_by_title(title)
        old_image = item.get('image', '')

        print(f"\n🔄 处理: [{news_id}] {title[:30]}...")
        print(f"    分类: {category}")
        print(f"    旧图片: {old_image}")

        # 生成 SVG
        new_image_path = gn.save_news_image(title, category, news_id)
        print(f"    新图片: {new_image_path}")

        # 更新记录
        item['image'] = new_image_path
        updated_data.append(item)

        # 删除旧 jpg 文件（如果是从旧 API 下载的）
        if old_image and old_image != new_image_path:
            old_path = os.path.join(BASE_DIR, old_image)
            if os.path.exists(old_path) and old_path.endswith('.jpg'):
                # 检查文件大小，只有较小的（可能是占位图）才删除
                file_size = os.path.getsize(old_path)
                if file_size < 5000:  # 小于5KB的可能是无效文件
                    os.remove(old_path)
                    print(f"    🗑 已删除旧文件: {old_image} ({file_size}字节)")
                else:
                    print(f"    ℹ 保留旧文件: {old_image} ({file_size}字节)")

    # 3. 更新 news-data.json
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ news-data.json 已更新 ({len(updated_data)} 条记录)")

    # 4. 更新 news.html 中的图片引用
    news_html_path = os.path.join(BASE_DIR, 'news.html')
    with open(news_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 构建 ID -> 新图片路径的映射
    id_to_image = {}
    for item in updated_data:
        id_to_image[item['id']] = item['image']

    # 替换 news.html 中的图片引用
    # 匹配 <img src="assets/images/news/xxx.jpg" alt="..."> 模式
    for news_id, new_path in id_to_image.items():
        # 查找与该 ID 关联的所有图片引用
        # 通过 news-id href 或 alt 中的标题关联
        old_patterns = set()
        for item in news_data:
            if item['id'] == news_id:
                old_img = item.get('image', '')
                if old_img and old_img != new_path:
                    old_patterns.add(old_img)

        for old_path in old_patterns:
            html_content = html_content.replace(old_path, new_path)
            print(f"  🔁 news.html: {old_path} → {new_path}")

    # 也处理 news_fix_* 系列的引用
    # 用标题来匹配
    title_to_image = {}
    for item in updated_data:
        title_to_image[item['title']] = item['image']

    # 清理 news_fix_* 和其他无效引用
    html_content = re.sub(
        r'<img\s+src="assets/images/news/[^"]*news_fix[^"]*\.jpg"',
        lambda m: replace_fix_image(m, title_to_image, updated_data),
        html_content
    )

    with open(news_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n✓ news.html 已更新")

    # 5. 验证
    print("\n" + "=" * 60)
    print("✅ 回填完成！")
    print(f"   - 处理新闻: {len(updated_data)} 条")
    print(f"   - 图片目录: assets/images/news/")
    print(f"   - 图片格式: 全部为 SVG（零外部依赖）")

    # 验证文件
    svg_count = sum(1 for f in os.listdir(os.path.join(BASE_DIR, 'assets', 'images', 'news')) if f.endswith('.svg'))
    print(f"   - SVG 文件数: {svg_count}")

    # 检查 news.html 中是否还有 .jpg 新闻图片引用
    jpg_refs = re.findall(r'src="(assets/images/news/[^"]+\.jpg)"', html_content)
    if jpg_refs:
        print(f"   ⚠ news.html 中仍有 {len(jpg_refs)} 个 .jpg 引用:")
        for ref in set(jpg_refs):
            print(f"      - {ref}")
    else:
        print(f"   ✓ news.html 中所有新闻图片均为 SVG")


def replace_fix_image(match, title_to_image, updated_data):
    """替换 news_fix_ 系列图片"""
    # 从 alt 属性获取标题
    full_match = match.group(0)
    alt_match = re.search(r'alt="([^"]*)"', full_match)
    if alt_match:
        alt_text = alt_match.group(1)
        # 尝试匹配标题
        for title, img_path in title_to_image.items():
            if alt_text in title or title in alt_text:
                return full_match.replace(full_match.split('src="')[1].split('"')[0], img_path)
    # 返回默认 SVG
    return full_match


if __name__ == '__main__':
    main()
