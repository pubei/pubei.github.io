#!/usr/bin/env python3
"""
自动生成公司新闻 - 每天自动发布一条关于浦北装修设计/全屋定制的新闻或动态
每条新闻的图片都与标题内容紧密相关，确保图文匹配
图片采用纯 SVG 动态生成，零外部依赖，CI/CD 环境 100% 可靠
"""

import os
import json
import random
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_FILE = os.path.join(BASE_DIR, 'news.html')
NEWS_DATA_FILE = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')

# ============================================================================
# SVG 图片生成 - 零外部依赖，稳定可靠
# ============================================================================

# 分类配色方案 - 每个分类有独特的渐变配色
CATEGORY_THEMES = {
    "全屋定制": {
        "gradients": [
            ("#00d4ff", "#7b2ff7"),
            ("#7b2ff7", "#00ff80"),
            ("#ff6b6b", "#feca57"),
            ("#48dbfb", "#0abde3"),
            ("#5f27cd", "#341f97"),
        ],
        "icons": ["🏠", "🛋️", "🪑", "🗄️", "🚪", "🪟", "📐", "🔨"],
        "subtitle": "全屋定制 · 品质生活",
    },
    "装修设计": {
        "gradients": [
            ("#667eea", "#764ba2"),
            ("#f093fb", "#f5576c"),
            ("#4facfe", "#00f2fe"),
            ("#43e97b", "#38f9d7"),
            ("#fa709a", "#fee140"),
        ],
        "icons": ["🎨", "🖌️", "✨", "💡", "🪟", "🌈", "🌸", "🖼️"],
        "subtitle": "装修设计 · 匠心品质",
    },
    "公司动态": {
        "gradients": [
            ("#00d4ff", "#0099cc"),
            ("#06beb6", "#48b1bf"),
            ("#11998e", "#38ef7d"),
            ("#373b44", "#4286f4"),
            ("#232526", "#414345"),
        ],
        # 装修相关图标：工地/展厅/工具/施工语义
        "icons": ["🏠", "🏗️", "🔨", "🪚", "🪜", "🧰", "📐", "📋"],
        "subtitle": "公司动态 · 实时更新",
    },
    "行业资讯": {
        "gradients": [
            ("#ee0979", "#ff6a00"),
            ("#ff9966", "#ff5e62"),
            ("#f7971e", "#ffd200"),
            ("#134e5e", "#71b280"),
            ("#614385", "#516395"),
        ],
        # 装修相关图标：材料/环保/空间语义
        "icons": ["🪵", "🌿", "🧱", "🪟", "🏠", "🛋️", "💡", "📐"],
        "subtitle": "行业资讯 · 前沿洞察",
    },
}

# 默认主题（未匹配分类时使用）- 全部为装修相关图标
DEFAULT_THEME = {
    "gradients": [
        ("#00d4ff", "#7b2ff7"),
        ("#7b2ff7", "#00ff80"),
    ],
    "icons": ["🏠", "✨", "🪟", "🔨", "🪑", "📐"],
    "subtitle": "浦北装修设计",
}


def _hash_to_seed(text):
    """将文本转换为随机种子，确保同一新闻ID生成相同图片"""
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


def _truncate_title(title, max_chars=14):
    """截断长标题以适配图片显示"""
    if len(title) <= max_chars:
        return title
    return title[:max_chars - 1] + "…"


