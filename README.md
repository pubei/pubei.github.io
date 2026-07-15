# 浦北装修设计官网

> 专业品质装修服务 - 一站式装修解决方案

![Website Preview](assets/images/logo.svg)

## 项目简介

浦北装修设计官网是一个基于纯静态HTML/CSS/JavaScript构建的企业展示网站，提供装修服务展示、案例展示、新闻资讯等功能。

## 功能特性

- **响应式设计**: 支持桌面端和移动端访问
- **导航优化**: 玻璃态动感透明图标，现代化呼吸灯效果
- **服务展示**: 全屋定制、新房装修、智能家居、软装设计、旧房翻新、局部改造、水电工程、装修监理
- **案例展示**: 多种装修风格案例展示（现代简约、轻奢、北欧等）
- **新闻资讯**: 公司动态和行业资讯
- **在线预约**: 免费咨询和报价获取
- **社交媒体**: 微信、QQ、抖音、小红书、GitHub、Bilibili等社交链接

## 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **样式**: 原生CSS3（含动画、渐变、玻璃态效果）
- **图标**: SVG矢量图标
- **部署**: GitHub Pages
- **CI/CD**: GitHub Actions（每日新闻更新）

## 项目结构

```
├── .github/workflows/    # GitHub Actions 工作流
├── assets/
│   ├── css/              # 样式文件
│   ├── data/             # 数据文件（新闻数据）
│   ├── images/           # 图片资源
│   └── js/               # JavaScript 文件
├── index.html            # 首页
├── services.html         # 服务项目
├── projects.html         # 装修案例
├── news.html             # 公司新闻
├── about.html            # 关于我们
├── contact.html          # 在线预约
├── CNAME                 # 自定义域名配置
├── sitemap.xml           # 网站地图
├── robots.txt            # 搜索引擎配置
└── *.py                  # 自动化脚本（批量更新、优化等）
```

## 快速开始

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/pubei/pubei.github.io.git

# 进入项目目录
cd pubei.github.io

# 启动本地服务器（Python 3）
python3 -m http.server 8080

# 访问网站
# http://localhost:8080
```

### 部署

项目使用 GitHub Pages 自动部署：

1. 提交代码到 `main` 分支
2. GitHub Pages 自动构建并部署
3. 访问：https://pboo.top

## 自动化脚本

项目包含多个 Python 脚本用于批量操作：

| 脚本 | 功能 |
|------|------|
| `update_nav_icons.py` | 批量更新导航图标 |
| `update_footer.py` | 批量更新页脚 |
| `add_social_links.py` | 添加社交媒体链接 |
| `update_favicon.py` | 更新网站图标 |
| `generate_news.py` | 生成新闻页面 |
| `optimize_fonts.py` | 优化字体加载 |

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 电话：134-1227-7880
- 邮箱：contact@pboo.top
- 地址：浦北县小江街道

---

# Pubei Decoration Design Website

> Professional Quality Decoration Services - One-stop Decoration Solutions

## Project Introduction

This is a static HTML/CSS/JavaScript website for Pubei Decoration Design, a professional home decoration company. It provides service showcases, case studies, news updates, and more.

## Features

- **Responsive Design**: Supports desktop and mobile devices
- **Navigation Optimization**: Glassmorphism style icons with breathing animation
- **Service Showcase**: Custom home, new home decoration, smart home, soft decoration, old home renovation, partial renovation, water/electric works, decoration supervision
- **Case Studies**: Various decoration styles (modern, luxury, Nordic, etc.)
- **News Updates**: Company news and industry information
- **Online Booking**: Free consultation and quotation
- **Social Media**: WeChat, QQ, Douyin, Xiaohongshu, GitHub, Bilibili

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Native CSS3 (animations, gradients, glassmorphism)
- **Icons**: SVG Vector Icons
- **Deployment**: GitHub Pages
- **CI/CD**: GitHub Actions (daily news updates)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/pubei/pubei.github.io.git

# Navigate to the project directory
cd pubei.github.io

# Start local server (Python 3)
python3 -m http.server 8080

# Visit the website
# http://localhost:8080
```

## License

MIT License