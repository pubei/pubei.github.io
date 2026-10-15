#!/usr/bin/env python3
"""
为所有公司新闻生成与"装修设计 / 全屋定制"内容相关的本地 SVG 场景插画。
- 按标题关键词匹配具体场景(客厅/厨房/卧室/儿童房/书房/工艺车间/环保材料等)
- 用 SVG 矢量绘制可识别的室内场景,本地存储保证稳定显示
- 同步把 news-data.json 与 news.html 中的 .jpg 引用修复回 .svg
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DATA = os.path.join(BASE_DIR, 'assets', 'data', 'news-data.json')
NEWS_HTML = os.path.join(BASE_DIR, 'news.html')
IMG_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'news')

# 分类 -> 配色(渐变两端 + 副标题)
CATEGORY_THEMES = {
    '装修设计': {'grad': ['#4facfe', '#00f2fe'], 'subtitle': '装修设计 · 匠心品质'},
    '全屋定制': {'grad': ['#a18cd1', '#fbc2eb'], 'subtitle': '全屋定制 · 专属定制'},
    '公司动态': {'grad': ['#fa709a', '#fee140'], 'subtitle': '公司动态 · 品质承诺'},
    '行业资讯': {'grad': ['#30cfd0', '#330867'], 'subtitle': '行业资讯 · 前沿洞察'},
}
DEFAULT_THEME = {'grad': ['#667eea', '#764ba2'], 'subtitle': '浦北装修设计 · 专业品质'}


# ============ 场景插画生成器 ============
# 每个函数返回一段 <g>...</g> SVG,绘制于中心区域(x:70-330, y:55-190)
# 统一样式:白色描边 + 半透明填充,叠加在渐变背景上

def scene_living_room():
    """客厅:沙发+茶几+电视+绿植+落地灯"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 电视墙 -->
      <rect x="150" y="58" width="100" height="58" rx="4" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <rect x="158" y="66" width="84" height="42" rx="2" fill="rgba(0,0,0,0.25)" stroke="white" stroke-width="1.2"/>
      <line x1="180" y1="120" x2="220" y2="120" stroke="white" stroke-width="2"/>
      <rect x="188" y="120" width="24" height="6" fill="white" opacity="0.7"/>
      <!-- 落地灯 -->
      <line x1="92" y1="78" x2="92" y2="178" stroke="white" stroke-width="2"/>
      <path d="M 78 78 L 106 78 L 100 60 L 84 60 Z" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="2"/>
      <circle cx="92" cy="180" r="4" fill="white" opacity="0.7"/>
      <!-- 沙发 -->
      <rect x="120" y="140" width="160" height="40" rx="10" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
      <rect x="120" y="128" width="160" height="22" rx="8" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <rect x="124" y="150" width="44" height="22" rx="6" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <rect x="178" y="150" width="44" height="22" rx="6" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <rect x="232" y="150" width="44" height="22" rx="6" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <!-- 茶几 -->
      <rect x="170" y="172" width="60" height="10" rx="3" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <!-- 绿植 -->
      <path d="M 300 168 L 300 184 L 320 184 L 320 168 Z" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.6"/>
      <circle cx="310" cy="158" r="14" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1.6"/>
      <circle cx="300" cy="150" r="9" fill="rgba(0,255,128,0.25)" stroke="white" stroke-width="1.4"/>
      <circle cx="320" cy="150" r="9" fill="rgba(0,255,128,0.25)" stroke="white" stroke-width="1.4"/>
    </g>'''


def scene_children_room():
    """儿童房:床+玩具箱+小书桌+云朵+星星"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 云朵 -->
      <path d="M 80 70 q 8 -14 20 -8 q 4 -10 14 -6 q 10 -4 14 6 q 10 -2 12 8 z" fill="rgba(255,255,255,0.18)" stroke="white" stroke-width="1.4"/>
      <path d="M 270 64 q 7 -12 18 -7 q 5 -9 14 -5 q 9 -3 12 6 q 8 -1 10 7 z" fill="rgba(255,255,255,0.18)" stroke="white" stroke-width="1.4"/>
      <!-- 星星 -->
      <path d="M 150 80 l 2 6 l 6 2 l -6 2 l -2 6 l -2 -6 l -6 -2 l 6 -2 z" fill="white" opacity="0.8"/>
      <path d="M 250 92 l 1.6 4.8 l 4.8 1.6 l -4.8 1.6 l -1.6 4.8 l -1.6 -4.8 l -4.8 -1.6 l 4.8 -1.6 z" fill="white" opacity="0.7"/>
      <!-- 床 -->
      <rect x="90" y="150" width="120" height="34" rx="6" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
      <rect x="90" y="138" width="22" height="46" rx="8" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <rect x="118" y="156" width="84" height="22" rx="4" fill="rgba(255,200,220,0.30)" stroke="white" stroke-width="1.4"/>
      <!-- 玩具熊 -->
      <circle cx="132" cy="150" r="9" fill="rgba(255,210,170,0.5)" stroke="white" stroke-width="1.4"/>
      <circle cx="126" cy="144" r="3" fill="rgba(255,210,170,0.5)" stroke="white" stroke-width="1.2"/>
      <circle cx="138" cy="144" r="3" fill="rgba(255,210,170,0.5)" stroke="white" stroke-width="1.2"/>
      <!-- 玩具箱 -->
      <rect x="226" y="158" width="80" height="26" rx="4" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
      <line x1="226" y1="166" x2="306" y2="166" stroke="white" stroke-width="1.4"/>
      <circle cx="266" cy="162" r="3" fill="white" opacity="0.7"/>
      <!-- 小书桌 -->
      <rect x="232" y="116" width="64" height="6" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <line x1="240" y1="122" x2="240" y2="148" stroke="white" stroke-width="2"/>
      <line x1="288" y1="122" x2="288" y2="148" stroke="white" stroke-width="2"/>
      <!-- 球 -->
      <circle cx="218" cy="180" r="7" fill="rgba(0,212,255,0.35)" stroke="white" stroke-width="1.4"/>
    </g>'''