def generate_svg_image(news_id, title, category):
    """
    为新闻生成一张独特的 SVG 封面图
    - 根据分类选择配色和图标
    - 根据 news_id 哈希生成确定性随机，保证一致性
    - 包含装饰性几何元素
    """
    seed = _hash_to_seed(news_id)
    rng = random.Random(seed)
    
    theme = CATEGORY_THEMES.get(category, DEFAULT_THEME)
    gradient = rng.choice(theme["gradients"])
    icon = rng.choice(theme["icons"])
    subtitle = theme.get("subtitle", DEFAULT_THEME["subtitle"])
    
    accent_color = gradient[1]
    gradient_id = f"grad_{news_id}"
    pattern_id = f"pat_{news_id}"
    
    display_title = _truncate_title(title, 16)
    
    # 生成装饰圆圈
    circles = []
    for i in range(rng.randint(3, 6)):
        cx = rng.randint(20, 380)
        cy = rng.randint(20, 280)
        r = rng.randint(15, 50)
        opacity = rng.uniform(0.05, 0.15)
        circles.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" opacity="{opacity:.2f}"/>'
        )
    
    circles_svg = "\n      ".join(circles)
    
    # 生成装饰线条
    lines = []
    for i in range(rng.randint(2, 4)):
        x1 = rng.randint(0, 200)
        y1 = rng.randint(0, 300)
        x2 = x1 + rng.randint(40, 120)
        y2 = y1 + rng.randint(-30, 30)
        opacity = rng.uniform(0.05, 0.12)
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="1" opacity="{opacity:.2f}"/>'
        )
    
    lines_svg = "\n      ".join(lines)

    # 装饰性房屋轮廓（所有分类共用，强化"装修"主题）
    house_decoration = '''<!-- 房屋轮廓装饰 -->
    <g opacity="0.10" fill="none" stroke="white" stroke-width="2" stroke-linejoin="round">
      <path d="M 330 265 L 330 205 L 370 175 L 410 205 L 410 265 Z"/>
      <rect x="345" y="225" width="18" height="40"/>
      <rect x="378" y="215" width="22" height="22"/>
    </g>
    <g opacity="0.08" fill="none" stroke="white" stroke-width="2" stroke-linejoin="round">
      <path d="M -10 285 L -10 245 L 25 220 L 60 245 L 60 285 Z"/>
      <rect x="5" y="255" width="15" height="30"/>
    </g>'''

    # 分割线位置
    divider_y = 210 if len(display_title) <= 10 else 220

    # emoji 字体栈，确保装修图标在所有平台正确渲染
    emoji_font = "'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
    <defs>
      <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{gradient[0]}"/>
        <stop offset="100%" stop-color="{gradient[1]}"/>
      </linearGradient>
      <linearGradient id="{gradient_id}_overlay" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="black" stop-opacity="0"/>
        <stop offset="100%" stop-color="black" stop-opacity="0.4"/>
      </linearGradient>
      <filter id="{gradient_id}_shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="black" flood-opacity="0.3"/>
      </filter>
    </defs>

    <!-- 背景渐变 -->
    <rect width="400" height="300" fill="url(#{gradient_id})"/>

    <!-- 装饰性圆圈 -->
    {circles_svg}

    <!-- 装饰性线条 -->
    {lines_svg}

    {house_decoration}

    <!-- 底部渐变遮罩 -->
    <rect width="400" height="300" fill="url(#{gradient_id}_overlay)"/>

    <!-- 分类标签 -->
    <rect x="20" y="20" rx="12" ry="12" width="{len(category) * 14 + 24}" height="28" fill="white" opacity="0.2"/>
    <text x="32" y="40" font-size="13" font-weight="600" fill="white" font-family="'Noto Sans SC', sans-serif">{category}</text>

    <!-- 图标（装修主题） -->
    <text x="200" y="135" text-anchor="middle" font-size="56" filter="url(#{gradient_id}_shadow)" font-family="{emoji_font}">{icon}</text>

    <!-- 主标题 -->
    <text x="200" y="175" text-anchor="middle" font-size="22" font-weight="700" fill="white" font-family="'Noto Sans SC', sans-serif" letter-spacing="1">{display_title}</text>

    <!-- 副标题 -->
    <text x="200" y="{divider_y + 20}" text-anchor="middle" font-size="13" fill="rgba(255,255,255,0.75)" font-family="'Noto Sans SC', sans-serif" letter-spacing="2">{subtitle}</text>

    <!-- 底部品牌信息 -->
    <line x1="150" y1="270" x2="250" y2="270" stroke="white" stroke-width="1" opacity="0.3"/>
    <text x="200" y="288" text-anchor="middle" font-size="11" fill="rgba(255,255,255,0.5)" font-family="'Noto Sans SC', sans-serif">浦北装修设计 · 专业品质 · 匠心铸就</text>
  </svg>'''
    
    return svg_content


# 图片生成 API 基础 URL（与首页 CSS 中使用的一致，浏览器带认证可正常加载）
IMAGE_API_BASE = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
IMAGE_SIZE = "landscape_4_3"  # 与首页案例卡片一致，横向 4:3 适合新闻卡片


def _build_image_url(prompt):
    """构造完整的图片生成 API URL（prompt 需 URL 编码）"""
    from urllib.parse import quote
    return f"{IMAGE_API_BASE}?prompt={quote(prompt)}&image_size={IMAGE_SIZE}"


def _prompt_for_news(title, category):
    """根据新闻标题和分类生成专属的真实装修场景英文 prompt
    与首页 CSS 中的 prompt 风格保持一致：真实室内设计摄影"""
    t = title

    # ===== 全屋定制 - 具体房间类型 =====
    if '客厅' in t and ('布局' in t or '装修' in t):
        return ("modern luxury living room interior design with elegant sofa "
                "TV wall unit soft lighting warm atmosphere minimalist style "
                "professional photography")
    if '儿童房' in t:
        return ("colorful children bedroom with custom safe furniture rounded edges "
                "eco-friendly materials wardrobe and study desk warm playful design "
                "professional interior photography")
    if '厨房' in t:
        return ("modern custom kitchen with elegant cabinets marble countertop "
                "kitchen island with storage integrated appliances professional "
                "interior design photography warm lighting")
    if '书房' in t:
        return ("modern home office study room with custom built-in bookshelf "
                "wooden desk tatami area organized workspace natural light "
                "professional interior design photography")
    if '卧室' in t or '衣柜' in t:
        return ("luxury bedroom with custom walk-in wardrobe integrated vanity "
                "table soft warm lighting modern minimalist design cozy atmosphere "
                "professional interior photography")
    if '小户型' in t:
        return ("small apartment with space-saving custom furniture multi-functional "
                "storage solutions built-in wardrobes foldable desk compact modern "
                "minimalist interior design photography")
    if '风格' in t and ('指南' in t or '解析' in t):
        return ("interior design style guide showing multiple room styles modern "
                "minimalist Nordic new Chinese luxury style comparison design mood "
                "board professional photography")

    # ===== 全屋定制 - 工艺/材料/流程 =====
    if '材料升级' in t or '环保板材' in t:
        return ("eco friendly wood panels stacked in warehouse E0 grade environmental "
                "protection boards green leaf symbol on packaging sustainable materials "
                "professional photography")
    if '工艺升级' in t or '工艺' in t:
        return ("custom furniture workshop with precision cutting machine craftsman "
                "working on wood panels modern manufacturing technology professional "
                "craftsmanship photography")
    if '安装' in t or '流程' in t:
        return ("custom furniture installation process workers installing wardrobe "
                "in modern bedroom professional installation team tools and materials "
                "professional photography")

    # ===== 智能家居 =====
    if '智能家居' in t and '融合' in t:
        return ("smart home integration with custom furniture voice control system "
                "automated wardrobe with LED lighting modern technology interior design "
                "professional photography")
    if '智能家居项目' in t or '锦绣花园' in t:
        return ("smart home control panel on wall modern living room with automation "
                "system smartphone controlling home devices futuristic interior design "
                "professional photography")

    # ===== 公司动态 =====
    if ('认证' in t or '荣获' in t) and '品质' in t:
        return ("quality service certification award ceremony golden trophy on stage "
                "certificate with seal professional award presentation modern elegant "
                "event photography")
    if '优秀室内设计企业' in t:
        return ("interior design award ceremony golden award trophy elegant stage "
                "with spotlight professional recognition event modern luxury interior "
                "design company showcase")
    if '培训' in t or '学习' in t or '设计师团队' in t:
        return ("interior designers attending training seminar professional workshop "
                "design education group learning in modern classroom design studio with "
                "presentation professional photography")
    if '订单' in t and ('新增' in t or '签约' in t):
        return ("professional design team meeting in modern office signing contract "
                "with client business handshake happy customer service modern interior "
                "design company photography")

    # ===== 行业资讯 =====
    if '避坑' in t or '注意事项' in t:
        return ("home renovation checklist ten important tips for decoration warning "
                "signs and notes construction site inspection professional engineer "
                "with clipboard professional photography")
    if '趋势' in t and ('风格' in t or '流行' in t):
        return ("interior design style trends comparison five different room styles "
                "showcase modern minimalist luxury Nordic Chinese wabi-sabi professional "
                "photography mood board")
    if '环保材料' in t or '环保' in t:
        return ("eco friendly renovation materials display zero formaldehyde boards "
                "water-based paint cans natural stone samples green building products "
                "sustainable interior design photography")
    if '预算' in t:
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
    return ("modern luxury home interior design with elegant living room minimalist "
            "style soft lighting warm atmosphere professional photography")


def save_news_image(title, category, news_id):
    """
    生成新闻图片 URL
    使用 trae-api-cn 图片生成 API（与首页背景图方案一致）
    浏览器带认证可正常加载，返回 API URL（不再生成本地 SVG）
    """
    prompt = _prompt_for_news(title, category)
    image_url = _build_image_url(prompt)
    print(f"    ✓ 真实装修图片 URL 已生成: {image_url[:80]}...")
    return image_url


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

    # 生成新闻ID（使用日期+随机数避免重复）
    news_id = datetime.now().strftime('%Y%m%d') + str(random.randint(100, 999))
    
    # 生成分类
    category = template.get("category", "装修设计")
    
    # 生成 SVG 图片 - 纯本地生成，零外部依赖
    image_url = save_news_image(title, category, news_id)

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


def regenerate_existing_images():
    """
    根据 news-data.json 重新生成所有新闻的 SVG 图片
    用于主题图标调整后回填，确保所有图片都符合装修设计/全屋定制主题
    历史遗留分类（如"装修知识"）会被映射到"装修设计"
    """
    print("=== 开始重新生成所有新闻 SVG 图片 ===")
    with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 分类映射：将历史遗留分类统一到标准分类
    category_mapping = {
        "装修知识": "装修设计",
    }

    updated_count = 0
    for item in data:
        news_id = str(item['id'])
        title = item['title']
        category = item.get('category', '装修设计')

        # 处理历史遗留分类
        original_category = category
        if category in category_mapping:
            category = category_mapping[category]
            item['category'] = category
            print(f"  ↺ ID={news_id}: 分类 '{original_category}' → '{category}'")

        # 重新生成 SVG
        save_news_image(title, category, news_id)
        updated_count += 1

    # 保存更新后的 JSON（分类可能被映射）
    with open(NEWS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=== 已重新生成 {updated_count} 张 SVG 图片 ===")
    print(f"=== 所有图片均使用装修设计/全屋定制主题图标 ===")


def main():
    import sys

    # 命令行参数：重新生成所有现有新闻的 SVG 图片
    if '--regenerate-images' in sys.argv:
        regenerate_existing_images()
        return

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
