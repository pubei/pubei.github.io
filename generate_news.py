#!/usr/bin/env python3
"""
自动生成公司新闻 - 每天自动发布一条关于浦北装修设计/全屋定制的新闻或动态
"""

import os
import json
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_FILE = os.path.join(BASE_DIR, 'news.html')
NEWS_DATA_FILE = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')

# 装修相关图片关键词库
INTERIOR_KEYWORDS = [
    "interior+design", "home+renovation", "custom+furniture", 
    "modern+living+room", "kitchen+cabinets", "bedroom+wardrobe",
    "home+interior", "luxury+home", "minimalist+design",
    "house+remodeling", "furniture+design", "home+decor",
    "smart+home", "eco+friendly+home", "showroom+design"
]

# 新闻模板库 - 涵盖全屋定制、装修知识、公司动态、行业资讯等
NEWS_TEMPLATES = [
    {
        "category": "全屋定制",
        "title": "全屋定制趋势：{year}年最受欢迎的定制设计方案",
        "excerpt": "随着生活品质的提升，全屋定制已成为现代家庭装修的首选。本期为您解读{year}年最受欢迎的全屋定制设计方案，包括简约风格、轻奢风格和新中式风格...",
        "image_keywords": ["custom+furniture", "modern+interior"]
    },
    {
        "category": "装修知识",
        "title": "全屋定制避坑指南：业主必须了解的{year}个关键细节",
        "excerpt": "全屋定制虽然方便，但如果不注意细节，很容易踩坑。今天我们整理了全屋定制中最容易出问题的{year}个关键细节，帮助您避免装修遗憾...",
        "image_keywords": ["home+renovation+tips", "interior+design"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计本月新增{year}个全屋定制订单，服务再升级",
        "excerpt": "感谢客户们的信任与支持，本月我公司新增{year}个全屋定制订单。为更好地服务客户，我们升级了设计团队和施工工艺，为您提供更优质的全屋定制服务...",
        "image_keywords": ["design+studio", "professional+team"]
    },
    {
        "category": "行业资讯",
        "title": "环保材料新标准出台，全屋定制行业迎来新变革",
        "excerpt": "国家最新环保材料标准正式实施，对全屋定制行业提出更高要求。浦北装修设计积极响应新标准，全面升级环保材料供应链，为客户提供更健康的家居环境...",
        "image_keywords": ["eco+friendly+materials", "green+interior"]
    },
    {
        "category": "全屋定制",
        "title": "小户型全屋定制方案：{year}平米也能住出大空间感",
        "excerpt": "面积小不代表不能拥有高品质的生活。通过合理的全屋定制方案，即使是{year}平米的小户型也能打造出宽敞舒适的居住空间。本期分享几个实用的设计技巧...",
        "image_keywords": ["small+apartment+design", "space+saving"]
    },
    {
        "category": "装修知识",
        "title": "全屋定制板材怎么选？E0、E1、ENF级区别详解",
        "excerpt": "全屋定制中最重要的就是板材选择。E0级、E1级、ENF级板材有什么区别？哪种更适合家庭使用？本文为您详细解读各种环保等级板材的特点和适用场景...",
        "image_keywords": ["wood+panels", "furniture+materials"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制展厅焕新升级，欢迎参观体验",
        "excerpt": "为了给客户带来更好的体验，我公司全屋定制展厅已完成焕新升级。新展厅展示了多种风格的全屋定制实景效果，包括现代简约、轻奢、北欧等风格，欢迎莅临参观...",
        "image_keywords": ["showroom+interior", "furniture+display"]
    },
    {
        "category": "全屋定制",
        "title": "客厅全屋定制设计要点：打造温馨实用的家庭核心区",
        "excerpt": "客厅是家庭活动的核心区域，全屋定制客厅需要兼顾美观与实用。本文为您分享客厅全屋定制的设计要点，包括电视柜、收纳柜、展示柜的定制技巧...",
        "image_keywords": ["modern+living+room", "TV+cabinet"]
    },
    {
        "category": "行业资讯",
        "title": "智能家居与全屋定制融合，打造未来智慧家居生活",
        "excerpt": "随着智能家居技术的发展，全屋定制与智能系统的融合已成为新趋势。浦北装修设计推出智能全屋定制方案，将智能照明、安防监控、家电控制等融入定制家具中...",
        "image_keywords": ["smart+home", "modern+living+room"]
    },
    {
        "category": "全屋定制",
        "title": "卧室全屋定制攻略：衣柜+梳妆台+床头柜一体化设计",
        "excerpt": "卧室是休息的重要空间，全屋定制卧室需要考虑收纳和舒适度。本文为您分享卧室一体化定制方案，包括衣柜、梳妆台、床头柜的协调设计...",
        "image_keywords": ["modern+bedroom", "custom+wardrobe"]
    },
    {
        "category": "装修知识",
        "title": "全屋定制预算怎么算？2026年最新价格参考",
        "excerpt": "全屋定制的价格是很多业主关心的问题。本文为您详细分析2026年全屋定制的价格构成，包括板材费、五金件费、设计费、安装费等，帮助您合理规划装修预算...",
        "image_keywords": ["home+budget", "renovation+cost"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计荣获全屋定制品质服务认证",
        "excerpt": "经过严格评审，浦北装修设计公司荣获全屋定制品质服务认证。这一认证标志着我们在设计能力、施工质量、售后服务等方面均达到行业领先水平...",
        "image_keywords": ["award+certificate", "quality+service"]
    },
    {
        "category": "全屋定制",
        "title": "厨房全屋定制设计：橱柜+岛台+收纳一体化方案",
        "excerpt": "厨房是家庭使用频率最高的空间之一。全屋定制厨房需要考虑动线、收纳和美观。本文分享厨房橱柜、岛台、收纳系统的一体化定制方案...",
        "image_keywords": ["modern+kitchen", "custom+cabinets"]
    },
    {
        "category": "行业资讯",
        "title": "全屋定制行业报告：消费者最看重的三大因素",
        "excerpt": "最新行业调查报告显示，消费者在选择全屋定制时最看重的是品质、环保和设计感。浦北装修设计始终坚持以客户需求为导向，在这三个方面持续投入和提升...",
        "image_keywords": ["market+research", "home+design"]
    },
    {
        "category": "全屋定制",
        "title": "书房全屋定制方案：打造安静舒适的居家办公空间",
        "excerpt": "随着居家办公的普及，书房定制需求不断增长。本文为您分享书房全屋定制方案，包括书柜、书桌、榻榻米等一体化设计，打造多功能书房空间...",
        "image_keywords": ["home+office", "custom+bookshelf"]
    }
]


def generate_news():
    """生成一条新闻"""
    today = datetime.now().strftime('%Y-%m-%d')
    template = random.choice(NEWS_TEMPLATES)

    # 替换模板中的变量
    year_var = str(random.randint(5, 15))
    title = template["title"].format(year=year_var)
    excerpt = template["excerpt"].format(year=year_var)

    # 生成图片URL - 使用Unsplash支持关键词搜索的图片服务，确保图片与装修设计相关
    keywords = template.get('image_keywords', INTERIOR_KEYWORDS)
    selected_keyword = random.choice(keywords)
    # 混合通用关键词确保图片相关性
    all_keywords = f"{selected_keyword},{random.choice(INTERIOR_KEYWORDS)}"
    image_url = f"https://source.unsplash.com/random/800x450/?{all_keywords}"

    # 生成新闻ID（使用日期+随机数避免重复）
    news_id = datetime.now().strftime('%Y%m%d') + str(random.randint(100, 999))

    # 生成完整文章内容
    content = generate_article_content(template, title)

    # 生成新闻HTML
    news_html = f'''          <article class="news-card">
            <div class="news-card-image">
              <img src="{image_url}" alt="{title}">
            </div>
            <div class="news-card-content">
              <div class="news-card-meta">
                <span class="news-date">{today}</span>
                <span class="news-category">{template["category"]}</span>
              </div>
              <h2 class="news-card-title">{title}</h2>
              <p class="news-card-excerpt">{excerpt}</p>
              <a href="news-detail.html?id={news_id}" class="news-card-readmore">阅读更多 →</a>
            </div>
          </article>
'''

    # 生成新闻数据（用于JSON）
    news_data = {
        "id": news_id,
        "date": today,
        "category": template["category"],
        "title": title,
        "image": image_url,
        "excerpt": excerpt,
        "content": content
    }

    return news_html, news_data


def generate_article_content(template, title):
    """根据模板生成完整的文章内容"""
    category = template["category"]

    intros = [
        f"今天为大家带来一篇关于{category}的精彩内容，希望对您有所帮助。",
        f"作为浦北装修设计的专业团队，我们持续关注{category}领域的最新动态。",
        f"本期话题聚焦{category}，为您分享实用的装修知识和经验。",
    ]

    body = [
        f"**{title}**",
        random.choice(intros),
        f"浦北装修设计一直致力于为客户提供专业、优质的装修服务。在{category}方面，我们拥有丰富的经验和专业的团队。",
        f"我们始终坚持以客户为中心，以品质为根基，以创新为动力。不断学习和引进新的设计理念和技术，为客户提供更好的服务体验。",
        f"如果您对我们的服务感兴趣，欢迎拨打咨询热线：134-1227-7880，或到店参观体验。地址：浦北县小江街道XX路XX号。",
    ]

    # 根据分类添加特定内容
    if category == "全屋定制":
        body.insert(2, "全屋定制是现代装修的重要趋势，它能够根据客户的实际需求和空间特点，量身定制个性化的家具和收纳方案。我们使用环保板材，搭配精致的五金配件，确保每一件定制家具都兼具美观和实用。")
    elif category == "装修知识":
        body.insert(2, "装修是一门学问，很多细节需要提前了解。我们建议业主在装修前多做功课，了解基本的装修流程和注意事项，这样才能避免踩坑，确保装修顺利进行。")
    elif category == "公司动态":
        body.insert(2, "感谢广大客户对浦北装修设计的信任与支持。我们将继续提升服务品质，为客户带来更好的装修体验。近期我们还推出了多项服务升级，欢迎咨询了解。")
    elif category == "行业资讯":
        body.insert(2, "装修行业在不断发展变化，新材料、新工艺、新设计理念层出不穷。我们紧跟行业趋势，为客户推荐最合适的装修方案和材料选择。")

    return body


def insert_news_to_page(news_html, force=False):
    """将新闻插入到news.html页面中"""
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到新闻列表的起始位置
    marker = '<div class="news-list">'
    pos = content.find(marker)

    if pos == -1:
        print("Error: Could not find news-list div in news.html")
        return False

    # 找到marker后的换行符
    insert_pos = content.find('\n', pos) + 1

    # 检查今天的新闻是否已存在（精确匹配日期标签）
    today_str = datetime.now().strftime('%Y-%m-%d')
    date_marker = f'<span class="news-date">{today_str}</span>'
    if date_marker in content and not force:
        print(f"News for {today_str} already exists, skipping...")
        return False

    # 插入新闻
    new_content = content[:insert_pos] + news_html + content[insert_pos:]

    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Successfully inserted news for {today_str}")
    return True


def update_sidebar_latest(news_title, news_id):
    """更新侧边栏最新文章列表"""
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到侧边栏最新文章列表
    marker = '<ul class="sidebar-news-list">'
    pos = content.find(marker)

    if pos == -1:
        print("Warning: Could not find sidebar-news-list")
        return

    # 找到列表开始位置
    insert_pos = content.find('\n', pos) + 1

    # 添加新文章到列表顶部
    new_item = f'              <li><a href="news-detail.html?id={news_id}">{news_title}</a></li>\n'

    new_content = content[:insert_pos] + new_item + content[insert_pos:]

    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)


def update_news_data_json(news_data):
    """将新闻数据添加到news-data.json文件中"""
    with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查是否已存在同ID的新闻
    exists = any(item['id'] == news_data['id'] for item in data)
    if exists:
        print(f"News data {news_data['id']} already exists in JSON, skipping...")
        return False

    # 在列表顶部插入新新闻
    data.insert(0, news_data)

    with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"News data {news_data['id']} added to JSON")
    return True


def main():
    import sys
    force = '--force' in sys.argv
    print("=== 开始生成公司新闻 ===")

    # 生成新闻
    news_html, news_data = generate_news()

    # 提取标题用于侧边栏更新
    import re
    title_match = re.search(r'<h2 class="news-card-title">(.*?)</h2>', news_html)
    title = title_match.group(1) if title_match else "新文章"

    news_id = news_data['id']

    # 插入新闻到页面
    success = insert_news_to_page(news_html, force=force)

    if success:
        # 更新JSON数据文件
        update_news_data_json(news_data)
        # 更新侧边栏
        update_sidebar_latest(title, news_id)
        print(f"=== 新闻生成完成: {title} ===")
    else:
        print("=== 新闻生成跳过 ===")


if __name__ == '__main__':
    main()