def scene_kitchen():
    """厨房:橱柜+台面+灶台+油烟机+锅"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 油烟机 -->
      <path d="M 150 60 L 250 60 L 244 84 L 156 84 Z" fill="rgba(255,255,255,0.18)" stroke="white" stroke-width="2"/>
      <rect x="170" y="84" width="60" height="8" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.4"/>
      <!-- 上橱柜 -->
      <rect x="86" y="92" width="60" height="40" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="2"/>
      <line x1="116" y1="92" x2="116" y2="132" stroke="white" stroke-width="1.4"/>
      <circle cx="110" cy="112" r="2" fill="white" opacity="0.8"/>
      <circle cx="122" cy="112" r="2" fill="white" opacity="0.8"/>
      <rect x="254" y="92" width="60" height="40" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="2"/>
      <line x1="284" y1="92" x2="284" y2="132" stroke="white" stroke-width="1.4"/>
      <circle cx="278" cy="112" r="2" fill="white" opacity="0.8"/>
      <circle cx="290" cy="112" r="2" fill="white" opacity="0.8"/>
      <!-- 台面 -->
      <rect x="78" y="148" width="244" height="10" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.6"/>
      <!-- 下橱柜 -->
      <rect x="86" y="158" width="228" height="32" rx="3" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="2"/>
      <line x1="162" y1="158" x2="162" y2="190" stroke="white" stroke-width="1.4"/>
      <line x1="238" y1="158" x2="238" y2="190" stroke="white" stroke-width="1.4"/>
      <circle cx="120" cy="174" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="196" cy="174" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="272" cy="174" r="2.5" fill="white" opacity="0.8"/>
      <!-- 灶台 -->
      <circle cx="170" cy="138" r="9" fill="rgba(0,0,0,0.25)" stroke="white" stroke-width="1.6"/>
      <circle cx="170" cy="138" r="3" fill="rgba(255,120,80,0.6)"/>
      <circle cx="220" cy="138" r="9" fill="rgba(0,0,0,0.25)" stroke="white" stroke-width="1.6"/>
      <circle cx="220" cy="138" r="3" fill="rgba(255,120,80,0.6)"/>
      <!-- 锅 -->
      <path d="M 250 132 q 16 0 16 10 l -4 6 -24 0 -4 -6 q 16 -10 16 -10 z" fill="rgba(255,255,255,0.22)" stroke="white" stroke-width="1.6"/>
      <!-- 蒸汽 -->
      <path d="M 256 122 q -4 -6 0 -10 q 4 -4 0 -8" fill="none" stroke="white" stroke-width="1.4" opacity="0.5"/>
      <path d="M 262 120 q -4 -6 0 -10 q 4 -4 0 -8" fill="none" stroke="white" stroke-width="1.4" opacity="0.5"/>
    </g>'''


def scene_bedroom():
    """卧室:床+衣柜+床头柜+台灯+挂画"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 衣柜 -->
      <rect x="260" y="74" width="64" height="116" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="2"/>
      <line x1="292" y1="74" x2="292" y2="190" stroke="white" stroke-width="1.4"/>
      <line x1="260" y1="120" x2="324" y2="120" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <circle cx="284" cy="132" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="300" cy="132" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="284" cy="160" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="300" cy="160" r="2.5" fill="white" opacity="0.8"/>
      <!-- 挂画 -->
      <rect x="92" y="74" width="56" height="40" rx="2" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.6"/>
      <circle cx="108" cy="90" r="6" fill="rgba(0,212,255,0.4)" stroke="white" stroke-width="1"/>
      <path d="M 120 108 L 132 92 L 140 108 Z" fill="rgba(0,255,128,0.35)" stroke="white" stroke-width="1"/>
      <!-- 床头板 -->
      <rect x="78" y="118" width="150" height="14" rx="6" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <!-- 床 -->
      <rect x="78" y="132" width="160" height="40" rx="6" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
      <!-- 枕头 -->
      <rect x="86" y="136" width="44" height="14" rx="4" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="86" y="152" width="140" height="16" rx="4" fill="rgba(220,230,255,0.25)" stroke="white" stroke-width="1.4"/>
      <!-- 床头柜 + 台灯 -->
      <rect x="232" y="150" width="26" height="22" rx="2" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.6"/>
      <path d="M 240 142 L 250 142 L 248 130 L 242 130 Z" fill="rgba(255,220,120,0.4)" stroke="white" stroke-width="1.4"/>
      <line x1="245" y1="142" x2="245" y2="150" stroke="white" stroke-width="1.4"/>
    </g>'''


def scene_study():
    """书房:书架+书桌+椅子+台灯+书"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 书架 -->
      <rect x="262" y="64" width="62" height="126" rx="3" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="2"/>
      <line x1="262" y1="96" x2="324" y2="96" stroke="white" stroke-width="1.6"/>
      <line x1="262" y1="128" x2="324" y2="128" stroke="white" stroke-width="1.6"/>
      <line x1="262" y1="160" x2="324" y2="160" stroke="white" stroke-width="1.6"/>
      <!-- 书 -->
      <rect x="268" y="72" width="6" height="22" fill="rgba(0,212,255,0.5)" stroke="white" stroke-width="1"/>
      <rect x="276" y="72" width="6" height="22" fill="rgba(255,120,180,0.5)" stroke="white" stroke-width="1"/>
      <rect x="284" y="76" width="6" height="18" fill="rgba(0,255,128,0.5)" stroke="white" stroke-width="1"/>
      <rect x="298" y="72" width="6" height="22" fill="rgba(255,200,80,0.5)" stroke="white" stroke-width="1"/>
      <rect x="306" y="74" width="6" height="20" fill="rgba(180,140,255,0.5)" stroke="white" stroke-width="1"/>
      <rect x="270" y="104" width="6" height="22" fill="rgba(255,120,180,0.5)" stroke="white" stroke-width="1"/>
      <rect x="278" y="106" width="6" height="20" fill="rgba(0,212,255,0.5)" stroke="white" stroke-width="1"/>
      <rect x="294" y="104" width="6" height="22" fill="rgba(0,255,128,0.5)" stroke="white" stroke-width="1"/>
      <!-- 书桌 -->
      <rect x="80" y="146" width="160" height="10" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.6"/>
      <rect x="86" y="156" width="10" height="34" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.4"/>
      <rect x="224" y="156" width="10" height="34" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.4"/>
      <rect x="86" y="186" width="148" height="4" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1"/>
      <!-- 桌上书+台灯 -->
      <rect x="100" y="134" width="40" height="12" rx="1" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <line x1="120" y1="134" x2="120" y2="146" stroke="white" stroke-width="1"/>
      <path d="M 170 138 L 186 138 L 182 120 L 174 120 Z" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="1.4"/>
      <line x1="178" y1="138" x2="178" y2="146" stroke="white" stroke-width="1.4"/>
      <!-- 椅子 -->
      <rect x="130" y="160" width="50" height="6" rx="2" fill="rgba(255,255,255,0.22)" stroke="white" stroke-width="1.4"/>
      <line x1="136" y1="166" x2="136" y2="190" stroke="white" stroke-width="2"/>
      <line x1="174" y1="166" x2="174" y2="190" stroke="white" stroke-width="2"/>
      <path d="M 128 160 q 2 -14 26 -14 q 24 0 26 14" fill="none" stroke="white" stroke-width="2"/>
    </g>'''


