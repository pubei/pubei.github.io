#!/usr/bin/env python3
"""
自动生成公司新闻 - 每天自动发布一条关于浦北装修设计/全屋定制的新闻或动态
每条新闻的图片都与标题内容紧密相关，确保图文匹配
"""

import os
import json
import random
from datetime import datetime
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_FILE = os.path.join(BASE_DIR, 'news.html')
NEWS_DATA_FILE = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')

# 图片生成API基础URL
IMAGE_API_BASE = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"


def build_image_url(prompt, size="landscape_4_3"):
    """构建图片生成URL"""
    return f"{IMAGE_API_BASE}?prompt={quote(prompt)}&image_size={size}"


# 新闻模板库 - 全部围绕浦北装修设计和全屋定制主题
# 每个模板都配有与内容相关的具体图片prompt，确保图文匹配
NEWS_TEMPLATES = [
    # ============ 全屋定制类 ============
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制案例分享：{year}平米现代简约风格",
        "excerpt": "浦北装修设计近期完成了一套{year}平米现代简约风格的全屋定制项目。从整体设计到细节处理，每一处都体现了专业定制的品质与美感...",
        "image_prompt": "modern minimalist living room with custom built-in wardrobe and TV cabinet, clean white and wood tone interior design, professional photography"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制工艺升级，打造高品质家居体验",
        "excerpt": "为了给客户提供更好的全屋定制服务，浦北装修设计对定制工艺进行了全面升级，包括环保板材选用、精细切割工艺、智能装配技术等...",
        "image_prompt": "custom furniture workshop with precision cutting machine, craftsman working on wood panels, modern manufacturing technology, professional craftsmanship"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制优势：{year}大核心竞争力",
        "excerpt": "浦北装修设计在全屋定制领域深耕多年，积累了丰富的经验和专业优势。本期为您介绍我们的{year}大核心竞争力...",
        "image_prompt": "professional interior designer presenting custom furniture design plans to client, modern design studio, 3D renderings on screen, consultation meeting"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制材料升级：环保板材更安心",
        "excerpt": "浦北装修设计始终把客户健康放在首位，全面升级全屋定制材料，采用E0级、ENF级环保板材，为您打造绿色健康的家居环境...",
        "image_prompt": "eco friendly wood panels stacked in warehouse, E0 grade environmental protection boards, green leaf symbol on packaging, sustainable materials"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制流程解析：从设计到安装一站式服务",
        "excerpt": "浦北装修设计提供全屋定制一站式服务，从前期沟通、方案设计、材料选购到现场安装，全程专业团队跟进，让您省心省力...",
        "image_prompt": "custom furniture installation process, workers installing wardrobe in modern bedroom, professional installation team, tools and materials"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计客厅全屋定制：{year}款热门设计方案",
        "excerpt": "客厅是家庭的核心区域，全屋定制客厅需要兼顾美观与实用。浦北装修设计为您精选{year}款热门客厅定制方案，总有一款适合您...",
        "image_prompt": "modern living room with custom TV wall unit, built-in shelves and cabinets, elegant display cabinets with lighting, contemporary design"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计卧室全屋定制：衣柜+梳妆台一体化方案",
        "excerpt": "卧室是休息的重要空间，浦北装修设计提供卧室全屋定制服务，包括衣柜、梳妆台、床头柜等一体化设计，打造舒适温馨的睡眠环境...",
        "image_prompt": "luxury bedroom with custom walk-in wardrobe and integrated vanity table, soft lighting, modern minimalist design, warm wood tones"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计厨房全屋定制：打造高效舒适的烹饪空间",
        "excerpt": "厨房是家庭使用频率最高的空间，浦北装修设计提供专业的厨房全屋定制服务，从橱柜设计到收纳系统，让烹饪变得轻松愉快...",
        "image_prompt": "modern custom kitchen with elegant cabinets, marble countertop, integrated appliances, kitchen island with storage, professional design"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制价格透明，{year}项免费服务",
        "excerpt": "浦北装修设计坚持透明报价体系，让客户明明白白消费。同时推出{year}项免费服务，包括免费设计咨询、免费上门测量、免费方案修改等...",
        "image_prompt": "interior design consultation table with blueprint and cost breakdown, client and designer discussing budget, transparent pricing documents"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制售后服务升级：终身维护保障",
        "excerpt": "浦北装修设计不仅注重定制品质，更重视售后服务。我们推出全屋定制终身维护保障，让您的定制家具长久如新...",
        "image_prompt": "professional after-sales service technician repairing and maintaining custom furniture, uniformed worker with tools, customer satisfaction guarantee"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计小户型全屋定制：{year}个空间扩容技巧",
        "excerpt": "小户型也能拥有大空间感！浦北装修设计分享{year}个全屋定制空间扩容技巧，让有限空间发挥无限可能...",
        "image_prompt": "small apartment with space-saving custom furniture, multi-functional storage solutions, built-in wardrobes and foldable desk, compact modern design"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计全屋定制风格指南：{year}大流行风格解析",
        "excerpt": "全屋定制风格多样，如何选择适合自己的风格？浦北装修设计为您解析{year}大流行风格，帮助您找到理想的家居设计方向...",
        "image_prompt": "interior design style guide showing multiple room styles, modern minimalist, Nordic, new Chinese, luxury style comparison, design mood board"
    },
    {
        "category": "全屋定制",
        "title": "浦北装修设计儿童房全屋定制：安全环保更贴心",
        "excerpt": "儿童房装修安全最重要！浦北装修设计提供专业的儿童房全屋定制服务，采用环保材料和圆角设计，为孩子打造安全舒适的成长空间...",
        "image_prompt": "colorful children room with custom safe furniture, rounded edges, eco-friendly materials, study desk and wardrobe, playful design"
    },

    # ============ 装修设计类 ============
    {
        "category": "装修设计",
        "title": "浦北装修设计发布{year}年装修设计趋势报告",
        "excerpt": "浦北装修设计发布{year}年装修设计趋势报告，从色彩搭配、材质选择到空间布局，为您解析今年最流行的装修设计方向...",
        "image_prompt": "interior design trend report magazine, color palette samples, material swatches, design concept boards, modern aesthetic layout"
    },
    {
        "category": "装修设计",
        "title": "浦北装修设计新作：{year}平米北欧风格装修案例",
        "excerpt": "浦北装修设计最新完成一套{year}平米北欧风格装修案例，简洁的线条、温暖的木质元素、明亮的色彩搭配，营造温馨舒适的居家氛围...",
        "image_prompt": "Scandinavian Nordic style living room interior, white walls, light wood furniture, plants, cozy textile, bright natural lighting"
    },
    {
        "category": "装修设计",
        "title": "浦北装修设计：新中式风格的现代演绎",
        "excerpt": "传统中式与现代简约的完美融合，浦北装修设计为您呈现新中式风格的现代演绎，让东方韵味在当代家居中焕发新生...",
        "image_prompt": "new Chinese style interior design, modern interpretation of traditional Chinese elements, wooden lattice screen, ink painting, elegant furniture"
    },
    {
        "category": "装修设计",
        "title": "浦北装修设计：轻奢风格装修指南",
        "excerpt": "低调奢华有内涵，浦北装修设计为您解读轻奢风格装修要点，从材质选择到色彩搭配，打造高级感十足的居家空间...",
        "image_prompt": "luxury light style interior design, gold accents, marble surfaces, velvet furniture, crystal chandelier, elegant and sophisticated atmosphere"
    },
    {
        "category": "装修设计",
        "title": "浦北装修设计客厅装修：{year}种流行布局方案",
        "excerpt": "客厅是家的门面，浦北装修设计为您介绍{year}种流行的客厅布局方案，根据不同户型和需求，打造理想中的客厅空间...",
        "image_prompt": "various living room layout designs, sofa placement options, TV wall arrangements, multiple interior design solutions comparison"
    },
    {
        "category": "装修设计",
        "title": "浦北装修设计卧室装修：打造舒适睡眠空间",
        "excerpt": "卧室是休息的港湾，浦北装修设计为您分享卧室装修要点，从色彩、灯光到收纳，全方位打造舒适睡眠空间...",
        "image_prompt": "cozy master bedroom with soft lighting, comfortable bed, elegant bedside lamps, warm color palette, relaxing atmosphere"
    },

    # ============ 公司动态类 ============
    {
        "category": "公司动态",
        "title": "浦北装修设计本月新增{year}个全屋定制订单，客户好评如潮",
        "excerpt": "感谢客户们的信任与支持，本月浦北装修设计新增{year}个全屋定制订单。每一位客户的认可都是我们前进的动力...",
        "image_prompt": "professional design team meeting in modern office, signing contract with client, business handshake, happy customer service"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制展厅全新开放，欢迎预约参观",
        "excerpt": "浦北装修设计全屋定制展厅已完成焕新升级，展示了多种风格的全屋定制实景效果。欢迎预约参观，亲身体验专业定制的魅力...",
        "image_prompt": "modern furniture showroom with multiple room displays, custom cabinet displays, professional lighting, elegant exhibition space"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计荣获全屋定制行业品质服务认证",
        "excerpt": "经过严格评审，浦北装修设计公司荣获全屋定制品质服务认证。这一认证标志着我们在设计能力、施工质量、售后服务等方面均达到行业领先水平...",
        "image_prompt": "quality service certification award ceremony, golden trophy on stage, certificate with seal, professional award presentation"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计设计师团队赴{year}城市学习先进定制理念",
        "excerpt": "为了提升专业水平，浦北装修设计组织设计师团队赴{year}城市学习先进的全屋定制设计理念和工艺技术，为客户带来更好的服务...",
        "image_prompt": "interior designers attending training seminar, professional workshop, design education, group learning in modern classroom"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计全屋定制优惠活动：{year}限时折扣",
        "excerpt": "感恩回馈新老客户，浦北装修设计推出全屋定制限时优惠活动，{year}折起！活动期间预定还可享受免费升级服务...",
        "image_prompt": "home renovation promotion banner, discount signage, custom furniture sale event, attractive marketing display"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计锦绣花园智能家居项目圆满交付",
        "excerpt": "近日，我公司承接的锦绣花园智能家居项目已顺利完成并交付使用。该项目采用全屋智能系统，实现了灯光、安防、家电的智能控制...",
        "image_prompt": "smart home control panel on wall, modern living room with automation system, smartphone controlling home devices, futuristic interior"
    },
    {
        "category": "公司动态",
        "title": "浦北装修设计荣获{year}年度优秀室内设计企业",
        "excerpt": "在近日举行的广西室内设计行业年度评选中，我公司凭借出色的设计作品和优质的客户服务，荣获\"{year}年度优秀室内设计企业\"称号...",
        "image_prompt": "interior design award ceremony, golden award trophy, elegant stage with spotlight, professional recognition event"
    },

    # ============ 行业资讯类 ============
    {
        "category": "行业资讯",
        "title": "全屋定制行业新趋势，浦北装修设计引领浦北市场",
        "excerpt": "随着消费者对品质生活的追求，全屋定制已成为装修主流趋势。浦北装修设计凭借专业实力和优质服务，引领浦北地区全屋定制市场发展...",
        "image_prompt": "modern home design market exhibition, custom furniture industry trade show, business trend analysis, market growth chart"
    },
    {
        "category": "行业资讯",
        "title": "环保材料新标准出台，全屋定制行业迎来新变革",
        "excerpt": "国家最新环保材料标准正式实施，对全屋定制行业提出更高要求。浦北装修设计积极响应新标准，全面升级环保材料供应链，为客户提供更健康的家居环境...",
        "image_prompt": "eco friendly building materials certification, green environmental protection standard, sustainable wood panels with leaf symbol"
    },
    {
        "category": "行业资讯",
        "title": "全屋定制与智能家居融合，浦北装修设计引领智慧家居新潮流",
        "excerpt": "随着智能家居技术的发展，全屋定制与智能系统的融合已成为新趋势。浦北装修设计推出智能全屋定制方案，打造未来智慧家居生活...",
        "image_prompt": "smart home integration with custom furniture, voice control system, automated wardrobe with LED lighting, modern technology interior"
    },
    {
        "category": "行业资讯",
        "title": "全屋定制预算怎么算？{year}年最新价格参考",
        "excerpt": "全屋定制的价格是很多业主关心的问题。本文为您详细分析{year}年全屋定制的价格构成，包括板材费、五金件费、设计费、安装费等，帮助您合理规划装修预算...",
        "image_prompt": "home renovation budget planning, cost breakdown chart, calculator and blueprint, financial planning for interior design"
    },
    {
        "category": "行业资讯",
        "title": "书房全屋定制方案：打造安静舒适的居家办公空间",
        "excerpt": "随着居家办公的普及，书房定制需求不断增长。本文为您分享书房全屋定制方案，包括书柜、书桌、榻榻米等一体化设计，打造多功能书房空间...",
        "image_prompt": "modern home office study room with custom bookshelf, built-in desk, tatami area, organized workspace with natural light"
    },
    {
        "category": "行业资讯",
        "title": "环保装修材料新升级，打造绿色健康家居",
        "excerpt": "随着人们对环保健康的重视，我公司引入了一系列新型环保装修材料，包括零甲醛板材、水性涂料、天然石材等，为客户提供更健康、更环保的装修解决方案...",
        "image_prompt": "eco friendly renovation materials display, zero formaldehyde boards, water-based paint cans, natural stone samples, green building products"
    },
    {
        "category": "行业资讯",
        "title": "设计团队参加高端室内设计培训，提升专业素养",
        "excerpt": "为了不断提升设计团队的专业水平，我公司组织设计人员参加了为期一周的高端室内设计培训课程，学习最新的设计理念和技术...",
        "image_prompt": "interior design training class, professional designers learning new skills, design workshop with presentation, modern education setting"
    },
    {
        "category": "行业资讯",
        "title": "{year}年装修流行趋势：这五种风格将引领潮流",
        "excerpt": "新的一年，装修风格也在不断演变。根据行业数据分析，{year}年以下五种装修风格将成为主流：现代简约、轻奢风格、北欧风格、新中式和侘寂风...",
        "image_prompt": "interior design style trends comparison, five different room styles showcase, modern minimalist luxury Nordic Chinese wabi-sabi"
    },
    {
        "category": "行业资讯",
        "title": "装修避坑指南：新房装修必看的十大注意事项",
        "excerpt": "很多业主在装修时都会遇到各种问题，导致装修效果不尽如人意。今天，我们为大家整理了新房装修中最容易踩坑的十个方面，希望能帮助您避开装修陷阱...",
        "image_prompt": "home renovation checklist, ten important tips for decoration, warning signs and notes, construction site inspection"
    },
]


