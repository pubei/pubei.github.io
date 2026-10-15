#!/usr/bin/env python3
"""
将新闻列表图片从本地 SVG 切换为 trae-api-cn 真实装修设计/全屋定制图片
与首页图片方案保持一致（浏览器带认证可正常加载）

参考首页 CSS 中的 prompt 风格：
  - modern luxury home interior design with elegant living room
  - modern custom furniture design living room wardrobe kitchen cabinet
  - bathroom remodel modern design clean elegant home improvement

为每条新闻根据标题关键词生成专属的真实场景英文 prompt
同时更新 news-data.json（详情页数据源）和 news.html（列表页 img src）
"""

import os
import json
import re
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DATA_FILE = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')
NEWS_HTML_FILE = os.path.join(BASE_DIR, 'news.html')

# 图片生成 API 基础 URL（与首页 CSS 中使用的一致）
IMAGE_API_BASE = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
IMAGE_SIZE = "landscape_4_3"  # 与首页案例卡片一致，横向 4:3 适合新闻卡片


def build_image_url(prompt: str) -> str:
    """构造完整的图片生成 API URL（prompt 需 URL 编码）"""
    return f"{IMAGE_API_BASE}?prompt={quote(prompt)}&image_size={IMAGE_SIZE}"


# ============================================================================
# 标题关键词 -> 真实场景英文 prompt 映射
# 参考首页 prompt 风格：真实室内设计摄影，专业、温暖、现代
# ============================================================================
def prompt_for_news(title: str, category: str) -> str:
    """根据新闻标题和分类生成专属的真实装修场景英文 prompt"""
    t = title

    # ===== 全屋定制 - 具体房间类型 =====
    if '客厅' in t and ('布局' in t or '装修' in t):
        # 客厅布局方案
        return ("modern luxury living room interior design with elegant sofa "
                "TV wall unit soft lighting warm atmosphere minimalist style "
                "professional photography")

    if '儿童房' in t:
        # 儿童房全屋定制
        return ("colorful children bedroom with custom safe furniture rounded edges "
                "eco-friendly materials wardrobe and study desk warm playful design "
                "professional interior photography")

    if '厨房' in t:
        # 厨房全屋定制
        return ("modern custom kitchen with elegant cabinets marble countertop "
                "kitchen island with storage integrated appliances professional "
                "interior design photography warm lighting")

    if '书房' in t:
        # 书房全屋定制
        return ("modern home office study room with custom built-in bookshelf "
                "wooden desk tatami area organized workspace natural light "
                "professional interior design photography")

    if '卧室' in t or '衣柜' in t:
        # 卧室/衣柜定制
        return ("luxury bedroom with custom walk-in wardrobe integrated vanity "
                "table soft warm lighting modern minimalist design cozy atmosphere "
                "professional interior photography")

    if '小户型' in t:
        # 小户型扩容
        return ("small apartment with space-saving custom furniture multi-functional "
                "storage solutions built-in wardrobes foldable desk compact modern "
                "minimalist interior design photography")

    if '风格' in t and ('指南' in t or '解析' in t):
        # 全屋定制风格指南
        return ("interior design style guide showing multiple room styles modern "
                "minimalist Nordic new Chinese luxury style comparison design mood "
                "board professional photography")

    # ===== 全屋定制 - 工艺/材料/流程 =====
    if '材料升级' in t or '环保板材' in t:
        # 环保板材升级
        return ("eco friendly wood panels stacked in warehouse E0 grade environmental "
                "protection boards green leaf symbol on packaging sustainable materials "
                "professional photography")

    if '工艺升级' in t or '工艺' in t:
        # 工艺升级
        return ("custom furniture workshop with precision cutting machine craftsman "
                "working on wood panels modern manufacturing technology professional "
                "craftsmanship photography")

    if '安装' in t or '流程' in t:
        # 安装流程
        return ("custom furniture installation process workers installing wardrobe "
                "in modern bedroom professional installation team tools and materials "
                "professional photography")

    # ===== 智能家居 =====
    if '智能家居' in t and '融合' in t:
        # 全屋定制 + 智能家居融合
        return ("smart home integration with custom furniture voice control system "
                "automated wardrobe with LED lighting modern technology interior design "
                "professional photography")

    if '智能家居项目' in t or '锦绣花园' in t:
        # 智能家居项目交付
        return ("smart home control panel on wall modern living room with automation "
                "system smartphone controlling home devices futuristic interior design "
                "professional photography")

    # ===== 公司动态 =====
    if ('认证' in t or '荣获' in t) and '品质' in t:
        # 行业品质服务认证
        return ("quality service certification award ceremony golden trophy on stage "
                "certificate with seal professional award presentation modern elegant "
                "event photography")

    if '优秀室内设计企业' in t:
        # 优秀室内设计企业
        return ("interior design award ceremony golden award trophy elegant stage "
                "with spotlight professional recognition event modern luxury interior "
                "design company showcase")

    if '培训' in t or '学习' in t or '设计师团队' in t:
        # 设计师培训
        return ("interior designers attending training seminar professional workshop "
                "design education group learning in modern classroom design studio with "
                "presentation professional photography")

    if '订单' in t and ('新增' in t or '签约' in t):
        # 订单签约
        return ("professional design team meeting in modern office signing contract "
                "with client business handshake happy customer service modern interior "
                "design company photography")

    # ===== 行业资讯 =====
    if '避坑' in t or '注意事项' in t:
        # 避坑指南
        return ("home renovation checklist ten important tips for decoration warning "
                "signs and notes construction site inspection professional engineer "
                "with clipboard professional photography")

    if '趋势' in t and ('风格' in t or '流行' in t):
        # 流行趋势
        return ("interior design style trends comparison five different room styles "
                "showcase modern minimalist luxury Nordic Chinese wabi-sabi professional "
                "photography mood board")

    if '环保材料' in t or '环保' in t:
        # 环保材料
        return ("eco friendly renovation materials display zero formaldehyde boards "
                "water-based paint cans natural stone samples green building products "
                "sustainable interior design photography")

    if '预算' in t:
        # 预算计算
        return ("home renovation budget planning cost breakdown chart calculator and "
                "blueprint financial planning for interior design modern desk with "
                "documents and coins professional photography")

    # ===== 备选：按分类默认 =====
    if category == '全屋定制':
        return ("modern custom furniture design living room wardrobe kitchen cabinet "
                "interior design professional photography elegant warm atmosphere")

    if category == '装修设计':
        return ("modern luxury home interior design with elegant living room and "
                "minimalist style soft lighting warm atmosphere professional photography")

    if category == '公司动态':
        return ("professional interior design company team meeting modern office "
                "with design samples and blueprints warm atmosphere corporate photography")

    if category == '行业资讯':
        return ("modern home renovation construction site building materials professional "
                "work interior design industry trends professional photography")

    # 最终默认
    return ("modern luxury home interior design with elegant living room minimalist "
            "style soft lighting warm atmosphere professional photography")