def scene_smart_home():
    """智能家居:电视+控制屏+智能音箱+手机"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 墙面控制屏 -->
      <rect x="86" y="64" width="90" height="56" rx="6" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="2"/>
      <circle cx="104" cy="84" r="7" fill="none" stroke="#00ff80" stroke-width="2"/>
      <circle cx="104" cy="84" r="2.5" fill="#00ff80"/>
      <rect x="120" y="78" width="48" height="6" rx="2" fill="rgba(0,212,255,0.6)"/>
      <rect x="120" y="90" width="40" height="6" rx="2" fill="rgba(255,255,255,0.4)"/>
      <rect x="120" y="102" width="30" height="6" rx="2" fill="rgba(0,255,128,0.5)"/>
      <!-- 电视 -->
      <rect x="200" y="70" width="116" height="66" rx="4" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="2"/>
      <path d="M 214 96 L 232 84 L 232 108 Z" fill="rgba(0,212,255,0.6)"/>
      <rect x="236" y="86" width="60" height="6" rx="2" fill="rgba(255,255,255,0.4)"/>
      <rect x="236" y="98" width="44" height="6" rx="2" fill="rgba(255,255,255,0.3)"/>
      <rect x="236" y="110" width="52" height="6" rx="2" fill="rgba(0,255,128,0.5)"/>
      <line x1="244" y1="136" x2="272" y2="136" stroke="white" stroke-width="2"/>
      <!-- 智能音箱 -->
      <rect x="96" y="148" width="30" height="42" rx="6" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="2"/>
      <circle cx="111" cy="160" r="6" fill="none" stroke="#00d4ff" stroke-width="1.6"/>
      <circle cx="111" cy="160" r="2" fill="#00d4ff"/>
      <line x1="100" y1="176" x2="122" y2="176" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <line x1="100" y1="182" x2="122" y2="182" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <!-- 手机 -->
      <rect x="280" y="150" width="26" height="42" rx="4" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="1.8"/>
      <line x1="288" y1="156" x2="298" y2="156" stroke="white" stroke-width="1.4"/>
      <rect x="286" y="162" width="14" height="10" rx="1" fill="rgba(0,212,255,0.5)"/>
      <rect x="286" y="176" width="14" height="4" rx="1" fill="rgba(255,255,255,0.4)"/>
      <rect x="286" y="182" width="14" height="4" rx="1" fill="rgba(255,255,255,0.3)"/>
      <!-- 信号波 -->
      <path d="M 132 156 q 8 -8 16 0" fill="none" stroke="#00ff80" stroke-width="1.6" opacity="0.7"/>
      <path d="M 134 162 q 6 -6 12 0" fill="none" stroke="#00ff80" stroke-width="1.4" opacity="0.5"/>
    </g>'''


def scene_eco_materials():
    """环保材料:堆叠板材+绿叶+回收标志"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 木板材堆叠(透视) -->
      <path d="M 96 168 L 240 168 L 256 156 L 112 156 Z" fill="rgba(210,170,120,0.45)" stroke="white" stroke-width="1.8"/>
      <path d="M 112 156 L 256 156 L 256 146 L 112 146 Z" fill="rgba(210,170,120,0.35)" stroke="white" stroke-width="1.6"/>
      <path d="M 112 146 L 256 146 L 256 136 L 112 136 Z" fill="rgba(210,170,120,0.30)" stroke="white" stroke-width="1.6"/>
      <path d="M 112 136 L 256 136 L 256 126 L 112 126 Z" fill="rgba(210,170,120,0.25)" stroke="white" stroke-width="1.6"/>
      <!-- 木纹 -->
      <line x1="120" y1="162" x2="232" y2="162" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <line x1="120" y1="151" x2="232" y2="151" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <line x1="120" y1="141" x2="232" y2="141" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <!-- 立式板材 -->
      <rect x="264" y="100" width="14" height="80" rx="1" fill="rgba(210,170,120,0.4)" stroke="white" stroke-width="1.6"/>
      <rect x="280" y="92" width="14" height="88" rx="1" fill="rgba(210,170,120,0.45)" stroke="white" stroke-width="1.6"/>
      <rect x="296" y="106" width="14" height="74" rx="1" fill="rgba(210,170,120,0.4)" stroke="white" stroke-width="1.6"/>
      <line x1="266" y1="110" x2="276" y2="110" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <line x1="282" y1="102" x2="292" y2="102" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <!-- 绿叶(环保标志) -->
      <circle cx="150" cy="86" r="26" fill="rgba(0,255,128,0.20)" stroke="#00ff80" stroke-width="2"/>
      <path d="M 150 72 q 14 8 0 28 q -14 -20 0 -28 z" fill="rgba(0,255,128,0.5)" stroke="white" stroke-width="1.4"/>
      <line x1="150" y1="74" x2="150" y2="98" stroke="white" stroke-width="1.2"/>
      <!-- E0 标签 -->
      <rect x="186" y="74" width="40" height="22" rx="4" fill="rgba(0,0,0,0.30)" stroke="#00ff80" stroke-width="1.6"/>
      <text x="206" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#00ff80" font-family="'Noto Sans SC', sans-serif">E0</text>
    </g>'''


def scene_budget():
    """预算:桌面+图纸+计算器+钱币"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 桌面 -->
      <rect x="78" y="170" width="244" height="8" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <!-- 图纸(展开) -->
      <rect x="92" y="92" width="120" height="78" rx="2" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.8"/>
      <line x1="106" y1="108" x2="198" y2="108" stroke="white" stroke-width="1" opacity="0.6"/>
      <line x1="106" y1="120" x2="198" y2="120" stroke="white" stroke-width="1" opacity="0.6"/>
      <line x1="106" y1="132" x2="180" y2="132" stroke="white" stroke-width="1" opacity="0.6"/>
      <!-- 户型图线条 -->
      <rect x="112" y="138" width="40" height="24" fill="none" stroke="rgba(0,212,255,0.7)" stroke-width="1.4"/>
      <line x1="152" y1="150" x2="172" y2="150" stroke="rgba(0,212,255,0.7)" stroke-width="1.4"/>
      <rect x="172" y="138" width="20" height="24" fill="none" stroke="rgba(0,212,255,0.7)" stroke-width="1.4"/>
      <!-- 计算器 -->
      <rect x="232" y="96" width="62" height="74" rx="4" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.8"/>
      <rect x="240" y="104" width="46" height="16" rx="2" fill="rgba(0,0,0,0.35)" stroke="white" stroke-width="1"/>
      <text x="282" y="116" text-anchor="end" font-size="10" font-weight="700" fill="#00ff80" font-family="monospace">8888</text>
      <!-- 按键 -->
      <g fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1">
        <rect x="240" y="126" width="10" height="8" rx="1"/>
        <rect x="254" y="126" width="10" height="8" rx="1"/>
        <rect x="268" y="126" width="10" height="8" rx="1"/>
        <rect x="240" y="138" width="10" height="8" rx="1"/>
        <rect x="254" y="138" width="10" height="8" rx="1"/>
        <rect x="268" y="138" width="10" height="8" rx="1"/>
        <rect x="240" y="150" width="10" height="8" rx="1"/>
        <rect x="254" y="150" width="10" height="8" rx="1"/>
        <rect x="268" y="150" width="10" height="8" rx="1" fill="rgba(0,212,255,0.5)"/>
      </g>
      <!-- 钱币 -->
      <circle cx="100" cy="86" r="11" fill="rgba(255,200,80,0.45)" stroke="white" stroke-width="1.6"/>
      <text x="100" y="90" text-anchor="middle" font-size="12" font-weight="700" fill="white" font-family="sans-serif">¥</text>
      <circle cx="120" cy="78" r="8" fill="rgba(255,200,80,0.40)" stroke="white" stroke-width="1.4"/>
      <text x="120" y="81" text-anchor="middle" font-size="9" font-weight="700" fill="white" font-family="sans-serif">¥</text>
      <!-- 笔 -->
      <line x1="200" y1="84" x2="224" y2="100" stroke="white" stroke-width="2.4"/>
      <path d="M 200 84 L 196 80 L 200 84 Z" fill="white"/>
    </g>'''