def generate_news():
    """生成一条新闻"""
    today = datetime.now().strftime('%Y-%m-%d')
    template = random.choice(NEWS_TEMPLATES)

    # 替换模板中的变量
    year_var = str(random.randint(5, 15))
    title = template["title"].format(year=year_var)
    excerpt = template["excerpt"].format(year=year_var)

    # 生成图片URL - 根据新闻内容生成相关图片，确保图文匹配
    image_url = build_image_url(template["image_prompt"])

    # 生成新闻ID（使用日期+随机数避免重复）
    news_id = datetime.now().strftime('%Y%m%d') + str(random.randint(100, 999))

    # 生成完整文章内容
    content = generate_article_content(template, title)

    # 生成新闻HTML
    news_html = f'''          <article class="news-card">
            <div class="news-card-image">
              <img src="{image_url}" alt="{title}">
              <div class="news-card-image-overlay">
                <div class="news-card-image-title">{title}</div>
              </div>
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
    elif category == "装修设计":
        body.insert(2, "专业的装修设计能够最大程度地发挥空间潜力，结合业主的生活习惯和审美偏好，打造既美观又实用的居住环境。我们注重每一个设计细节，从色彩搭配到材质选择，都力求完美。")
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
        print(f"=== 新闻类别: {news_data['category']} ===")
        print(f"=== 图片URL已根据内容生成 ===")
    else:
        print("=== 新闻生成跳过 ===")


if __name__ == '__main__':
    main()
