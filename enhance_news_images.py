#!/usr/bin/env python3
"""
增强版新闻 SVG 图片生成器
为每条新闻生成与装修设计/全屋定制内容强相关的精致 SVG 插画
特点：
- 3D 透视场景（地板/墙面/天花板的远近层次）
- 玻璃拟态效果（半透明面板、模糊、内发光）
- 渐变光效（暖色调灯光、冷暖对比）
- 现代家具剪影（沙发、电视墙、橱柜、书架等）
- 与新闻标题内容强相关（客厅、儿童房、厨房、书房等）
- 无标题文字（由 HTML overlay 显示，避免冗余）
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DATA_FILE = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')
NEWS_IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'news')


# ============================================================================
# 通用 SVG 头部和定义
# ============================================================================

def svg_defs(gradient_id, color_a, color_b, accent_color):
    """生成通用 defs：背景渐变、玻璃拟态滤镜、阴影滤镜、发光滤镜"""
    return f'''<defs>
      <linearGradient id="{gradient_id}_bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{color_a}"/>
        <stop offset="100%" stop-color="{color_b}"/>
      </linearGradient>
      <linearGradient id="{gradient_id}_floor" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="rgba(0,0,0,0.45)"/>
        <stop offset="100%" stop-color="rgba(0,0,0,0.05)"/>
      </linearGradient>
      <linearGradient id="{gradient_id}_wall" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="rgba(255,255,255,0.18)"/>
        <stop offset="100%" stop-color="rgba(255,255,255,0.02)"/>
      </linearGradient>
      <linearGradient id="{gradient_id}_glass" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="rgba(255,255,255,0.28)"/>
        <stop offset="50%" stop-color="rgba(255,255,255,0.10)"/>
        <stop offset="100%" stop-color="rgba(255,255,255,0.20)"/>
      </linearGradient>
      <radialGradient id="{gradient_id}_spot" cx="50%" cy="20%" r="60%">
        <stop offset="0%" stop-color="rgba(255,240,200,0.55)"/>
        <stop offset="100%" stop-color="rgba(255,240,200,0)"/>
      </radialGradient>
      <linearGradient id="{gradient_id}_accent" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{accent_color}" stop-opacity="0"/>
        <stop offset="50%" stop-color="{accent_color}" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="{accent_color}" stop-opacity="0"/>
      </linearGradient>
      <filter id="{gradient_id}_blur" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2.5"/>
      </filter>
      <filter id="{gradient_id}_shadow" x="-30%" y="-30%" width="160%" height="160%">
        <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="black" flood-opacity="0.35"/>
      </filter>
      <filter id="{gradient_id}_glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>'''


def svg_skeleton(gradient_id, color_a, color_b, accent_color, scene_svg, category_label=""):
    """生成 SVG 骨架：背景 + 顶部聚光 + 场景 + 底部暗化遮罩 + 分类标签"""
    defs = svg_defs(gradient_id, color_a, color_b, accent_color)
    category_html = ""
    if category_label:
        label_w = len(category_label) * 14 + 24
        category_html = f'''
    <!-- 分类标签（玻璃拟态） -->
    <rect x="18" y="18" rx="14" ry="14" width="{label_w}" height="26" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.35)" stroke-width="1" filter="url(#{gradient_id}_blur)"/>
    <rect x="18" y="18" rx="14" ry="14" width="{label_w}" height="26" fill="rgba(0,0,0,0.18)" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
    <text x="30" y="36" font-size="12" font-weight="600" fill="white" font-family="'Noto Sans SC', sans-serif">{category_label}</text>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
    {defs}

    <!-- 背景渐变 -->
    <rect width="400" height="300" fill="url(#{gradient_id}_bg)"/>

    <!-- 顶部聚光（暖光氛围） -->
    <rect width="400" height="180" fill="url(#{gradient_id}_spot)"/>

    <!-- 装饰光斑 -->
    <circle cx="60" cy="50" r="42" fill="white" opacity="0.06"/>
    <circle cx="350" cy="240" r="55" fill="white" opacity="0.05"/>
    <circle cx="340" cy="60" r="22" fill="white" opacity="0.08"/>

    <!-- 场景插画 -->
    {scene_svg}

    <!-- 底部渐变遮罩（增强文字可读性，配合 HTML overlay） -->
    <rect y="170" width="400" height="130" fill="url(#{gradient_id}_floor)"/>
{category_html}
  </svg>'''


# ============================================================================
# 场景组件库 - 装修设计/全屋定制实景元素
# ============================================================================

def room_perspective(g, floor_y=210, wall_color="rgba(255,255,255,0.12)", floor_color="rgba(0,0,0,0.18)"):
    """绘制房间透视：左墙、右墙、后墙、地板"""
    return f'''
      <!-- 房间透视：后墙 + 地板 -->
      <rect x="40" y="60" width="320" height="{floor_y - 60}" fill="{wall_color}"/>
      <polygon points="40,{floor_y} 360,{floor_y} 380,280 20,280" fill="{floor_color}"/>
      <polygon points="40,60 40,{floor_y} 20,280 20,90" fill="rgba(0,0,0,0.20)"/>
      <polygon points="360,60 360,{floor_y} 380,280 380,90" fill="rgba(0,0,0,0.20)"/>
      <!-- 地板木纹 -->
      <line x1="60" y1="{floor_y + 18}" x2="340" y2="{floor_y + 18}" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
      <line x1="50" y1="{floor_y + 42}" x2="350" y2="{floor_y + 42}" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
    '''


def sofa(g, x=120, y=190, w=160, h=44, color="rgba(255,255,255,0.22)"):
    """现代沙发"""
    return f'''
      <!-- 沙发主体 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" stroke="rgba(255,255,255,0.5)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 沙发靠背 -->
      <rect x="{x}" y="{y - 14}" width="{w}" height="22" rx="10" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.4)" stroke-width="1.4"/>
      <!-- 沙发抱枕 -->
      <rect x="{x + 8}" y="{y + 6}" width="40" height="26" rx="6" fill="rgba(0,212,255,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="{x + w - 48}" y="{y + 6}" width="40" height="26" rx="6" fill="rgba(255,120,180,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
    '''


def tv_wall(g, x=150, y=70, w=100, h=58):
    """电视墙 + 电视"""
    return f'''
      <!-- 电视背景墙 -->
      <rect x="{x - 12}" y="{y - 8}" width="{w + 24}" height="{h + 20}" rx="4" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.4)" stroke-width="1.6"/>
      <!-- 电视 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(0,0,0,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 电视屏幕光晕 -->
      <rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="2" fill="rgba(0,212,255,0.18)"/>
      <!-- 电视支架 -->
      <line x1="{x + w//2}" y1="{y + h}" x2="{x + w//2}" y2="{y + h + 6}" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
      <rect x="{x + w//2 - 18}" y="{y + h + 6}" width="36" height="4" rx="1" fill="rgba(255,255,255,0.45)"/>
    '''


def coffee_table(g, x=170, y=200, w=60, h=10):
    """茶几"""
    return f'''
      <!-- 茶几 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(255,255,255,0.35)" stroke="rgba(255,255,255,0.55)" stroke-width="1.4" filter="url(#{g}_shadow)"/>
      <rect x="{x + 4}" y="{y + h}" width="6" height="22" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <rect x="{x + w - 10}" y="{y + h}" width="6" height="22" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <!-- 茶几上的花瓶 -->
      <rect x="{x + w//2 - 4}" y="{y - 14}" width="8" height="14" rx="2" fill="rgba(255,120,180,0.5)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <circle cx="{x + w//2}" cy="{y - 18}" r="5" fill="rgba(0,255,128,0.55)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
    '''


def floor_lamp(g, x=78, y_top=70, y_bottom=210):
    """落地灯"""
    return f'''
      <!-- 落地灯灯罩 -->
      <path d="M {x - 14} {y_top + 18} L {x + 14} {y_top + 18} L {x + 8} {y_top} L {x - 8} {y_top} Z" fill="rgba(255,240,200,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.6" filter="url(#{g}_glow)"/>
      <!-- 灯杆 -->
      <line x1="{x}" y1="{y_top + 18}" x2="{x}" y2="{y_bottom}" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
      <!-- 灯座 -->
      <ellipse cx="{x}" cy="{y_bottom + 2}" rx="12" ry="3" fill="rgba(255,255,255,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <!-- 灯光晕染 -->
      <circle cx="{x}" cy="{y_top + 10}" r="22" fill="rgba(255,240,200,0.18)"/>
    '''


def plant(g, x=300, y=170, height=50):
    """绿植"""
    pot_h = 22
    pot_w = 20
    return f'''
      <!-- 花盆 -->
      <path d="M {x - pot_w//2} {y + height - pot_h} L {x + pot_w//2} {y + height - pot_h} L {x + pot_w//2 - 2} {y + height} L {x - pot_w//2 + 2} {y + height} Z" fill="rgba(255,255,255,0.30)" stroke="rgba(255,255,255,0.5)" stroke-width="1.4"/>
      <!-- 植物叶子 -->
      <ellipse cx="{x}" cy="{y + 8}" rx="18" ry="22" fill="rgba(0,255,128,0.45)" stroke="rgba(255,255,255,0.5)" stroke-width="1.4"/>
      <ellipse cx="{x - 12}" cy="{y + 14}" rx="10" ry="16" fill="rgba(0,255,128,0.40)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <ellipse cx="{x + 12}" cy="{y + 14}" rx="10" ry="16" fill="rgba(0,255,128,0.40)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <ellipse cx="{x}" cy="{y + 2}" rx="9" ry="14" fill="rgba(0,255,128,0.55)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
    '''


def wall_art(g, x=70, y=80, w=42, h=52):
    """墙画装饰"""
    return f'''
      <!-- 画框 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="rgba(255,255,255,0.20)" stroke="rgba(255,255,255,0.6)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 画内容：抽象色块 -->
      <rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h//2 - 2}" fill="rgba(0,212,255,0.4)"/>
      <rect x="{x + 4}" y="{y + h//2 + 2}" width="{w - 8}" height="{h//2 - 6}" fill="rgba(255,120,180,0.4)"/>
      <circle cx="{x + w//2}" cy="{y + h//2}" r="6" fill="rgba(255,240,200,0.6)"/>
    '''


def bookshelf(g, x=240, y=70, w=80, h=140):
    """书架（全屋定制风格）"""
    books = []
    # 4 层书架
    for i in range(4):
        shelf_y = y + i * (h // 4) + 6
        # 隔板
        books.append(f'<line x1="{x}" y1="{shelf_y + (h//4 - 8)}" x2="{x + w}" y2="{shelf_y + (h//4 - 8)}" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>')
        # 书本
        bx = x + 4
        for j in range(7):
            bw = 6 + (j % 3)
            bh = (h // 4 - 12) - (j % 4) * 3
            colors = ["rgba(0,212,255,0.5)", "rgba(255,120,180,0.5)", "rgba(0,255,128,0.5)", "rgba(255,200,80,0.5)", "rgba(180,140,255,0.5)"]
            books.append(f'<rect x="{bx}" y="{shelf_y + (h//4 - 8) - bh - 2}" width="{bw}" height="{bh}" fill="{colors[j % 5]}" stroke="rgba(255,255,255,0.5)" stroke-width="0.8"/>')
            bx += bw + 1
    books_svg = "\n      ".join(books)
    return f'''
      <!-- 书架外框（玻璃拟态定制柜） -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.55)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 玻璃门反光 -->
      <line x1="{x + 4}" y1="{y + 4}" x2="{x + w - 8}" y2="{y + 30}" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
      <!-- 书本 -->
      {books_svg}
    '''


def desk(g, x=80, y=160, w=160, h=10):
    """书桌"""
    return f'''
      <!-- 桌面 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="rgba(255,255,255,0.32)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 桌腿 -->
      <rect x="{x + 4}" y="{y + h}" width="8" height="42" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
      <rect x="{x + w - 12}" y="{y + h}" width="8" height="42" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
      <!-- 抽屉 -->
      <rect x="{x + w - 60}" y="{y + h + 4}" width="48" height="34" rx="2" fill="rgba(255,255,255,0.16)" stroke="rgba(255,255,255,0.4)" stroke-width="1.2"/>
      <line x1="{x + w - 36}" y1="{y + h + 18}" x2="{x + w - 24}" y2="{y + h + 18}" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
    '''


def chair(g, x=130, y=180):
    """椅子"""
    return f'''
      <!-- 椅座 -->
      <rect x="{x}" y="{y}" width="50" height="8" rx="2" fill="rgba(255,255,255,0.28)" stroke="rgba(255,255,255,0.5)" stroke-width="1.4"/>
      <!-- 椅腿 -->
      <line x1="{x + 4}" y1="{y + 8}" x2="{x + 4}" y2="{y + 30}" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <line x1="{x + 46}" y1="{y + 8}" x2="{x + 46}" y2="{y + 30}" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <!-- 椅背 -->
      <path d="M {x} {y} q 2 -16 25 -16 q 23 0 25 16" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
    '''


def custom_cabinet(g, x=70, y=80, w=80, h=130, doors=3):
    """全屋定制柜体"""
    door_w = (w - 8) / doors
    doors_svg = []
    for i in range(doors):
        dx = x + 4 + i * door_w
        doors_svg.append(f'<rect x="{dx}" y="{y + 4}" width="{door_w - 2}" height="{h - 8}" rx="2" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>')
        doors_svg.append(f'<circle cx="{dx + door_w - 6}" cy="{y + h//2}" r="1.6" fill="rgba(255,255,255,0.7)"/>')
        # 内部玻璃反光
        doors_svg.append(f'<line x1="{dx + 2}" y1="{y + 6}" x2="{dx + door_w - 4}" y2="{y + 30}" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>')
    doors_str = "\n      ".join(doors_svg)
    return f'''
      <!-- 定制柜外框 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.55)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 柜门 -->
      {doors_str}
      <!-- 顶部台面 -->
      <rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="6" rx="1" fill="rgba(255,255,255,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1.2"/>
    '''


def wardrobe(g, x=240, y=60, w=120, h=180):
    """衣柜（全屋定制）"""
    # 4扇柜门
    door_w = (w - 8) / 4
    doors_svg = []
    for i in range(4):
        dx = x + 4 + i * door_w
        doors_svg.append(f'<rect x="{dx}" y="{y + 4}" width="{door_w - 2}" height="{h - 8}" rx="2" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>')
        # 长把手
        doors_svg.append(f'<line x1="{dx + door_w - 5}" y1="{y + 30}" x2="{dx + door_w - 5}" y2="{y + h - 30}" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>')
        # 玻璃反光
        doors_svg.append(f'<line x1="{dx + 2}" y1="{y + 8}" x2="{dx + door_w - 4}" y2="{y + 40}" stroke="rgba(255,255,255,0.28)" stroke-width="1"/>')
    doors_str = "\n      ".join(doors_svg)
    return f'''
      <!-- 衣柜外框 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.55)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 柜门 -->
      {doors_str}
      <!-- 顶部装饰条 -->
      <rect x="{x - 2}" y="{y - 3}" width="{w + 4}" height="4" rx="1" fill="rgba(255,255,255,0.40)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
    '''


def kitchen_counter(g, x=70, y=180, w=270, h=12):
    """厨房台面"""
    # 下柜
    cabinet = f'''
      <rect x="{x}" y="{y + h}" width="{w}" height="40" rx="2" fill="rgba(255,255,255,0.16)" stroke="rgba(255,255,255,0.45)" stroke-width="1.4"/>
      <line x1="{x + w//3}" y1="{y + h}" x2="{x + w//3}" y2="{y + h + 40}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <line x1="{x + 2 * w//3}" y1="{y + h}" x2="{x + 2 * w//3}" y2="{y + h + 40}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <circle cx="{x + w//6}" cy="{y + h + 20}" r="1.6" fill="rgba(255,255,255,0.7)"/>
      <circle cx="{x + w//2}" cy="{y + h + 20}" r="1.6" fill="rgba(255,255,255,0.7)"/>
      <circle cx="{x + 5 * w//6}" cy="{y + h + 20}" r="1.6" fill="rgba(255,255,255,0.7)"/>'''
    # 台面（大理石质感）
    counter = f'''
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="rgba(255,255,255,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4" filter="url(#{g}_shadow)"/>
      <!-- 大理石纹理 -->
      <path d="M {x + 20} {y + 4} q 30 -2 60 4 q 30 4 50 -2" fill="none" stroke="rgba(0,0,0,0.10)" stroke-width="1"/>
      <path d="M {x + 100} {y + 8} q 40 -4 80 2" fill="none" stroke="rgba(0,0,0,0.10)" stroke-width="1"/>'''
    # 水槽 + 水龙头
    sink = f'''
      <rect x="{x + 30}" y="{y + 2}" width="40" height="8" rx="2" fill="rgba(0,0,0,0.30)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <path d="M {x + 50} {y - 16} L {x + 50} {y} L {x + 56} {y} L {x + 56} {y - 14}" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.6"/>'''
    # 灶台
    stove = f'''
      <rect x="{x + w - 80}" y="{y + 2}" width="60" height="8" rx="1" fill="rgba(0,0,0,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <circle cx="{x + w - 65}" cy="{y + 6}" r="2" fill="rgba(255,120,80,0.6)"/>
      <circle cx="{x + w - 50}" cy="{y + 6}" r="2" fill="rgba(255,120,80,0.6)"/>
      <circle cx="{x + w - 35}" cy="{y + 6}" r="2" fill="rgba(255,120,80,0.6)"/>'''
    return cabinet + counter + sink + stove


def upper_cabinets(g, x=70, y=70, w=270, h=60):
    """厨房上吊柜"""
    doors = 4
    door_w = (w - 8) / doors
    doors_svg = []
    for i in range(doors):
        dx = x + 4 + i * door_w
        doors_svg.append(f'<rect x="{dx}" y="{y + 4}" width="{door_w - 2}" height="{h - 8}" rx="2" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>')
        doors_svg.append(f'<line x1="{dx + door_w - 5}" y1="{y + 14}" x2="{dx + door_w - 5}" y2="{y + h - 14}" stroke="rgba(255,255,255,0.6)" stroke-width="1.2"/>')
    doors_str = "\n      ".join(doors_svg)
    return f'''
      <!-- 上吊柜 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.55)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      {doors_str}'''


def bed(g, x=120, y=170, w=160, h=50):
    """床"""
    return f'''
      <!-- 床头板 -->
      <rect x="{x}" y="{y - 30}" width="{w}" height="32" rx="6" fill="rgba(255,255,255,0.20)" stroke="rgba(255,255,255,0.5)" stroke-width="1.6"/>
      <!-- 床垫 -->
      <rect x="{x - 4}" y="{y}" width="{w + 8}" height="{h}" rx="4" fill="rgba(255,255,255,0.32)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 被子 -->
      <path d="M {x + 4} {y + h//2} L {x + w - 4} {y + h//2} L {x + w - 4} {y + h - 4} L {x + 4} {y + h - 4} Z" fill="rgba(0,212,255,0.30)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <!-- 枕头 -->
      <rect x="{x + 10}" y="{y - 4}" width="40" height="14" rx="3" fill="rgba(255,255,255,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.2"/>
      <rect x="{x + w - 50}" y="{y - 4}" width="40" height="14" rx="3" fill="rgba(255,255,255,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.2"/>
    '''


def eco_panel(g, x=80, y=110, w=240, h=100):
    """环保板材展示"""
    panels = []
    # 3 块板材
    for i in range(3):
        px = x + i * (w // 3) + 8
        # 板材
        panels.append(f'<rect x="{px}" y="{y}" width="{w//3 - 16}" height="{h - 30}" rx="2" fill="rgba(255,200,140,0.40)" stroke="rgba(255,255,255,0.6)" stroke-width="1.6" filter="url(#{g}_shadow)"/>')
        # 木纹
        panels.append(f'<line x1="{px + 4}" y1="{y + 14}" x2="{px + w//3 - 20}" y2="{y + 14}" stroke="rgba(0,0,0,0.15)" stroke-width="1"/>')
        panels.append(f'<line x1="{px + 4}" y1="{y + 28}" x2="{px + w//3 - 20}" y2="{y + 28}" stroke="rgba(0,0,0,0.12)" stroke-width="1"/>')
        panels.append(f'<line x1="{px + 4}" y1="{y + 42}" x2="{px + w//3 - 20}" y2="{y + 42}" stroke="rgba(0,0,0,0.10)" stroke-width="1"/>')
        # 环保标识（叶子）
        cx = px + (w//3 - 16) // 2
        cy = y + h - 50
        panels.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="rgba(0,255,128,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>')
        panels.append(f'<path d="M {cx - 4} {cy + 1} q 4 -8 8 0 q -4 6 -8 0 Z" fill="rgba(255,255,255,0.85)"/>')
        # E0 标签
        labels = ["E0", "ENF", "E1"]
        panels.append(f'<text x="{cx}" y="{y + h - 18}" text-anchor="middle" font-size="10" font-weight="700" fill="white" font-family="sans-serif">{labels[i]}</text>')
    panels_str = "\n      ".join(panels)
    return panels_str


def smart_panel(g, x=70, y=80, w=80, h=60):
    """智能家居控制屏"""
    return f'''
      <!-- 控制屏 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="rgba(0,0,0,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 屏幕状态点 -->
      <circle cx="{x + 16}" cy="{y + 18}" r="5" fill="none" stroke="rgba(0,255,128,0.9)" stroke-width="1.8"/>
      <circle cx="{x + 16}" cy="{y + 18}" r="2" fill="rgba(0,255,128,0.9)" filter="url(#{g}_glow)"/>
      <!-- 状态条 -->
      <rect x="{x + 28}" y="{y + 14}" width="{w - 36}" height="4" rx="2" fill="rgba(0,212,255,0.6)"/>
      <rect x="{x + 28}" y="{y + 22}" width="{w - 50}" height="4" rx="2" fill="rgba(255,255,255,0.4)"/>
      <rect x="{x + 28}" y="{y + 30}" width="{w - 60}" height="4" rx="2" fill="rgba(0,255,128,0.5)"/>
      <!-- 控制图标 -->
      <circle cx="{x + 18}" cy="{y + 48}" r="4" fill="rgba(255,200,80,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <circle cx="{x + 40}" cy="{y + 48}" r="4" fill="rgba(0,212,255,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <circle cx="{x + 62}" cy="{y + 48}" r="4" fill="rgba(255,120,180,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
    '''


def certificate(g, x=120, y=70, w=160, h=120):
    """证书/认证"""
    return f'''
      <!-- 证书背景 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(255,255,255,0.20)" stroke="rgba(255,240,200,0.85)" stroke-width="2" filter="url(#{g}_shadow)"/>
      <!-- 金色边框 -->
      <rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" rx="2" fill="none" stroke="rgba(255,200,80,0.7)" stroke-width="1.4"/>
      <!-- 顶部装饰 -->
      <path d="M {x + w//2 - 16} {y + 14} l 4 8 l 8 1 l -6 6 l 2 8 l -8 -4 l -8 4 l 2 -8 l -6 -6 l 8 -1 z" fill="rgba(255,220,120,0.85)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <!-- 标题条 -->
      <rect x="{x + 30}" y="{y + 36}" width="{w - 60}" height="6" rx="2" fill="rgba(255,200,80,0.7)"/>
      <!-- 内容线条 -->
      <line x1="{x + 24}" y1="{y + 58}" x2="{x + w - 24}" y2="{y + 58}" stroke="rgba(255,255,255,0.55)" stroke-width="1"/>
      <line x1="{x + 30}" y1="{y + 70}" x2="{x + w - 30}" y2="{y + 70}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <line x1="{x + 30}" y1="{y + 80}" x2="{x + w - 40}" y2="{y + 80}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <!-- 认证印章 -->
      <circle cx="{x + w - 28}" cy="{y + h - 26}" r="14" fill="rgba(255,80,80,0.55)" stroke="rgba(255,200,200,0.85)" stroke-width="1.6"/>
      <path d="M {x + w - 36} {y + h - 26} l 5 5 l 8 -10" fill="none" stroke="white" stroke-width="1.6" stroke-linecap="round"/>
      <!-- 丝带 -->
      <path d="M {x + 30} {y + h} L {x + 22} {y + h + 18} L {x + 30} {y + h + 12} L {x + 38} {y + h + 18} Z" fill="rgba(255,120,80,0.55)" stroke="rgba(255,255,255,0.6)" stroke-width="1.2"/>
    '''


def trophy(g, x=200, y=80):
    """奖杯"""
    return f'''
      <!-- 奖杯杯身 -->
      <path d="M {x - 24} {y} L {x + 24} {y} L {x + 20} {y + 36} q -4 14 -20 14 q -16 0 -20 -14 Z" fill="rgba(255,220,120,0.65)" stroke="rgba(255,255,255,0.85)" stroke-width="2" filter="url(#{g}_shadow)"/>
      <!-- 奖杯把手 -->
      <path d="M {x - 24} {y + 6} q -14 2 -12 16 q 2 8 12 6" fill="none" stroke="rgba(255,220,120,0.65)" stroke-width="2"/>
      <path d="M {x + 24} {y + 6} q 14 2 12 16 q -2 8 -12 6" fill="none" stroke="rgba(255,220,120,0.65)" stroke-width="2"/>
      <!-- 奖杯底座 -->
      <rect x="{x - 8}" y="{y + 50}" width="16" height="14" fill="rgba(255,255,255,0.35)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <rect x="{x - 18}" y="{y + 64}" width="36" height="6" rx="2" fill="rgba(255,255,255,0.45)" stroke="rgba(255,255,255,0.65)" stroke-width="1.4"/>
      <!-- 星星 -->
      <path d="M {x} {y + 14} l 3 7 l 7 1 l -5 5 l 1 7 l -6 -3 l -6 3 l 1 -7 l -5 -5 l 7 -1 z" fill="rgba(255,255,255,0.85)" stroke="rgba(255,200,80,0.7)" stroke-width="1"/>
    '''


def designer_team(g, x=80, y=120, count=4):
    """设计师团队（人物剪影）"""
    people = []
    spacing = 60
    for i in range(count):
        px = x + i * spacing
        # 头
        people.append(f'<circle cx="{px}" cy="{y}" r="9" fill="rgba(255,255,255,0.45)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>')
        # 身体
        people.append(f'<path d="M {px - 14} {y + 36} q 0 -22 14 -22 q 14 0 14 22 Z" fill="rgba(255,255,255,0.30)" stroke="rgba(255,255,255,0.55)" stroke-width="1.4"/>')
        # 衣服细节（领带/颜色变化）
        colors = ["rgba(0,212,255,0.4)", "rgba(255,120,180,0.4)", "rgba(0,255,128,0.4)", "rgba(255,200,80,0.4)"]
        people.append(f'<rect x="{px - 2}" y="{y + 16}" width="4" height="18" fill="{colors[i % 4]}"/>')
    people_str = "\n      ".join(people)
    # 演示板
    board = f'''
      <!-- 演示板/投影屏 -->
      <rect x="60" y="60" width="280" height="42" rx="3" fill="rgba(255,255,255,0.16)" stroke="rgba(255,255,255,0.6)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <rect x="68" y="68" width="60" height="4" rx="1" fill="rgba(0,212,255,0.6)"/>
      <rect x="68" y="78" width="100" height="3" rx="1" fill="rgba(255,255,255,0.4)"/>
      <rect x="68" y="86" width="80" height="3" rx="1" fill="rgba(255,255,255,0.3)"/>
      <rect x="180" y="68" width="40" height="26" rx="2" fill="rgba(0,255,128,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="230" y="68" width="40" height="26" rx="2" fill="rgba(255,120,180,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="280" y="68" width="50" height="26" rx="2" fill="rgba(255,200,80,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>'''
    return board + "\n      " + people_str


def installation_worker(g, x=80, y=160):
    """安装工人 + 柜体"""
    # 工人
    worker = f'''
      <!-- 工人剪影 -->
      <circle cx="{x}" cy="{y - 30}" r="8" fill="rgba(255,200,80,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <!-- 安全帽 -->
      <path d="M {x - 12} {y - 32} q 12 -14 24 0 Z" fill="rgba(255,200,80,0.85)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <rect x="{x - 13}" y="{y - 33}" width="26" height="3" rx="1" fill="rgba(255,200,80,0.85)"/>
      <!-- 身体（工装） -->
      <path d="M {x - 14} {y - 8} q 0 -16 14 -16 q 14 0 14 16 L {x + 14} {y + 16} L {x - 14} {y + 16} Z" fill="rgba(0,212,255,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <!-- 工具腰带 -->
      <rect x="{x - 14}" y="{y + 6}" width="28" height="4" fill="rgba(255,120,80,0.65)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <!-- 工具 -->
      <rect x="{x + 14}" y="{y - 4}" width="14" height="3" fill="rgba(255,255,255,0.6)"/>'''
    # 半安装的柜体
    cabinet = custom_cabinet(g, x=170, y=80, w=100, h=130, doors=2)
    # 工具箱
    toolbox = f'''
      <rect x="270" y="190" width="36" height="22" rx="2" fill="rgba(255,160,80,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <path d="M 280 190 q 0 -8 8 -8 q 8 0 8 8" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <line x1="278" y1="200" x2="298" y2="200" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>'''
    return worker + cabinet + toolbox


def chart_trend(g, x=80, y=80, w=240, h=120):
    """趋势图表"""
    return f'''
      <!-- 图表背景 -->
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.5)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 坐标轴 -->
      <line x1="{x + 20}" y1="{y + h - 16}" x2="{x + w - 12}" y2="{y + h - 16}" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <line x1="{x + 20}" y1="{y + 12}" x2="{x + 20}" y2="{y + h - 16}" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <!-- 柱状图 -->
      <rect x="{x + 36}" y="{y + h - 50}" width="22" height="34" rx="1" fill="rgba(0,212,255,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="{x + 70}" y="{y + h - 64}" width="22" height="48" rx="1" fill="rgba(0,255,128,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="{x + 104}" y="{y + h - 78}" width="22" height="62" rx="1" fill="rgba(255,200,80,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="{x + 138}" y="{y + h - 92}" width="22" height="76" rx="1" fill="rgba(255,120,180,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <rect x="{x + 172}" y="{y + h - 104}" width="22" height="88" rx="1" fill="rgba(180,140,255,0.6)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <!-- 趋势线 -->
      <path d="M {x + 47} {y + h - 56} L {x + 81} {y + h - 70} L {x + 115} {y + h - 84} L {x + 149} {y + h - 98} L {x + 183} {y + h - 110}" fill="none" stroke="rgba(255,255,255,0.85)" stroke-width="2" stroke-linejoin="round"/>
      <!-- 数据点 -->
      <circle cx="{x + 47}" cy="{y + h - 56}" r="3" fill="white"/>
      <circle cx="{x + 81}" cy="{y + h - 70}" r="3" fill="white"/>
      <circle cx="{x + 115}" cy="{y + h - 84}" r="3" fill="white"/>
      <circle cx="{x + 149}" cy="{y + h - 98}" r="3" fill="white"/>
      <circle cx="{x + 183}" cy="{y + h - 110}" r="3" fill="rgba(0,255,128,0.9)" filter="url(#{g}_glow)"/>
    '''


def checklist(g, x=70, y=80, w=140, h=140):
    """避坑指南清单"""
    items = []
    for i in range(5):
        iy = y + 10 + i * 24
        # 复选框
        items.append(f'<rect x="{x}" y="{iy}" width="14" height="14" rx="2" fill="rgba(0,255,128,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>')
        # 勾
        items.append(f'<path d="M {x + 3} {iy + 7} l 3 3 l 5 -6" fill="none" stroke="white" stroke-width="1.6" stroke-linecap="round"/>')
        # 文字线
        items.append(f'<rect x="{x + 22}" y="{iy + 4}" width="{w - 30}" height="3" rx="1" fill="rgba(255,255,255,0.5)"/>')
        items.append(f'<rect x="{x + 22}" y="{iy + 10}" width="{w - 50}" height="3" rx="1" fill="rgba(255,255,255,0.3)"/>')
    items_str = "\n      ".join(items)
    return f'''
      <!-- 清单卡片 -->
      <rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" rx="6" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      {items_str}
    '''


def warning_icon(g, x=240, y=120):
    """警示图标"""
    return f'''
      <!-- 警示三角 -->
      <path d="M {x} {y + 50} L {x + 50} {y + 50} L {x + 25} {y} Z" fill="rgba(255,200,80,0.65)" stroke="rgba(255,255,255,0.85)" stroke-width="2" filter="url(#{g}_shadow)"/>
      <!-- 感叹号 -->
      <rect x="{x + 23}" y="{y + 14}" width="4" height="22" rx="1" fill="white"/>
      <circle cx="{x + 25}" cy="{y + 42}" r="2.5" fill="white"/>
    '''


def small_apartment_layout(g):
    """小户型多功能空间"""
    # 紧凑布局：上下铺/折叠桌/收纳墙
    return f'''
      <!-- 多功能墙（收纳组合） -->
      <rect x="60" y="70" width="100" height="140" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 上层搁板 -->
      <rect x="66" y="76" width="88" height="22" rx="2" fill="rgba(0,212,255,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="70" y="80" width="20" height="14" rx="1" fill="rgba(255,120,180,0.5)"/>
      <rect x="92" y="80" width="20" height="14" rx="1" fill="rgba(0,255,128,0.5)"/>
      <rect x="114" y="80" width="20" height="14" rx="1" fill="rgba(255,200,80,0.5)"/>
      <!-- 中层挂衣杆 -->
      <rect x="66" y="106" width="88" height="30" rx="2" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <line x1="70" y1="118" x2="150" y2="118" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <path d="M 78 118 L 76 132 L 84 132 L 82 118" fill="rgba(180,140,255,0.55)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <path d="M 100 118 L 98 132 L 106 132 L 104 118" fill="rgba(255,120,180,0.55)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <path d="M 122 118 L 120 132 L 128 132 L 126 118" fill="rgba(0,212,255,0.55)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <!-- 下层抽屉 -->
      <rect x="66" y="142" width="88" height="62" rx="2" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <line x1="66" y1="173" x2="154" y2="173" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <circle cx="110" cy="160" r="1.8" fill="rgba(255,255,255,0.7)"/>
      <circle cx="110" cy="187" r="1.8" fill="rgba(255,255,255,0.7)"/>

      <!-- 折叠书桌 -->
      <rect x="200" y="160" width="120" height="8" rx="2" fill="rgba(255,255,255,0.35)" stroke="rgba(255,255,255,0.55)" stroke-width="1.4" filter="url(#{g}_shadow)"/>
      <line x1="206" y1="168" x2="206" y2="200" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <line x1="314" y1="168" x2="314" y2="200" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <!-- 桌面笔记本 -->
      <rect x="224" y="146" width="48" height="14" rx="1" fill="rgba(0,0,0,0.4)" stroke="rgba(255,255,255,0.6)" stroke-width="1.2"/>
      <rect x="228" y="150" width="40" height="6" rx="1" fill="rgba(0,212,255,0.45)"/>
      <!-- 折叠椅 -->
      <rect x="280" y="172" width="22" height="4" rx="1" fill="rgba(255,255,255,0.4)"/>
      <line x1="282" y1="176" x2="282" y2="194" stroke="rgba(255,255,255,0.5)" stroke-width="1.6"/>
      <line x1="298" y1="176" x2="298" y2="194" stroke="rgba(255,255,255,0.5)" stroke-width="1.6"/>

      <!-- 收纳盒（角落） -->
      <rect x="320" y="180" width="40" height="20" rx="2" fill="rgba(255,200,80,0.45)" stroke="rgba(255,255,255,0.55)" stroke-width="1.2"/>
      <rect x="324" y="184" width="32" height="3" rx="1" fill="rgba(255,255,255,0.5)"/>
    '''


def budget_calc(g, x=80, y=80):
    """预算计算"""
    # 计算器
    calc = f'''
      <!-- 计算器 -->
      <rect x="{x}" y="{y}" width="100" height="130" rx="6" fill="rgba(0,0,0,0.45)" stroke="rgba(255,255,255,0.65)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 屏幕 -->
      <rect x="{x + 8}" y="{y + 8}" width="84" height="24" rx="2" fill="rgba(0,255,128,0.35)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <text x="{x + 86}" y="{y + 26}" text-anchor="end" font-size="14" font-weight="700" fill="rgba(255,255,255,0.95)" font-family="monospace">¥38,800</text>
      <!-- 按键 -->
      <g>'''
    # 4x4 按键
    keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "+", "C", "0", "=", "-"]
    for i, k in enumerate(keys):
        row = i // 4
        col = i % 4
        kx = x + 10 + col * 21
        ky = y + 40 + row * 22
        color = "rgba(255,255,255,0.18)" if k.isdigit() else ("rgba(0,212,255,0.45)" if k in "÷×+-=" else "rgba(255,80,80,0.5)")
        calc += f'<rect x="{kx}" y="{ky}" width="18" height="18" rx="3" fill="{color}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/><text x="{kx + 9}" y="{ky + 13}" text-anchor="middle" font-size="10" font-weight="600" fill="white" font-family="monospace">{k}</text>'
    calc += '</g>'
    # 蓝图 + 算盘式预算明细
    blueprint = f'''
      <!-- 蓝图卷 -->
      <rect x="220" y="{y + 20}" width="120" height="80" rx="3" fill="rgba(0,212,255,0.20)" stroke="rgba(255,255,255,0.6)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 蓝图内容 -->
      <line x1="228" y1="{y + 32}" x2="332" y2="{y + 32}" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <line x1="228" y1="{y + 42}" x2="320" y2="{y + 42}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <line x1="228" y1="{y + 52}" x2="332" y2="{y + 52}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <line x1="228" y1="{y + 62}" x2="310" y2="{y + 62}" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <!-- 户型图标识 -->
      <rect x="240" y="{y + 70}" width="34" height="22" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <rect x="280" y="{y + 70}" width="20" height="14" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <!-- 饼图 -->
      <circle cx="300" cy="{y + 110}" r="22" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>
      <path d="M 300 {y + 88} A 22 22 0 0 1 321 {y + 114} L 300 {y + 110} Z" fill="rgba(0,212,255,0.55)"/>
      <path d="M 321 {y + 114} A 22 22 0 0 1 287 {y + 122} L 300 {y + 110} Z" fill="rgba(0,255,128,0.55)"/>
      <path d="M 287 {y + 122} A 22 22 0 0 1 300 {y + 88} L 300 {y + 110} Z" fill="rgba(255,200,80,0.55)"/>'''
    return calc + blueprint


def order_signing(g):
    """订单签约场景：合同 + 握手 + 房屋钥匙"""
    return f'''
      <!-- 桌面 -->
      <rect x="50" y="170" width="300" height="8" rx="2" fill="rgba(255,255,255,0.30)" stroke="rgba(255,255,255,0.5)" stroke-width="1.4" filter="url(#{g}_shadow)"/>
      <rect x="56" y="178" width="6" height="36" fill="rgba(255,255,255,0.22)"/>
      <rect x="338" y="178" width="6" height="36" fill="rgba(255,255,255,0.22)"/>

      <!-- 合同文件 -->
      <rect x="80" y="120" width="120" height="60" rx="2" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.7)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <line x1="90" y1="132" x2="190" y2="132" stroke="rgba(0,0,0,0.25)" stroke-width="1"/>
      <line x1="90" y1="140" x2="180" y2="140" stroke="rgba(0,0,0,0.18)" stroke-width="1"/>
      <line x1="90" y1="148" x2="184" y2="148" stroke="rgba(0,0,0,0.18)" stroke-width="1"/>
      <line x1="90" y1="156" x2="170" y2="156" stroke="rgba(0,0,0,0.18)" stroke-width="1"/>
      <!-- 合同印章 -->
      <circle cx="180" cy="168" r="8" fill="rgba(255,80,80,0.65)" stroke="rgba(255,200,200,0.8)" stroke-width="1.2"/>

      <!-- 笔 -->
      <line x1="210" y1="148" x2="240" y2="148" stroke="rgba(255,255,255,0.8)" stroke-width="2.4"/>
      <path d="M 240 148 L 246 145 L 246 151 Z" fill="rgba(255,255,255,0.9)"/>

      <!-- 房屋钥匙/钥匙扣 -->
      <circle cx="290" cy="135" r="12" fill="none" stroke="rgba(255,200,80,0.85)" stroke-width="2.4" filter="url(#{g}_glow)"/>
      <rect x="300" y="132" width="30" height="6" rx="1" fill="rgba(255,200,80,0.85)" stroke="rgba(255,255,255,0.7)" stroke-width="1"/>
      <rect x="320" y="138" width="4" height="6" fill="rgba(255,200,80,0.85)"/>
      <rect x="326" y="138" width="4" height="6" fill="rgba(255,200,80,0.85)"/>

      <!-- 全屋定制户型图（背景装饰） -->
      <g opacity="0.45">
        <rect x="200" y="80" width="120" height="36" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
        <line x1="240" y1="80" x2="240" y2="116" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
        <line x1="280" y1="80" x2="280" y2="116" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
        <text x="260" y="102" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.85)" font-family="'Noto Sans SC', sans-serif">户型图</text>
      </g>
    '''


def style_grid(g):
    """风格展示网格（5大风格）"""
    # 5 个小卡片代表 5 种风格
    styles = [
        {"name": "简约", "color": "rgba(0,212,255,0.4)", "icon_color": "rgba(255,255,255,0.7)"},
        {"name": "轻奢", "color": "rgba(255,200,80,0.5)", "icon_color": "rgba(255,255,255,0.7)"},
        {"name": "北欧", "color": "rgba(0,255,128,0.4)", "icon_color": "rgba(255,255,255,0.7)"},
        {"name": "新中式", "color": "rgba(255,120,180,0.45)", "icon_color": "rgba(255,255,255,0.7)"},
        {"name": "侘寂", "color": "rgba(180,140,255,0.4)", "icon_color": "rgba(255,255,255,0.7)"}
    ]
    cards = []
    card_w = 64
    card_h = 80
    spacing = 8
    total_w = 5 * card_w + 4 * spacing
    start_x = (400 - total_w) // 2
    for i, s in enumerate(styles):
        s_color = s["color"]
        s_name = s["name"]
        s_icon = s["icon_color"]
        cx = start_x + i * (card_w + spacing)
        cy = 100
        cards.append(f'<rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" rx="4" fill="{s_color}" stroke="rgba(255,255,255,0.65)" stroke-width="1.4" filter="url(#{g}_shadow)"/>')
        # 风格小图（沙发剪影）
        cards.append(f'<rect x="{cx + 10}" y="{cy + 14}" width="{card_w - 20}" height="20" rx="3" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>')
        cards.append(f'<rect x="{cx + 12}" y="{cy + 10}" width="{card_w - 24}" height="6" rx="2" fill="rgba(255,255,255,0.35)"/>')
        # 风格名称
        cards.append(f'<text x="{cx + card_w//2}" y="{cy + 56}" text-anchor="middle" font-size="11" font-weight="700" fill="white" font-family="\'Noto Sans SC\', sans-serif">{s_name}</text>')
        # 装饰条
        cards.append(f'<rect x="{cx + 16}" y="{cy + 66}" width="{card_w - 32}" height="3" rx="1" fill="{s_icon}"/>')
    cards_str = "\n      ".join(cards)
    return cards_str


def workshop_scene(g):
    """工坊/工艺场景"""
    return f'''
      <!-- 工作台 -->
      <rect x="50" y="180" width="300" height="10" rx="2" fill="rgba(255,200,140,0.55)" stroke="rgba(255,255,255,0.7)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <rect x="58" y="190" width="6" height="32" fill="rgba(255,255,255,0.3)"/>
      <rect x="336" y="190" width="6" height="32" fill="rgba(255,255,255,0.3)"/>

      <!-- 板材（半成品） -->
      <rect x="70" y="150" width="100" height="30" rx="2" fill="rgba(255,200,140,0.55)" stroke="rgba(255,255,255,0.65)" stroke-width="1.4"/>
      <line x1="80" y1="160" x2="160" y2="160" stroke="rgba(0,0,0,0.18)" stroke-width="1"/>
      <line x1="80" y1="170" x2="160" y2="170" stroke="rgba(0,0,0,0.15)" stroke-width="1"/>
      <!-- 切割线 -->
      <line x1="100" y1="150" x2="100" y2="180" stroke="rgba(255,80,80,0.7)" stroke-width="1" stroke-dasharray="3 2"/>
      <line x1="140" y1="150" x2="140" y2="180" stroke="rgba(255,80,80,0.7)" stroke-width="1" stroke-dasharray="3 2"/>

      <!-- 精密切割机 -->
      <rect x="190" y="135" width="80" height="45" rx="4" fill="rgba(0,0,0,0.5)" stroke="rgba(255,255,255,0.7)" stroke-width="1.8" filter="url(#{g}_shadow)"/>
      <!-- 显示屏 -->
      <rect x="200" y="142" width="36" height="20" rx="2" fill="rgba(0,255,128,0.4)" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
      <line x1="204" y1="148" x2="232" y2="148" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <line x1="204" y1="156" x2="226" y2="156" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
      <!-- 控制旋钮 -->
      <circle cx="252" cy="155" r="6" fill="rgba(255,200,80,0.6)" stroke="rgba(255,255,255,0.7)" stroke-width="1.2"/>
      <line x1="252" y1="150" x2="252" y2="155" stroke="white" stroke-width="1.4"/>

      <!-- 工具挂板 -->
      <rect x="290" y="80" width="80" height="80" rx="3" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.5)" stroke-width="1.4"/>
      <!-- 挂着的工具 -->
      <rect x="298" y="92" width="6" height="22" rx="1" fill="rgba(255,200,80,0.6)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <rect x="312" y="92" width="6" height="22" rx="1" fill="rgba(0,212,255,0.6)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <rect x="326" y="92" width="6" height="22" rx="1" fill="rgba(255,120,180,0.6)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <rect x="340" y="92" width="6" height="22" rx="1" fill="rgba(0,255,128,0.6)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <rect x="354" y="92" width="6" height="22" rx="1" fill="rgba(180,140,255,0.6)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <!-- 第二排 -->
      <circle cx="304" cy="138" r="8" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <circle cx="324" cy="138" r="8" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>
      <rect x="340" y="130" width="20" height="6" rx="2" fill="rgba(255,255,255,0.4)"/>

      <!-- 木屑/碎料（地板装饰） -->
      <rect x="70" y="220" width="14" height="3" rx="1" fill="rgba(255,200,140,0.5)" transform="rotate(15 77 221)"/>
      <rect x="100" y="225" width="10" height="3" rx="1" fill="rgba(255,200,140,0.5)" transform="rotate(-20 105 226)"/>
      <rect x="200" y="220" width="12" height="3" rx="1" fill="rgba(255,200,140,0.5)" transform="rotate(30 206 221)"/>
    '''


def kids_room_scene(g):
    """儿童房场景"""
    # 童趣色彩 + 圆角家具
    return f'''
      <!-- 儿童床（带护栏） -->
      <rect x="60" y="160" width="120" height="40" rx="6" fill="rgba(255,120,180,0.40)" stroke="rgba(255,255,255,0.7)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 床围栏 -->
      <path d="M 60 160 q 0 -30 14 -30 q 14 0 14 30" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
      <path d="M 60 160 q 0 -30 14 -30 q 14 0 14 30" fill="rgba(255,255,255,0.18)"/>
      <path d="M 88 160 q 0 -30 14 -30 q 14 0 14 30" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
      <path d="M 88 160 q 0 -30 14 -30 q 14 0 14 30" fill="rgba(255,255,255,0.18)"/>
      <path d="M 116 160 q 0 -30 14 -30 q 14 0 14 30" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
      <path d="M 116 160 q 0 -30 14 -30 q 14 0 14 30" fill="rgba(255,255,255,0.18)"/>
      <path d="M 144 160 q 0 -30 14 -30 q 14 0 14 30" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
      <path d="M 144 160 q 0 -30 14 -30 q 14 0 14 30" fill="rgba(255,255,255,0.18)"/>
      <!-- 床垫 -->
      <rect x="64" y="164" width="112" height="14" rx="3" fill="rgba(0,212,255,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
      <!-- 枕头 -->
      <rect x="70" y="166" width="22" height="10" rx="3" fill="rgba(255,255,255,0.7)"/>

      <!-- 玩具熊 -->
      <circle cx="130" cy="156" r="9" fill="rgba(255,200,80,0.65)" stroke="rgba(255,255,255,0.7)" stroke-width="1.2"/>
      <circle cx="125" cy="148" r="3" fill="rgba(255,200,80,0.65)"/>
      <circle cx="135" cy="148" r="3" fill="rgba(255,200,80,0.65)"/>
      <circle cx="127" cy="156" r="1" fill="rgba(0,0,0,0.5)"/>
      <circle cx="133" cy="156" r="1" fill="rgba(0,0,0,0.5)"/>

      <!-- 圆角书桌 -->
      <rect x="200" y="160" width="80" height="6" rx="3" fill="rgba(0,255,128,0.5)" stroke="rgba(255,255,255,0.65)" stroke-width="1.4"/>
      <line x1="206" y1="166" x2="206" y2="195" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <line x1="274" y1="166" x2="274" y2="195" stroke="rgba(255,255,255,0.5)" stroke-width="1.8"/>
      <!-- 桌面书本 -->
      <rect x="216" y="148" width="20" height="12" rx="1" fill="rgba(255,120,180,0.6)" stroke="rgba(255,255,255,0.55)" stroke-width="1"/>
      <rect x="238" y="150" width="20" height="10" rx="1" fill="rgba(0,212,255,0.6)" stroke="rgba(255,255,255,0.55)" stroke-width="1"/>

      <!-- 玩具收纳柜（圆角） -->
      <rect x="295" y="100" width="80" height="100" rx="8" fill="rgba(255,200,80,0.30)" stroke="rgba(255,255,255,0.65)" stroke-width="1.6" filter="url(#{g}_shadow)"/>
      <!-- 收纳格 -->
      <rect x="302" y="108" width="32" height="30" rx="4" fill="rgba(255,120,180,0.5)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="338" y="108" width="32" height="30" rx="4" fill="rgba(0,212,255,0.5)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="302" y="142" width="32" height="30" rx="4" fill="rgba(0,255,128,0.5)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="338" y="142" width="32" height="30" rx="4" fill="rgba(180,140,255,0.5)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
      <rect x="302" y="176" width="68" height="20" rx="4" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>

      <!-- 星星装饰 -->
      <path d="M 230 70 l 2 5 l 5 1 l -4 4 l 1 5 l -4 -2 l -4 2 l 1 -5 l -4 -4 l 5 -1 z" fill="rgba(255,240,120,0.8)" stroke="rgba(255,255,255,0.6)" stroke-width="0.8"/>
      <path d="M 110 80 l 1.5 4 l 4 0.8 l -3 3 l 0.8 4 l -3.3 -1.6 l -3.3 1.6 l 0.8 -4 l -3 -3 l 4 -0.8 z" fill="rgba(255,120,180,0.8)" stroke="rgba(255,255,255,0.6)" stroke-width="0.8"/>
      <!-- 云朵 -->
      <ellipse cx="320" cy="80" rx="22" ry="9" fill="rgba(255,255,255,0.32)"/>
      <ellipse cx="310" cy="76" rx="14" ry="7" fill="rgba(255,255,255,0.28)"/>
    '''


# ============================================================================
# 场景类型 -> 颜色 + 元素组合
# ============================================================================

SCENE_DEFS = {
    # 装修设计类 - 客厅场景（暖色紫红渐变）
    "living_room": {
        "colors": ("#667eea", "#764ba2"),
        "accent": "#00d4ff",
        "category": "装修设计",
        "scene": lambda g: room_perspective(g, 210) +
                          tv_wall(g, 150, 70, 100, 58) +
                          floor_lamp(g, 78, 70, 210) +
                          sofa(g, 120, 178, 160, 38) +
                          coffee_table(g, 170, 200) +
                          plant(g, 310, 168, 50) +
                          wall_art(g, 70, 78, 36, 48)
    },
    # 全屋定制 - 衣柜卧室
    "wardrobe_bedroom": {
        "colors": ("#4facfe", "#00f2fe"),
        "accent": "#7b2ff7",
        "category": "全屋定制",
        "scene": lambda g: room_perspective(g, 200) +
                          wardrobe(g, 240, 60, 120, 180) +
                          bed(g, 80, 175, 140, 40) +
                          floor_lamp(g, 230, 80, 200) +
                          wall_art(g, 80, 80, 36, 48)
    },
    # 全屋定制 - 书房
    "study_room": {
        "colors": ("#a18cd1", "#fbc2eb"),
        "accent": "#00ff80",
        "category": "全屋定制",
        "scene": lambda g: room_perspective(g, 210) +
                          bookshelf(g, 250, 70, 80, 140) +
                          desk(g, 80, 160, 160, 10) +
                          chair(g, 130, 180) +
                          floor_lamp(g, 78, 80, 210) +
                          # 桌面物品
                          '\n      <!-- 桌面物品 -->\n      <rect x="100" y="146" width="40" height="14" rx="1" fill="rgba(255,255,255,0.30)" stroke="rgba(255,255,255,0.55)" stroke-width="1.2"/>\n      <line x1="120" y1="146" x2="120" y2="160" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>\n      <path d="M 170 138 L 186 138 L 182 120 L 174 120 Z" fill="rgba(255,240,200,0.55)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>\n      <line x1="178" y1="138" x2="178" y2="160" stroke="rgba(255,255,255,0.5)" stroke-width="1.4"/>'
    },
    # 全屋定制 - 厨房
    "kitchen": {
        "colors": ("#fa709a", "#fee140"),
        "accent": "#00d4ff",
        "category": "全屋定制",
        "scene": lambda g: room_perspective(g, 180) +
                          upper_cabinets(g, 70, 70, 270, 60) +
                          kitchen_counter(g, 70, 180, 270, 12) +
                          # 厨房岛台装饰
                          '\n      <!-- 厨房岛台 -->\n      <rect x="140" y="200" width="120" height="36" rx="2" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6"/>\n      <rect x="136" y="194" width="128" height="6" rx="1" fill="rgba(255,255,255,0.45)" stroke="rgba(255,255,255,0.6)" stroke-width="1.2"/>'
    },
    # 全屋定制 - 儿童房
    "kids_room": {
        "colors": ("#ff9a9e", "#fad0c4"),
        "accent": "#00d4ff",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 儿童房背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n      <polygon points="40,60 40,210 20,280 20,90" fill="rgba(0,0,0,0.20)"/>\n      <polygon points="360,60 360,210 380,280 380,90" fill="rgba(0,0,0,0.20)"/>\n' + kids_room_scene(g)
    },
    # 全屋定制 - 小户型
    "small_apartment": {
        "colors": ("#5f27cd", "#341f97"),
        "accent": "#00ff80",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 小户型墙面 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n      <polygon points="40,60 40,210 20,280 20,90" fill="rgba(0,0,0,0.20)"/>\n      <polygon points="360,60 360,210 380,280 380,90" fill="rgba(0,0,0,0.20)"/>\n' + small_apartment_layout(g)
    },
    # 全屋定制 - 风格指南
    "style_guide": {
        "colors": ("#f093fb", "#f5576c"),
        "accent": "#00d4ff",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 风格展示墙背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.08)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + style_grid(g)
    },
    # 全屋定制 - 材料升级（环保板材）
    "eco_materials": {
        "colors": ("#43e97b", "#38f9d7"),
        "accent": "#7b2ff7",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 材料展示墙背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + eco_panel(g, 80, 90, 240, 110)
    },
    # 全屋定制 - 流程/安装
    "installation": {
        "colors": ("#00d4ff", "#0099cc"),
        "accent": "#ff6b6b",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 安装场景墙面 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + installation_worker(g, 80, 160)
    },
    # 全屋定制 - 工艺/工坊
    "workshop": {
        "colors": ("#ee0979", "#ff6a00"),
        "accent": "#00d4ff",
        "category": "全屋定制",
        "scene": lambda g: '\n      <!-- 工坊墙面 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + workshop_scene(g)
    },
    # 智能家居 + 全屋定制
    "smart_home_custom": {
        "colors": ("#0abde3", "#48dbfb"),
        "accent": "#00ff80",
        "category": "行业资讯",
        "scene": lambda g: room_perspective(g, 210) +
                          smart_panel(g, 70, 80, 80, 60) +
                          tv_wall(g, 175, 75, 90, 50) +
                          sofa(g, 120, 180, 160, 36) +
                          coffee_table(g, 170, 202) +
                          plant(g, 310, 168, 50) +
                          # 智能音箱
                          '\n      <!-- 智能音箱 -->\n      <rect x="92" y="178" width="22" height="32" rx="5" fill="rgba(255,255,255,0.20)" stroke="rgba(255,255,255,0.55)" stroke-width="1.6"/>\n      <circle cx="103" cy="188" r="4" fill="none" stroke="rgba(0,212,255,0.85)" stroke-width="1.4"/>\n      <circle cx="103" cy="188" r="1.6" fill="rgba(0,212,255,0.85)" filter="url(#' + g + '_glow)"/>\n      <line x1="96" y1="200" x2="110" y2="200" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>\n      <line x1="96" y1="204" x2="110" y2="204" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>\n      <!-- 信号波 -->\n      <path d="M 116 188 q 8 -8 16 0" fill="none" stroke="rgba(0,255,128,0.7)" stroke-width="1.4"/>\n      <path d="M 118 196 q 6 -6 12 0" fill="none" stroke="rgba(0,255,128,0.5)" stroke-width="1.2"/>'
    },
    # 智能家居项目（公司动态）
    "smart_home_project": {
        "colors": ("#fa709a", "#fee140"),
        "accent": "#00d4ff",
        "category": "公司动态",
        "scene": lambda g: room_perspective(g, 210) +
                          smart_panel(g, 70, 80, 80, 60) +
                          tv_wall(g, 175, 75, 90, 50) +
                          sofa(g, 120, 180, 160, 36) +
                          # 手机控制
                          '\n      <!-- 手机控制智能家居 -->\n      <rect x="280" y="170" width="22" height="36" rx="4" fill="rgba(0,0,0,0.45)" stroke="rgba(255,255,255,0.65)" stroke-width="1.6"/>\n      <rect x="284" y="174" width="14" height="8" rx="1" fill="rgba(0,212,255,0.55)"/>\n      <rect x="284" y="184" width="14" height="3" rx="1" fill="rgba(255,255,255,0.4)"/>\n      <rect x="284" y="190" width="14" height="3" rx="1" fill="rgba(0,255,128,0.45)"/>\n      <!-- 信号连接 -->\n      <path d="M 270 175 q -20 -10 -50 -10" fill="none" stroke="rgba(0,255,128,0.5)" stroke-width="1.2" stroke-dasharray="3 2"/>\n      <path d="M 270 185 q -30 0 -60 0" fill="none" stroke="rgba(0,212,255,0.5)" stroke-width="1.2" stroke-dasharray="3 2"/>'
    },
    # 公司动态 - 认证奖项
    "certification_award": {
        "colors": ("#fa709a", "#fee140"),
        "accent": "#00d4ff",
        "category": "公司动态",
        "scene": lambda g: '\n      <!-- 荣誉墙背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + certificate(g, 80, 80, 140, 110) + trophy(g, 250, 90) +
                          '\n      <!-- 奖章装饰 -->\n      <circle cx="320" cy="170" r="20" fill="rgba(255,200,80,0.50)" stroke="rgba(255,255,255,0.75)" stroke-width="1.8"/>\n      <circle cx="320" cy="170" r="12" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.4"/>\n      <path d="M 308 188 L 304 218 L 320 210 L 336 218 L 332 188 Z" fill="rgba(255,120,80,0.50)" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>\n      <text x="320" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="white" font-family="sans-serif">A+</text>'
    },
    # 公司动态 - 设计师培训
    "designer_training": {
        "colors": ("#11998e", "#38ef7d"),
        "accent": "#00d4ff",
        "category": "公司动态",
        "scene": lambda g: '\n      <!-- 培训场景背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + designer_team(g, 80, 130, 4)
    },
    # 公司动态 - 订单签约
    "order_signing": {
        "colors": ("#00d4ff", "#0099cc"),
        "accent": "#ff6b6b",
        "category": "公司动态",
        "scene": lambda g: '\n      <!-- 签约场景背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + order_signing(g)
    },
    # 行业资讯 - 趋势分析
    "trend_analysis": {
        "colors": ("#f7971e", "#ffd200"),
        "accent": "#7b2ff7",
        "category": "行业资讯",
        "scene": lambda g: '\n      <!-- 趋势分析背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + chart_trend(g, 80, 80, 240, 120)
    },
    # 行业资讯 - 避坑指南
    "checklist_guide": {
        "colors": ("#ee0979", "#ff6a00"),
        "accent": "#00d4ff",
        "category": "行业资讯",
        "scene": lambda g: '\n      <!-- 避坑指南背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + checklist(g, 70, 80, 140, 140) + warning_icon(g, 250, 110)
    },
    # 行业资讯 - 环保材料
    "eco_industry": {
        "colors": ("#134e5e", "#71b280"),
        "accent": "#00d4ff",
        "category": "行业资讯",
        "scene": lambda g: '\n      <!-- 环保材料背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + eco_panel(g, 80, 90, 240, 110) +
                          '\n      <!-- 环保标识 -->\n      <circle cx="320" cy="80" r="18" fill="rgba(0,255,128,0.40)" stroke="rgba(255,255,255,0.7)" stroke-width="1.6" filter="url(#' + g + '_glow)"/>\n      <path d="M 312 80 q 8 -14 16 0 q -8 -4 -16 0 Z" fill="rgba(255,255,255,0.85)"/>\n      <text x="320" y="116" text-anchor="middle" font-size="9" font-weight="600" fill="white" font-family="sans-serif">ECO</text>'
    },
    # 行业资讯 - 预算计算
    "budget_calc": {
        "colors": ("#614385", "#516395"),
        "accent": "#00ff80",
        "category": "行业资讯",
        "scene": lambda g: '\n      <!-- 预算计算背景 -->\n      <rect x="40" y="60" width="320" height="150" fill="rgba(255,255,255,0.10)"/>\n      <polygon points="40,210 360,210 380,280 20,280" fill="rgba(0,0,0,0.18)"/>\n' + budget_calc(g, 80, 80)
    },
}


# ============================================================================
# 新闻 ID -> 场景类型映射（基于标题内容）
# ============================================================================

def select_scene(item):
    """根据新闻条目内容选择合适的场景"""
    title = item.get('title', '')
    category = item.get('category', '')
    excerpt = item.get('excerpt', '')

    # 标题关键词匹配
    if '客厅' in title and ('布局' in title or '装修' in title):
        return 'living_room'
    if '儿童房' in title:
        return 'kids_room'
    if '书房' in title:
        return 'study_room'
    if '厨房' in title:
        return 'kitchen'
    if '小户型' in title:
        return 'small_apartment'
    if '风格' in title and ('指南' in title or '解析' in title):
        return 'style_guide'
    if '材料升级' in title or '环保板材' in title:
        return 'eco_materials'
    if '工艺升级' in title or '工艺' in title:
        return 'workshop'
    if '安装' in title or '流程' in title:
        return 'installation'
    if '智能家居' in title and '融合' in title:
        return 'smart_home_custom'
    if '智能家居项目' in title or '锦绣花园' in title:
        return 'smart_home_project'
    if ('认证' in title or '荣获' in title) and '品质' in title:
        return 'certification_award'
    if '优秀室内设计企业' in title:
        return 'certification_award'
    if '培训' in title or '学习' in title or '设计师团队' in title:
        return 'designer_training'
    if '订单' in title and ('新增' in title or '签约' in title):
        return 'order_signing'
    if '趋势' in title and ('风格' in title or '流行' in title):
        return 'trend_analysis'
    if '避坑' in title or '注意事项' in title:
        return 'checklist_guide'
    if '环保材料' in title or '环保' in title:
        return 'eco_industry'
    if '预算' in title:
        return 'budget_calc'

    # 备选：根据分类
    if category == '全屋定制':
        return 'wardrobe_bedroom'
    if category == '装修设计':
        return 'living_room'
    if category == '公司动态':
        return 'order_signing'
    if category == '行业资讯':
        return 'trend_analysis'
    return 'living_room'


# ============================================================================
# 生成函数
# ============================================================================

def generate_news_svg(item):
    """为单条新闻生成 SVG"""
    news_id = str(item['id'])
    scene_type = select_scene(item)
    scene_def = SCENE_DEFS[scene_type]

    color_a, color_b = scene_def["colors"]
    accent = scene_def["accent"]
    category_label = scene_def["category"]

    gradient_id = f"news_{news_id}"

    # 调用场景生成器
    scene_svg = scene_def["scene"](gradient_id)

    return svg_skeleton(
        gradient_id, color_a, color_b, accent,
        scene_svg, category_label
    )


def main():
    """主函数：为所有新闻重新生成增强版 SVG"""
    # 读取新闻数据
    with open(NEWS_DATA_FILE, 'r', encoding='utf-8') as f:
        news_data = json.load(f)

    print(f"📋 读取到 {len(news_data)} 条新闻记录")
    print(f"📂 输出目录: {NEWS_IMAGES_DIR}")
    print(f"=" * 60)

    os.makedirs(NEWS_IMAGES_DIR, exist_ok=True)

    # 场景统计
    scene_stats = {}

    for item in news_data:
        news_id = str(item['id'])
        title = item['title']
        scene_type = select_scene(item)

        # 生成 SVG
        svg_content = generate_news_svg(item)

        # 写入文件
        filename = f"news_{news_id}.svg"
        filepath = os.path.join(NEWS_IMAGES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        # 统计
        scene_stats[scene_type] = scene_stats.get(scene_type, 0) + 1

        print(f"✓ [{scene_type:20s}] {filename} - {title[:32]}")

    print(f"=" * 60)
    print(f"✅ 已生成 {len(news_data)} 张增强版 SVG 图片")
    print(f"\n📊 场景类型统计：")
    for scene, count in sorted(scene_stats.items(), key=lambda x: -x[1]):
        print(f"   - {scene:20s}: {count} 张")

    # 验证文件
    svg_files = [f for f in os.listdir(NEWS_IMAGES_DIR) if f.endswith('.svg')]
    print(f"\n📁 目录中共有 {len(svg_files)} 个 SVG 文件")


if __name__ == '__main__':
    main()