def scene_delivery():
    """项目交付:钥匙+完工房间+对勾+握手"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 完工房间 -->
      <rect x="150" y="64" width="120" height="110" rx="3" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <!-- 地板 -->
      <rect x="150" y="146" width="120" height="28" fill="rgba(210,170,120,0.30)" stroke="white" stroke-width="1.4"/>
      <line x1="180" y1="146" x2="180" y2="174" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <line x1="210" y1="146" x2="210" y2="174" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <line x1="240" y1="146" x2="240" y2="174" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <!-- 窗户 -->
      <rect x="166" y="78" width="40" height="34" rx="2" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1.6"/>
      <line x1="186" y1="78" x2="186" y2="112" stroke="white" stroke-width="1.2"/>
      <line x1="166" y1="95" x2="206" y2="95" stroke="white" stroke-width="1.2"/>
      <!-- 沙发剪影 -->
      <rect x="214" y="120" width="46" height="20" rx="4" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <rect x="214" y="114" width="46" height="8" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.2"/>
      <!-- 对勾徽章 -->
      <circle cx="270" cy="84" r="20" fill="rgba(0,255,128,0.30)" stroke="#00ff80" stroke-width="2.4"/>
      <path d="M 260 84 L 268 92 L 282 76" fill="none" stroke="#00ff80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- 钥匙 -->
      <g transform="translate(96,120)">
        <circle cx="0" cy="0" r="14" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="2"/>
        <circle cx="0" cy="0" r="5" fill="rgba(0,0,0,0.4)" stroke="white" stroke-width="1.2"/>
        <rect x="13" y="-3" width="40" height="6" rx="1" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="1.8"/>
        <rect x="44" y="3" width="5" height="10" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="1.6"/>
        <rect x="35" y="3" width="5" height="8" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="1.6"/>
      </g>
    </g>'''


def scene_training():
    """培训/团队:演示屏+图表+人物+座椅"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 演示屏 -->
      <rect x="110" y="60" width="180" height="78" rx="4" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="2"/>
      <!-- 图表柱 -->
      <rect x="130" y="108" width="14" height="20" fill="rgba(0,212,255,0.6)" stroke="white" stroke-width="1"/>
      <rect x="150" y="100" width="14" height="28" fill="rgba(0,255,128,0.6)" stroke="white" stroke-width="1"/>
      <rect x="170" y="92" width="14" height="36" fill="rgba(255,200,80,0.6)" stroke="white" stroke-width="1"/>
      <rect x="190" y="84" width="14" height="44" fill="rgba(255,120,180,0.6)" stroke="white" stroke-width="1"/>
      <rect x="210" y="76" width="14" height="52" fill="rgba(180,140,255,0.6)" stroke="white" stroke-width="1"/>
      <line x1="124" y1="128" x2="232" y2="128" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <!-- 趋势线 -->
      <path d="M 137 110 L 157 102 L 177 94 L 197 86 L 217 78" fill="none" stroke="#00ff80" stroke-width="2"/>
      <!-- 屏幕支架 -->
      <line x1="186" y1="138" x2="186" y2="148" stroke="white" stroke-width="2"/>
      <rect x="170" y="148" width="32" height="5" rx="1" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.2"/>
      <!-- 人物(听众) -->
      <g stroke="white" stroke-width="1.8" fill="rgba(255,255,255,0.18)">
        <circle cx="110" cy="162" r="7"/>
        <path d="M 98 188 q 12 -16 24 0 z"/>
        <circle cx="150" cy="162" r="7"/>
        <path d="M 138 188 q 12 -16 24 0 z"/>
        <circle cx="190" cy="162" r="7"/>
        <path d="M 178 188 q 12 -16 24 0 z"/>
        <circle cx="230" cy="162" r="7"/>
        <path d="M 218 188 q 12 -16 24 0 z"/>
        <circle cx="270" cy="162" r="7"/>
        <path d="M 258 188 q 12 -16 24 0 z"/>
      </g>
    </g>'''


def scene_trends():
    """趋势/流行:客厅+上升箭头+星标"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 设计师客厅 -->
      <rect x="92" y="124" width="150" height="44" rx="8" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="2"/>
      <rect x="92" y="112" width="150" height="20" rx="6" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <rect x="100" y="134" width="40" height="22" rx="5" fill="rgba(255,120,180,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="148" y="134" width="40" height="22" rx="5" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="196" y="134" width="40" height="22" rx="5" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1.4"/>
      <!-- 茶几 -->
      <rect x="140" y="160" width="54" height="8" rx="2" fill="rgba(255,255,255,0.28)" stroke="white" stroke-width="1.4"/>
      <!-- 装饰画 -->
      <rect x="258" y="92" width="50" height="40" rx="2" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="1.6"/>
      <circle cx="272" cy="106" r="6" fill="rgba(255,200,80,0.5)" stroke="white" stroke-width="1"/>
      <path d="M 286 124 L 296 110 L 304 124 Z" fill="rgba(0,212,255,0.4)" stroke="white" stroke-width="1"/>
      <!-- 上升箭头(趋势) -->
      <path d="M 100 96 L 130 96 L 130 86 L 150 86 L 150 76 L 170 76" fill="none" stroke="#00ff80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 162 70 L 172 76 L 162 82" fill="none" stroke="#00ff80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- 星标 -->
      <path d="M 244 70 l 2.5 7 l 7 2.5 l -7 2.5 l -2.5 7 l -2.5 -7 l -7 -2.5 l 7 -2.5 z" fill="rgba(255,220,120,0.7)" stroke="white" stroke-width="1.2"/>
    </g>'''


