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

# 装修相关图片URL库 - 使用本地SVG图片，确保图片稳定显示且与装修设计相关
INTERIOR_IMAGES = [
    "assets/images/news-bg-1.svg",
    "assets/images/news-bg-2.svg",
    "assets/images/news-bg-3.svg",
    "assets/images/news-bg-4.svg",
    "assets/images/news-bg-1.svg",
    "assets/images/news-bg-2.svg",
    "assets/images/news-bg-3.svg",
    "assets/images/news-bg-4.svg",
    "assets/images/news-bg-1.svg",
    "assets/images/news-bg-2.svg",
    "assets/images/news-bg-3.svg",
    "assets/images/news-bg-4.svg",
    "assets/images/news-bg-1.svg",
    "assets/images/news-bg-2.svg",
    "assets/images/news-bg-3.svg"
]

# 新闻模板库 - 全部围绕浦北装修设计和全屋定制主题
NEWS_TEMPLATES = [
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制案例分享：{year}平米现代简约风格",
        "excerpt": "浦北装修设计近期完成了一套{year}平米现代简约风格的全屋定制项目。从整体设计到细节处理，每一处都体现了专业定制的品质与美感...",
        "image_keywords": ["custom+furniture", "modern+interior"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制工艺升级，打造高品质家居体验",
        "excerpt": "为了给客户提供更好的全屋定制服务，浦北装修设计对定制工艺进行了全面升级，包括环保板材选用、精细切割工艺、智能装配技术等...",
        "image_keywords": ["custom+furniture", "modern+interior"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计本月新增{year}个全屋定制订单，客户好评如潮",
        "excerpt": "感谢客户们的信任与支持，本月浦北装修设计新增{year}个全屋定制订单。每一位客户的认可都是我们前进的动力...",
        "image_keywords": ["design+studio", "professional+team"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制优势：{year}大核心竞争力",
        "excerpt": "浦北装修设计在全屋定制领域深耕多年，积累了丰富的经验和专业优势。本期为您介绍我们的{year}大核心竞争力...",
        "image_keywords": ["design+studio", "professional+team"]
    },
    {
        "category": "行业资讯",
        "title": "全屋定制行业新趋势，浦北装修设计引领浦北市场",
        "excerpt": "随着消费者对品质生活的追求，全屋定制已成为装修主流趋势。浦北装修设计凭借专业实力和优质服务，引领浦北地区全屋定制市场发展...",
        "image_keywords": ["market+research", "home+design"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制材料升级：环保板材更安心",
        "excerpt": "浦北装修设计始终把客户健康放在首位，全面升级全屋定制材料，采用E0级、ENF级环保板材，为您打造绿色健康的家居环境...",
        "image_keywords": ["eco+friendly+materials", "green+interior"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制展厅全新开放，欢迎预约参观",
        "excerpt": "浦北装修设计全屋定制展厅已完成焕新升级，展示了多种风格的全屋定制实景效果。欢迎预约参观，亲身体验专业定制的魅力...",
        "image_keywords": ["showroom+interior", "furniture+display"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制流程解析：从设计到安装一站式服务",
        "excerpt": "浦北装修设计提供全屋定制一站式服务，从前期沟通、方案设计、材料选购到现场安装，全程专业团队跟进，让您省心省力...",
        "image_keywords": ["custom+furniture", "modern+interior"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计客厅全屋定制：{year}款热门设计方案",
        "excerpt": "客厅是家庭的核心区域，全屋定制客厅需要兼顾美观与实用。浦北装修设计为您精选{year}款热门客厅定制方案，总有一款适合您...",
        "image_keywords": ["modern+living+room", "TV+cabinet"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计卧室全屋定制：衣柜+梳妆台一体化方案",
        "excerpt": "卧室是休息的重要空间，浦北装修设计提供卧室全屋定制服务，包括衣柜、梳妆台、床头柜等一体化设计，打造舒适温馨的睡眠环境...",
        "image_keywords": ["modern+bedroom", "custom+wardrobe"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计厨房全屋定制：打造高效舒适的烹饪空间",
        "excerpt": "厨房是家庭使用频率最高的空间，浦北装修设计提供专业的厨房全屋定制服务，从橱柜设计到收纳系统，让烹饪变得轻松愉快...",
        "image_keywords": ["modern+kitchen", "custom+cabinets"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计荣获全屋定制行业品质服务认证",
        "excerpt": "经过严格评审，浦北装修设计公司荣获全屋定制品质服务认证。这一认证标志着我们在设计能力、施工质量、售后服务等方面均达到行业领先水平...",
        "image_keywords": ["award+certificate", "quality+service"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制价格透明，{year}项免费服务",
        "excerpt": "浦北装修设计坚持透明报价体系，让客户明明白白消费。同时推出{year}项免费服务，包括免费设计咨询、免费上门测量、免费方案修改等...",
        "image_keywords": ["home+budget", "renovation+cost"]
    },
    {
        "category": "行业资讯",
        "title": "全屋定制与智能家居融合，浦北装修设计引领智慧家居新潮流",
        "excerpt": "随着智能家居技术的发展，全屋定制与智能系统的融合已成为新趋势。浦北装修设计推出智能全屋定制方案，打造未来智慧家居生活...",
        "image_keywords": ["smart+home", "modern+living+room"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制售后服务升级：终身维护保障",
        "excerpt": "浦北装修设计不仅注重定制品质，更重视售后服务。我们推出全屋定制终身维护保障，让您的定制家具长久如新...",
        "image_keywords": ["quality+service", "after+sales"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计小户型全屋定制：{year}个空间扩容技巧",
        "excerpt": "小户型也能拥有大空间感！浦北装修设计分享{year}个全屋定制空间扩容技巧，让有限空间发挥无限可能...",
        "image_keywords": ["small+apartment+design", "space+saving"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计设计师团队赴{year}城市学习先进定制理念",
        "excerpt": "为了提升专业水平，浦北装修设计组织设计师团队赴{year}城市学习先进的全屋定制设计理念和工艺技术，为客户带来更好的服务...",
        "image_keywords": ["design+studio", "professional+team"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制风格指南：{year}大流行风格解析",
        "excerpt": "全屋定制风格多样，如何选择适合自己的风格？浦北装修设计为您解析{year}大流行风格，帮助您找到理想的家居设计方向...",
        "image_keywords": ["modern+interior", "design+style"]
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计儿童房全屋定制：安全环保更贴心",
        "excerpt": "儿童房装修安全最重要！浦北装修设计提供专业的儿童房全屋定制服务，采用环保材料和圆角设计，为孩子打造安全舒适的成长空间...",
        "image_keywords": ["kids+room", "safe+furniture"]
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制优惠活动：{year}限时折扣",
        "excerpt": "感恩回馈新老客户，浦北装修设计推出全屋定制限时优惠活动，{year}折起！活动期间预定还可享受免费升级服务...",
        "image_keywords": ["promotion", "discount"]
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

    # 生成图片URL - 使用固定的装修相关图片库，确保图片稳定且与装修设计相关
    image_url = random.choice(INTERIOR_IMAGES)

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