# ============================================================================
# 主流程
# ============================================================================
def main():
    # 1. 读取 news-data.json
    with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
        news_data = json.load(f)

    print(f"📋 读取到 {len(news_data)} 条新闻记录")
    print(f"=" * 70)

    # 2. 为每条新闻构造真实图片 URL
    id_to_url = {}
    for item in news_data:
        news_id = str(item['id'])
        title = item['title']
        category = item.get('category', '装修设计')

        prompt = prompt_for_news(title, category)
        image_url = build_image_url(prompt)

        id_to_url[news_id] = image_url
        item['image'] = image_url

        print(f"✓ [{category}] {news_id}")
        print(f"   标题: {title[:40]}")
        print(f"   prompt: {prompt[:80]}...")

    # 3. 写回 news-data.json
    with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ news-data.json 已更新（{len(news_data)} 条记录的 image 字段）")

    # 4. 同步更新 news.html 中的 img src
    with open(NEWS_HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 统计替换前的 SVG 引用数
    svg_before = len(re.findall(r'src="assets/images/news/news_[^"]*\.svg"', html_content))
    print(f"\n📊 news.html 中替换前共有 {svg_before} 个本地 SVG 图片引用")

    # 替换策略：
    # news.html 中 img 标签的 alt 属性通常包含新闻标题
    # 通过 alt 文本匹配到对应的 news_id，再替换 src
    # 同时按 news_id 直接替换 src="...news_<id>.svg"

    replace_count = 0
    for news_id, image_url in id_to_url.items():
        # 直接按文件名替换 src（最可靠）
        old_patterns = [
            f'src="assets/images/news/news_{news_id}.svg"',
        ]
        for old in old_patterns:
            if old in html_content:
                html_content = html_content.replace(old, f'src="{image_url}"')
                replace_count += 1

    print(f"✅ news.html 中已替换 {replace_count} 个 img src")

    # 检查是否有遗漏的 SVG 引用
    svg_after = len(re.findall(r'src="assets/images/news/news_[^"]*\.svg"', html_content))
    if svg_after > 0:
        print(f"⚠ news.html 中仍有 {svg_after} 个本地 SVG 引用未替换:")
        remaining = re.findall(r'src="(assets/images/news/news_[^"]*\.svg)"', html_content)
        for ref in set(remaining):
            print(f"   - {ref}")

    # 5. 写回 news.html
    with open(NEWS_HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n" + "=" * 70)
    print(f"✅ 完成！所有新闻图片已切换为真实装修设计/全屋定制图片")
    print(f"   - 图片源: {IMAGE_API_BASE}")
    print(f"   - 尺寸: {IMAGE_SIZE}")
    print(f"   - 与首页背景图方案一致（浏览器带认证可正常加载）")


if __name__ == '__main__':
    main()