def scene_construction():
    """施工/避坑:梯子+滚筒刷+工具+墙面"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 墙面(半刷) -->
      <rect x="92" y="60" width="120" height="130" rx="2" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.8"/>
      <rect x="92" y="60" width="120" height="70" rx="2" fill="rgba(0,212,255,0.15)" stroke="white" stroke-width="1.4"/>
      <line x1="92" y1="130" x2="212" y2="130" stroke="white" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.6"/>
      <!-- 梯子 -->
      <line x1="232" y1="190" x2="252" y2="86" stroke="white" stroke-width="2.4"/>
      <line x1="284" y1="190" x2="264" y2="86" stroke="white" stroke-width="2.4"/>
      <line x1="242" y1="120" x2="274" y2="120" stroke="white" stroke-width="2"/>
      <line x1="238" y1="140" x2="278" y2="140" stroke="white" stroke-width="2"/>
      <line x1="246" y1="100" x2="270" y2="100" stroke="white" stroke-width="2"/>
      <line x1="234" y1="160" x2="282" y2="160" stroke="white" stroke-width="2"/>
      <!-- 滚筒刷 -->
      <rect x="248" y="74" width="22" height="14" rx="3" fill="rgba(0,212,255,0.5)" stroke="white" stroke-width="1.6"/>
      <line x1="259" y1="88" x2="259" y2="100" stroke="white" stroke-width="2"/>
      <!-- 油漆桶 -->
      <path d="M 100 168 L 100 188 L 128 188 L 128 168 Z" fill="rgba(255,200,80,0.4)" stroke="white" stroke-width="1.8"/>
      <ellipse cx="114" cy="168" rx="14" ry="4" fill="rgba(255,220,120,0.5)" stroke="white" stroke-width="1.6"/>
      <path d="M 128 172 q 8 0 8 6 q 0 6 -6 6" fill="none" stroke="white" stroke-width="1.6"/>
      <!-- 工具(刷子) -->
      <rect x="148" y="150" width="8" height="26" rx="1" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="142" y="144" width="20" height="8" rx="1" fill="rgba(210,170,120,0.5)" stroke="white" stroke-width="1.4"/>
      <!-- 警示三角 -->
      <path d="M 180 178 L 200 178 L 190 160 Z" fill="rgba(255,200,80,0.4)" stroke="white" stroke-width="1.6"/>
      <line x1="190" y1="168" x2="190" y2="173" stroke="white" stroke-width="1.6"/>
      <circle cx="190" cy="176" r="0.8" fill="white"/>
    </g>'''


def scene_craftsmanship():
    """工艺:工作台+切割机+木料+齿轮"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 工作台 -->
      <rect x="80" y="158" width="240" height="10" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.6"/>
      <rect x="90" y="168" width="10" height="22" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.4"/>
      <rect x="300" y="168" width="10" height="22" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.4"/>
      <!-- 切割机 -->
      <rect x="120" y="120" width="80" height="30" rx="3" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.8"/>
      <circle cx="160" cy="150" r="14" fill="rgba(0,0,0,0.35)" stroke="white" stroke-width="1.8"/>
      <circle cx="160" cy="150" r="4" fill="rgba(0,212,255,0.6)"/>
      <line x1="160" y1="138" x2="160" y2="162" stroke="white" stroke-width="1.4"/>
      <line x1="148" y1="150" x2="172" y2="150" stroke="white" stroke-width="1.4"/>
      <!-- 木料在工作台上 -->
      <rect x="196" y="150" width="80" height="8" rx="1" fill="rgba(210,170,120,0.5)" stroke="white" stroke-width="1.4"/>
      <line x1="206" y1="150" x2="206" y2="158" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <line x1="230" y1="150" x2="230" y2="158" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <line x1="254" y1="150" x2="254" y2="158" stroke="white" stroke-width="0.8" opacity="0.5"/>
      <!-- 火花 -->
      <path d="M 174 142 L 180 138 M 176 150 L 182 150 M 174 158 L 180 162" stroke="#ffb800" stroke-width="1.4" opacity="0.8"/>
      <!-- 齿轮 -->
      <g transform="translate(280,100)">
        <circle r="20" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.8"/>
        <circle r="7" fill="rgba(0,0,0,0.35)" stroke="white" stroke-width="1.4"/>
        <g stroke="white" stroke-width="1.6" fill="rgba(255,255,255,0.20)">
          <rect x="-3" y="-26" width="6" height="8"/>
          <rect x="-3" y="18" width="6" height="8"/>
          <rect x="-26" y="-3" width="8" height="6"/>
          <rect x="18" y="-3" width="8" height="6"/>
          <rect x="-3" y="-26" width="6" height="8" transform="rotate(45)"/>
          <rect x="-3" y="18" width="6" height="8" transform="rotate(45)"/>
          <rect x="-26" y="-3" width="8" height="6" transform="rotate(45)"/>
          <rect x="18" y="-3" width="8" height="6" transform="rotate(45)"/>
        </g>
      </g>
      <!-- 卷尺/笔 -->
      <rect x="100" y="140" width="16" height="14" rx="2" fill="rgba(255,200,80,0.4)" stroke="white" stroke-width="1.4"/>
      <circle cx="108" cy="147" r="3" fill="rgba(0,0,0,0.3)"/>
    </g>'''


def scene_style():
    """风格:情绪板+色卡+家具剪影"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 情绪板背板 -->
      <rect x="84" y="62" width="232" height="116" rx="4" fill="rgba(255,255,255,0.06)" stroke="white" stroke-width="1.6"/>
      <!-- 色卡条 -->
      <rect x="96" y="74" width="22" height="60" rx="2" fill="rgba(0,212,255,0.55)" stroke="white" stroke-width="1.2"/>
      <rect x="122" y="74" width="22" height="60" rx="2" fill="rgba(0,255,128,0.55)" stroke="white" stroke-width="1.2"/>
      <rect x="148" y="74" width="22" height="60" rx="2" fill="rgba(255,200,80,0.55)" stroke="white" stroke-width="1.2"/>
      <rect x="174" y="74" width="22" height="60" rx="2" fill="rgba(255,120,180,0.55)" stroke="white" stroke-width="1.2"/>
      <rect x="200" y="74" width="22" height="60" rx="2" fill="rgba(180,140,255,0.55)" stroke="white" stroke-width="1.2"/>
      <!-- 家具剪影:椅子 -->
      <g transform="translate(240,90)" stroke="white" stroke-width="1.8" fill="rgba(255,255,255,0.18)">
        <path d="M 6 6 q 0 -10 16 -10 q 16 0 16 10 L 38 36 L 6 36 Z"/>
        <line x1="10" y1="36" x2="10" y2="56"/>
        <line x1="34" y1="36" x2="34" y2="56"/>
      </g>
      <!-- 灯具 -->
      <g transform="translate(258,74)" stroke="white" stroke-width="1.6" fill="rgba(255,220,120,0.4)">
        <path d="M 0 0 L 24 0 L 20 14 L 4 14 Z"/>
        <line x1="12" y1="14" x2="12" y2="34" stroke="white" stroke-width="1.6"/>
        <circle cx="12" cy="36" r="3" fill="rgba(255,255,255,0.5)"/>
      </g>
      <!-- 沙发剪影 -->
      <g transform="translate(96,140)" stroke="white" stroke-width="1.6" fill="rgba(255,255,255,0.18)">
        <rect x="0" y="0" width="80" height="22" rx="5"/>
        <rect x="0" y="-8" width="80" height="12" rx="4"/>
        <rect x="6" y="6" width="20" height="12" rx="3" fill="rgba(255,120,180,0.35)" stroke="white" stroke-width="1"/>
        <rect x="30" y="6" width="20" height="12" rx="3" fill="rgba(0,212,255,0.35)" stroke="white" stroke-width="1"/>
        <rect x="54" y="6" width="20" height="12" rx="3" fill="rgba(0,255,128,0.35)" stroke="white" stroke-width="1"/>
      </g>
    </g>'''


