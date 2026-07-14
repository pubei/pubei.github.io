#!/usr/bin/env python3
"""
自动生成公司新闻 - 每天自动发布一条关于浦北装修设计/全屋定制的新闻或动态
"""

import os
import random
from datetime import datetime, timedelta

NEWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'news.html')

# 新闻模板库 - 涵盖全屋定制、装修知识、公司动态、行业资讯等
NEWS_TEMPLATES = [
    {
        "category": "全屋定制",
        "title": "全屋定制趋势：{year}年最受欢迎的定制设计方案",
        "excerpt": "随着生活品质的提升，全屋定制已成为现代家庭装修的首选。本期为您解读{year}年最受欢迎的全屋定制设计方案，包括简约风格、轻奢风格和新中式风格...",
        "image_prompt": "custom%20home%20interior%20modern%20design%20wardrobe%20cabinet%20built%20in%20furniture%20elegant"
    },
    {
        "category": "装修知识",
        "title": "全屋定制避坑指南：业主必须了解的{year}个关键细节",
        "excerpt": "全屋定制虽然方便，但如果不注意细节，很容易踩坑。今天我们整理了全屋定制中最容易出问题的{year}个关键细节，帮助您避免装修遗憾...",
        "image_prompt": "home%20renovation%20tips%20guide%20professional%20consultation%20interior%20design%20advice"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计本月新增{year}个全屋定制订单，服务再升级",
        "excerpt": "感谢客户们的信任与支持，本月我公司新增{year}个全屋定制订单。为更好地服务客户，我们升级了设计团队和施工工艺，为您提供更优质的全屋定制服务...",
        "image_prompt": "professional%20team%20meeting%20interior%20design%20company%20office%20modern%20workspace"
    },
    {
        "category": "行业资讯",
        "title": "环保材料新标准出台，全屋定制行业迎来新变革",
        "excerpt": "国家最新环保材料标准正式实施，对全屋定制行业提出更高要求。浦北装修设计积极响应新标准，全面升级环保材料供应链，为客户提供更健康的家居环境...",
        "image_prompt": "eco%20friendly%20green%20building%20materials%20sustainable%20interior%20design%20nature"
    },
    {
        "category": "全屋定制",
        "title": "小户型全屋定制方案：{year}平米也能住出大空间感",
        "excerpt": "面积小不代表不能拥有高品质的生活。通过合理的全屋定制方案，即使是{year}平米的小户型也能打造出宽敞舒适的居住空间。本期分享几个实用的设计技巧...",
        "image_prompt": "small%20apartment%20interior%20design%20space%20saving%20custom%20furniture%20compact%20living"
    },
    {
        "category": "装修知识",
        "title": "全屋定制板材怎么选？E0、E1、ENF级区别详解",
        "excerpt": "全屋定制中最重要的就是板材选择。E0级、E1级、ENF级板材有什么区别？哪种更适合家庭使用？本文为您详细解读各种环保等级板材的特点和适用场景...",
        "image_prompt": "wood%20panels%20boards%20material%20selection%20furniture%20manufacturing%20quality"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制展厅焕新升级，欢迎参观体验",
        "excerpt": "为了给客户带来更好的体验，我公司全屋定制展厅已完成焕新升级。新展厅展示了多种风格的全屋定制实景效果，包括现代简约、轻奢、北欧等风格，欢迎莅临参观...",
        "image_prompt": "showroom%20interior%20design%20display%20modern%20furniture%20exhibition%20elegant"
    },
    {
        "category": "全屋定制",
        "title": "客厅全屋定制设计要点：打造温馨实用的家庭核心区",
        "excerpt": "客厅是家庭活动的核心区域，全屋定制客厅需要兼顾美观与实用。本文为您分享客厅全屋定制的设计要点，包括电视柜、收纳柜、展示柜的定制技巧...",
        "image_prompt": "modern%20living%20room%20custom%20cabinet%20TV%20wall%20storage%20elegant%20design"
    },
    {
        "category": "行业资讯",
        "title": "智能家居与全屋定制融合，打造未来智慧家居生活",
        "excerpt": "随着智能家居技术的发展，全屋定制与智能系统的融合已成为新趋势。浦北装修设计推出智能全屋定制方案，将智能照明、安防监控、家电控制等融入定制家具中...",
        "image_prompt": "smart%20home%20technology%20integration%20modern%20living%20room%20automated%20furniture"
    },
    {
        "category": "全屋定制",
        "title": "卧室全屋定制攻略：衣柜+梳妆台+床头柜一体化设计",
        "excerpt": "卧室是休息的重要空间，全屋定制卧室需要考虑收纳和舒适度。本文为您分享卧室一体化定制方案，包括衣柜、梳妆台、床头柜的协调设计...",
        "image_prompt": "modern%20bedroom%20custom%20wardrobe%20integrated%20design%20elegant%20cozy"
    },
    {
        "category": "装修知识",
        "title": "全屋定制预算怎么算？2026年最新价格参考",
        "excerpt": "全屋定制的价格是很多业主关心的问题。本文为您详细分析2026年全屋定制的价格构成，包括板材费、五金件费、设计费、安装费等，帮助您合理规划装修预算...",
        "image_prompt": "budget%20planning%20calculator%20home%20renovation%20cost%20estimate%20financial"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计荣获全屋定制品质服务认证",
        "excerpt": "经过严格评审，浦北装修设计公司荣获全屋定制品质服务认证。这一认证标志着我们在设计能力、施工质量、售后服务等方面均达到行业领先水平...",
        "image_prompt": "award%20ceremony%20certificate%20professional%20recognition%20quality%20service%20trophy"
    },
    {
        "category": "全屋定制",
        "title": "厨房全屋定制设计：橱柜+岛台+收纳一体化方案",
        "excerpt": "厨房是家庭使用频率最高的空间之一。全屋定制厨房需要考虑动线、收纳和美观。本文分享厨房橱柜、岛台、收纳系统的一体化定制方案...",
        "image_prompt": "modern%20kitchen%20custom%20cabinets%20island%20counter%20elegant%20design%20luxury"
    },
    {
        "category": "行业资讯",
        "title": "全屋定制行业报告：消费者最看重的三大因素",
        "excerpt": "最新行业调查报告显示，消费者在选择全屋定制时最看重的是品质、环保和设计感。浦北装修设计始终坚持以客户需求为导向，在这三个方面持续投入和提升...",
        "image_prompt": "market%20research%20data%20analysis%20consumer%20survey%20chart%20infographic"
    },
    {
        "category": "全屋定制",
        "title": "书房全屋定制方案：打造安静舒适的居家办公空间",
        "excerpt": "随着居家办公的普及，书房定制需求不断增长。本文为您分享书房全屋定制方案，包括书柜、书桌、榻榻米等一体化设计，打造多功能书房空间...",
        "image_prompt": "home%20office%20study%20room%20custom%20bookshelf%20desk%20elegant%20design%20quiet"
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

    # 生成图片URL
    image_url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={template['image_prompt']}&image_size=landscape_16_9"

    # 生成新闻ID（使用日期）
    news_id = datetime.now().strftime('%Y%m%d')

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

    return news_html


def insert_news_to_page(news_html):
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

    # 检查今天的新闻是否已存在
    today_str = datetime.now().strftime('%Y-%m-%d')
    if today_str in content:
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


def main():
    print("=== 开始生成公司新闻 ===")

    # 生成新闻
    news_html = generate_news()

    # 提取标题用于侧边栏更新
    import re
    title_match = re.search(r'<h2 class="news-card-title">(.*?)</h2>', news_html)
    title = title_match.group(1) if title_match else "新文章"

    news_id = datetime.now().strftime('%Y%m%d')

    # 插入新闻到页面
    success = insert_news_to_page(news_html)

    if success:
        # 更新侧边栏
        update_sidebar_latest(title, news_id)
        print(f"=== 新闻生成完成: {title} ===")
    else:
        print("=== 新闻生成跳过 ===")


if __name__ == '__main__':
    main()