def scene_award():
    """荣获/认证:奖杯+奖章+证书+彩带"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 证书 -->
      <rect x="80" y="74" width="110" height="86" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.8"/>
      <line x1="96" y1="92" x2="174" y2="92" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <line x1="96" y1="104" x2="174" y2="104" stroke="white" stroke-width="1" opacity="0.5"/>
      <line x1="96" y1="116" x2="160" y2="116" stroke="white" stroke-width="1" opacity="0.5"/>
      <line x1="96" y1="128" x2="168" y2="128" stroke="white" stroke-width="1" opacity="0.5"/>
      <!-- 证书徽章 -->
      <circle cx="135" cy="146" r="9" fill="rgba(255,200,80,0.5)" stroke="white" stroke-width="1.6"/>
      <path d="M 130 146 L 134 150 L 141 142" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
      <!-- 奖杯 -->
      <path d="M 220 70 L 280 70 L 276 110 q -4 14 -28 14 q -24 0 -28 -14 Z" fill="rgba(255,220,120,0.45)" stroke="white" stroke-width="2"/>
      <path d="M 220 78 q -16 2 -14 18 q 2 10 14 8" fill="none" stroke="white" stroke-width="2"/>
      <path d="M 280 78 q 16 2 14 18 q -2 10 -14 8" fill="none" stroke="white" stroke-width="2"/>
      <rect x="240" y="124" width="20" height="14" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.8"/>
      <rect x="228" y="138" width="44" height="8" rx="2" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.8"/>
      <!-- 星星 -->
      <path d="M 250 86 l 3 8 l 8 1 l -6 6 l 2 8 l -7 -4 l -7 4 l 2 -8 l -6 -6 l 8 -1 z" fill="rgba(255,255,255,0.6)" stroke="white" stroke-width="1"/>
      <!-- 彩带 -->
      <path d="M 250 124 L 244 160 L 250 154 L 256 160 Z" fill="rgba(255,120,180,0.4)" stroke="white" stroke-width="1.4"/>
      <!-- 奖章 -->
      <circle cx="310" cy="120" r="18" fill="rgba(255,200,80,0.45)" stroke="white" stroke-width="2"/>
      <circle cx="310" cy="120" r="11" fill="none" stroke="white" stroke-width="1.4"/>
      <path d="M 300 138 L 296 168 L 310 160 L 324 168 L 320 138 Z" fill="rgba(255,120,80,0.4)" stroke="white" stroke-width="1.6"/>
    </g>'''


def scene_small_apartment():
    """小户型:紧凑多功能家具+收纳+扩容箭头"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 房间轮廓 -->
      <rect x="80" y="64" width="240" height="126" rx="3" fill="rgba(255,255,255,0.06)" stroke="white" stroke-width="1.8"/>
      <!-- 高柜(到顶收纳) -->
      <rect x="92" y="76" width="40" height="104" rx="2" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.8"/>
      <line x1="92" y1="102" x2="132" y2="102" stroke="white" stroke-width="1.4"/>
      <line x1="92" y1="128" x2="132" y2="128" stroke="white" stroke-width="1.4"/>
      <line x1="92" y1="154" x2="132" y2="154" stroke="white" stroke-width="1.4"/>
      <circle cx="124" cy="90" r="2" fill="white" opacity="0.7"/>
      <circle cx="124" cy="116" r="2" fill="white" opacity="0.7"/>
      <circle cx="124" cy="142" r="2" fill="white" opacity="0.7"/>
      <!-- 多功能榻榻米床+收纳 -->
      <rect x="148" y="120" width="120" height="60" rx="3" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="1.8"/>
      <rect x="148" y="120" width="120" height="16" rx="2" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.4"/>
      <rect x="156" y="144" width="30" height="30" rx="2" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="192" y="144" width="30" height="30" rx="2" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="228" y="144" width="32" height="30" rx="2" fill="rgba(255,200,80,0.30)" stroke="white" stroke-width="1.4"/>
      <!-- 折叠桌 -->
      <rect x="280" y="120" width="30" height="6" rx="1" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
      <line x1="284" y1="126" x2="284" y2="150" stroke="white" stroke-width="1.6"/>
      <line x1="306" y1="126" x2="306" y2="150" stroke="white" stroke-width="1.6"/>
      <!-- 扩容箭头 -->
      <path d="M 170 92 L 230 92" fill="none" stroke="#00ff80" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M 222 86 L 232 92 L 222 98" fill="none" stroke="#00ff80" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 250 96 L 250 84" fill="none" stroke="#00ff80" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M 244 90 L 250 84 L 256 90" fill="none" stroke="#00ff80" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    </g>'''


def scene_general_custom():
    """全屋定制:通顶衣柜+橱柜"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 通顶衣柜 -->
      <rect x="86" y="60" width="110" height="130" rx="3" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="2"/>
      <line x1="123" y1="60" x2="123" y2="190" stroke="white" stroke-width="1.6"/>
      <line x1="160" y1="60" x2="160" y2="190" stroke="white" stroke-width="1.6"/>
      <!-- 门把手 -->
      <line x1="116" y1="100" x2="116" y2="150" stroke="white" stroke-width="1.6" opacity="0.7"/>
      <line x1="130" y1="100" x2="130" y2="150" stroke="white" stroke-width="1.6" opacity="0.7"/>
      <line x1="153" y1="100" x2="153" y2="150" stroke="white" stroke-width="1.6" opacity="0.7"/>
      <line x1="167" y1="100" x2="167" y2="150" stroke="white" stroke-width="1.6" opacity="0.7"/>
      <!-- 内部分区示意 -->
      <rect x="92" y="68" width="26" height="20" rx="1" fill="rgba(0,212,255,0.25)" stroke="white" stroke-width="1"/>
      <line x1="92" y1="100" x2="118" y2="100" stroke="white" stroke-width="1" opacity="0.5"/>
      <line x1="92" y1="130" x2="118" y2="130" stroke="white" stroke-width="1" opacity="0.5"/>
      <!-- 下方定制柜+开放格 -->
      <rect x="210" y="120" width="106" height="70" rx="3" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="2"/>
      <rect x="216" y="126" width="28" height="28" rx="1" fill="rgba(0,255,128,0.25)" stroke="white" stroke-width="1"/>
      <rect x="248" y="126" width="28" height="28" rx="1" fill="rgba(255,200,80,0.25)" stroke="white" stroke-width="1"/>
      <rect x="280" y="126" width="30" height="28" rx="1" fill="rgba(255,120,180,0.25)" stroke="white" stroke-width="1"/>
      <line x1="216" y1="162" x2="310" y2="162" stroke="white" stroke-width="1.4"/>
      <circle cx="246" cy="178" r="2.5" fill="white" opacity="0.8"/>
      <circle cx="280" cy="178" r="2.5" fill="white" opacity="0.8"/>
      <!-- 上方置物架 -->
      <rect x="210" y="80" width="106" height="10" rx="1" fill="rgba(255,255,255,0.20)" stroke="white" stroke-width="1.4"/>
      <rect x="216" y="64" width="20" height="14" rx="1" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1"/>
      <rect x="240" y="66" width="20" height="12" rx="1" fill="rgba(180,140,255,0.30)" stroke="white" stroke-width="1"/>
      <rect x="264" y="64" width="20" height="14" rx="1" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1"/>
      <rect x="288" y="66" width="20" height="12" rx="1" fill="rgba(255,200,80,0.30)" stroke="white" stroke-width="1"/>
    </g>'''


def scene_general_design():
    """装修设计:客厅+尺规+铅笔"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 客厅场景 -->
      <rect x="120" y="140" width="160" height="40" rx="8" fill="rgba(255,255,255,0.14)" stroke="white" stroke-width="2"/>
      <rect x="120" y="128" width="160" height="20" rx="6" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="2"/>
      <rect x="130" y="150" width="44" height="22" rx="5" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="182" y="150" width="44" height="22" rx="5" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="234" y="150" width="40" height="22" rx="5" fill="rgba(255,200,80,0.30)" stroke="white" stroke-width="1.4"/>
      <rect x="172" y="176" width="56" height="6" rx="2" fill="rgba(255,255,255,0.28)" stroke="white" stroke-width="1.2"/>
      <!-- 电视 -->
      <rect x="160" y="74" width="80" height="44" rx="3" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="1.8"/>
      <line x1="180" y1="118" x2="220" y2="118" stroke="white" stroke-width="2"/>
      <!-- 设计工具:三角尺 -->
      <g transform="translate(80,80)" stroke="white" stroke-width="1.8" fill="rgba(255,255,255,0.14)">
        <path d="M 0 0 L 0 40 L 40 40 Z"/>
        <line x1="0" y1="10" x2="10" y2="10" stroke="white" stroke-width="1"/>
        <line x1="0" y1="20" x2="20" y2="20" stroke="white" stroke-width="1"/>
        <line x1="0" y1="30" x2="30" y2="30" stroke="white" stroke-width="1"/>
      </g>
      <!-- 铅笔 -->
      <g transform="translate(300,70) rotate(35)">
        <rect x="0" y="0" width="6" height="50" fill="rgba(255,200,80,0.5)" stroke="white" stroke-width="1.4"/>
        <path d="M 0 0 L 6 0 L 3 -8 Z" fill="rgba(255,220,120,0.7)" stroke="white" stroke-width="1.2"/>
        <rect x="0" y="44" width="6" height="6" fill="rgba(255,120,80,0.6)" stroke="white" stroke-width="1.2"/>
      </g>
      <!-- 灵感灯泡 -->
      <g transform="translate(96,150)">
        <circle r="12" fill="rgba(255,220,120,0.4)" stroke="white" stroke-width="1.8"/>
        <rect x="-5" y="10" width="10" height="6" rx="1" fill="rgba(255,255,255,0.30)" stroke="white" stroke-width="1.4"/>
        <path d="M -4 -4 q 4 6 8 0" fill="none" stroke="white" stroke-width="1.4"/>
      </g>
    </g>'''


def scene_industry():
    """行业资讯:展厅+多个陈列+趋势线"""
    return '''<g class="scene" filter="url(#sc_shadow)">
      <!-- 展厅地面 -->
      <rect x="78" y="168" width="244" height="22" rx="2" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.4"/>
      <line x1="140" y1="168" x2="140" y2="190" stroke="white" stroke-width="1" opacity="0.5"/>
      <line x1="200" y1="168" x2="200" y2="190" stroke="white" stroke-width="1" opacity="0.5"/>
      <line x1="260" y1="168" x2="260" y2="190" stroke="white" stroke-width="1" opacity="0.5"/>
      <!-- 陈列展位1:衣柜 -->
      <rect x="92" y="100" width="50" height="68" rx="2" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="1.8"/>
      <line x1="92" y1="124" x2="142" y2="124" stroke="white" stroke-width="1.2"/>
      <line x1="117" y1="100" x2="117" y2="168" stroke="white" stroke-width="1.2"/>
      <circle cx="110" cy="116" r="2" fill="white" opacity="0.7"/>
      <!-- 陈列展位2:沙发 -->
      <rect x="156" y="130" width="56" height="20" rx="5" fill="rgba(255,255,255,0.16)" stroke="white" stroke-width="1.8"/>
      <rect x="156" y="122" width="56" height="12" rx="4" fill="rgba(255,255,255,0.10)" stroke="white" stroke-width="1.6"/>
      <rect x="162" y="134" width="14" height="12" rx="2" fill="rgba(0,212,255,0.30)" stroke="white" stroke-width="1"/>
      <rect x="180" y="134" width="14" height="12" rx="2" fill="rgba(0,255,128,0.30)" stroke="white" stroke-width="1"/>
      <!-- 陈列展位3:橱柜 -->
      <rect x="226" y="110" width="56" height="58" rx="2" fill="rgba(255,255,255,0.12)" stroke="white" stroke-width="1.8"/>
      <line x1="226" y1="139" x2="282" y2="139" stroke="white" stroke-width="1.2"/>
      <line x1="254" y1="110" x2="254" y2="168" stroke="white" stroke-width="1.2"/>
      <circle cx="240" cy="125" r="2" fill="white" opacity="0.7"/>
      <circle cx="268" cy="125" r="2" fill="white" opacity="0.7"/>
      <!-- 趋势/资讯符号 -->
      <g transform="translate(296,80)">
        <circle r="16" fill="rgba(0,255,128,0.20)" stroke="#00ff80" stroke-width="1.8"/>
        <path d="M -8 4 L -2 -2 L 2 2 L 8 -6" fill="none" stroke="#00ff80" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M 4 -6 L 8 -6 L 8 -2" fill="none" stroke="#00ff80" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <!-- 顶部信息条 -->
      <rect x="92" y="68" width="120" height="20" rx="3" fill="rgba(0,0,0,0.25)" stroke="white" stroke-width="1.4"/>
      <line x1="100" y1="78" x2="160" y2="78" stroke="white" stroke-width="1.4" opacity="0.7"/>
      <line x1="100" y1="84" x2="140" y2="84" stroke="white" stroke-width="1.2" opacity="0.5"/>
      <circle cx="170" cy="78" r="3" fill="rgba(0,255,128,0.6)"/>
    </g>'''


# 关键词 -> 场景(按优先级)
SCENE_RULES = [
    (['儿童房', '儿童'], scene_children_room),
    (['客厅'], scene_living_room),
    (['厨房', '烹饪'], scene_kitchen),
    (['卧室', '衣柜', '梳妆'], scene_bedroom),
    (['书房', '居家办公'], scene_study),
    (['智能家居', '智慧'], scene_smart_home),
    (['小户型', '扩容'], scene_small_apartment),
    (['环保', '材料升级', '绿色', '健康', '材料', '板材'], scene_eco_materials),
    (['预算', '价格'], scene_budget),
    (['交付', '订单'], scene_delivery),
    (['培训', '团队'], scene_training),
    (['趋势', '流行'], scene_trends),
    (['避坑', '注意事项', '新房'], scene_construction),
    (['工艺'], scene_craftsmanship),
    (['风格'], scene_style),
    (['荣获', '认证', '大奖', '优秀'], scene_award),
    (['全屋定制'], scene_general_custom),
    (['装修设计'], scene_general_design),
    (['行业', '资讯', '标准', '市场'], scene_industry),
]


def pick_scene(title, category):
    for keys, fn in SCENE_RULES:
        if any(k in title for k in keys):
            return fn
    if category == '全屋定制':
        return scene_general_custom
    if category == '装修设计':
        return scene_general_design
    return scene_industry


def truncate(title, n=16):
    return title if len(title) <= n else title[:n] + '…'


def generate_svg(news_id, title, category):
    theme = CATEGORY_THEMES.get(category, DEFAULT_THEME)
    g0, g1 = theme['grad']
    subtitle = theme['subtitle']
    scene_fn = pick_scene(title, category)
    scene = scene_fn()
    disp = truncate(title, 16)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
    <defs>
      <linearGradient id="bg_{news_id}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{g0}"/>
        <stop offset="100%" stop-color="{g1}"/>
      </linearGradient>
      <linearGradient id="ov_{news_id}" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="black" stop-opacity="0"/>
        <stop offset="100%" stop-color="black" stop-opacity="0.45"/>
      </linearGradient>
      <filter id="sc_shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="black" flood-opacity="0.25"/>
      </filter>
    </defs>

    <rect width="400" height="300" fill="url(#bg_{news_id})"/>
    <!-- 装饰光斑 -->
    <circle cx="60" cy="50" r="40" fill="white" opacity="0.06"/>
    <circle cx="350" cy="240" r="50" fill="white" opacity="0.05"/>
    <circle cx="340" cy="60" r="22" fill="white" opacity="0.08"/>

    <!-- 场景插画 -->
    {scene}

    <!-- 底部渐变遮罩(增强文字可读性) -->
    <rect y="195" width="400" height="105" fill="url(#ov_{news_id})"/>

    <!-- 分类标签 -->
    <rect x="20" y="20" rx="14" ry="14" width="{len(category) * 15 + 26}" height="28" fill="rgba(0,0,0,0.30)" stroke="white" stroke-width="1" opacity="0.9"/>
    <text x="33" y="40" font-size="13" font-weight="600" fill="white" font-family="'Noto Sans SC', sans-serif">{category}</text>

    <!-- 主标题 -->
    <text x="200" y="226" text-anchor="middle" font-size="20" font-weight="700" fill="white" font-family="'Noto Sans SC', sans-serif" letter-spacing="0.5">{disp}</text>

    <!-- 副标题 -->
    <text x="200" y="250" text-anchor="middle" font-size="12" fill="rgba(255,255,255,0.78)" font-family="'Noto Sans SC', sans-serif" letter-spacing="2">{subtitle}</text>

    <!-- 底部品牌信息 -->
    <line x1="150" y1="268" x2="250" y2="268" stroke="white" stroke-width="1" opacity="0.35"/>
    <text x="200" y="286" text-anchor="middle" font-size="11" fill="rgba(255,255,255,0.55)" font-family="'Noto Sans SC', sans-serif">浦北装修设计 · 专业品质 · 匠心铸就</text>
  </svg>'''


def main():
    os.makedirs(IMG_DIR, exist_ok=True)

    with open(NEWS_DATA, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    print(f'📋 共 {len(news_data)} 条新闻\n')

    for item in news_data:
        nid = item['id']
        title = item['title']
        category = item.get('category', '')
        svg = generate_svg(nid, title, category)
        path = os.path.join(IMG_DIR, f'news_{nid}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        item['image'] = f'assets/images/news/news_{nid}.svg'
        print(f'✓ [{nid}] {category:5s} | {title[:30]}')

    # 1. 更新 news-data.json(.jpg 引用修复为 .svg)
    with open(NEWS_DATA, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f'\n✓ news-data.json 已更新(全部指向 .svg)')

    # 2. 更新 news.html(.jpg -> .svg)
    with open(NEWS_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    # 逐条把 news_ID.jpg 替换为 news_ID.svg
    for item in news_data:
        nid = item['id']
        html = html.replace(f'assets/images/news/news_{nid}.jpg',
                            f'assets/images/news/news_{nid}.svg')
    with open(NEWS_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    jpg_left = len(re.findall(r'news_[^"\']+\.jpg', html))
    svg_cnt = len(re.findall(r'news_[^"\']+\.svg', html))
    print(f'✓ news.html 已更新(svg 引用 {svg_cnt} 处, 剩余 jpg {jpg_left} 处)')

    # 3. 清理可能残留的 .jpg 文件
    removed = 0
    for fn in os.listdir(IMG_DIR):
        if fn.endswith('.jpg'):
            try:
                os.remove(os.path.join(IMG_DIR, fn))
                removed += 1
            except Exception:
                pass
    if removed:
        print(f'✓ 清理残留 .jpg 文件 {removed} 个')

    svg_total = sum(1 for f in os.listdir(IMG_DIR) if f.endswith('.svg'))
    print(f'\n{"=" * 60}')
    print(f'✅ 完成:共生成 {svg_total} 张内容相关 SVG 场景插画')


if __name__ == '__main__':
    main()
