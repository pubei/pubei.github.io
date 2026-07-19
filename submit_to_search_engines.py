#!/usr/bin/env python3
"""
网站搜索引擎提交脚本 - 将网站推送给各大搜索引擎，加快收录速度

支持的搜索引擎：
- Google Search Console (需要手动验证)
- Bing Webmaster Tools (需要手动验证)
- Baidu 百度搜索资源平台 (需要手动验证)
- Yandex Webmaster (需要手动验证)
- 360 搜索 (需要手动验证)
- Sogou 搜狗搜索 (需要手动验证)

注意：现代搜索引擎要求通过站长平台进行身份验证后才能提交站点地图
本脚本主要用于生成SEO优化配置和提供手动提交指南
"""

import requests
import json
import time
from datetime import datetime

# 网站配置
SITE_URL = "https://pboo.top"
SITEMAP_URL = "https://pboo.top/sitemap.xml"


def generate_robots():
    """生成优化的robots.txt"""
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {SITEMAP_URL}

# Googlebot优化
User-agent: Googlebot
Allow: /
Crawl-delay: 1

# Bingbot优化
User-agent: Bingbot
Allow: /
Crawl-delay: 2

# Baiduspider优化
User-agent: Baiduspider
Allow: /
Crawl-delay: 2

# Yandex优化
User-agent: Yandex
Allow: /
Crawl-delay: 2
"""
    with open("robots.txt", 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print(f"✅ robots.txt 已优化")


def ping_search_engines():
    """尝试ping搜索引擎（部分可能需要验证）"""
    search_engines = [
        {
            "name": "Google",
            "url": f"https://www.google.com/ping?sitemap={SITEMAP_URL}",
            "description": "Google站点地图ping服务"
        },
        {
            "name": "Bing",
            "url": f"https://www.bing.com/webmaster/ping.aspx?siteMap={SITEMAP_URL}",
            "description": "Bing站点地图ping服务"
        },
        {
            "name": "Yandex",
            "url": f"https://webmaster.yandex.ru/site/map.xml?url={SITEMAP_URL}",
            "description": "Yandex站点地图提交"
        }
    ]
    
    results = []
    total_success = 0
    
    print("🔄 正在尝试ping搜索引擎...")
    print()
    
    for engine in search_engines:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(engine["url"], headers=headers, timeout=15)
            
            success = response.status_code in [200, 201, 202, 204]
            results.append({
                "name": engine["name"],
                "success": success,
                "status_code": response.status_code,
                "description": engine["description"]
            })
            
            if success:
                print(f"✅ {engine['name']}: ping成功")
                total_success += 1
            else:
                print(f"⚠️  {engine['name']}: 返回状态码 {response.status_code} (可能需要手动验证)")
                
        except Exception as e:
            print(f"❌ {engine['name']}: ping失败 - {str(e)}")
            results.append({
                "name": engine["name"],
                "success": False,
                "error": str(e),
                "description": engine["description"]
            })
        
        time.sleep(2)
    
    return results


def print_submission_guide():
    """打印手动提交指南"""
    print("\n" + "=" * 60)
    print("🎯 搜索引擎手动提交指南（推荐）")
    print("=" * 60)
    print("""

1. 📌 Google Search Console (最推荐)
   访问: https://search.google.com/search-console/
   添加站点: https://pboo.top
   验证方式: HTML文件验证或DNS验证
   提交sitemap: https://pboo.top/sitemap.xml

2. 📌 Bing Webmaster Tools
   访问: https://www.bing.com/webmasters/
   添加站点: https://pboo.top
   验证方式: HTML文件验证或DNS验证
   提交sitemap: https://pboo.top/sitemap.xml

3. 📌 百度搜索资源平台 (国内用户必做)
   访问: https://ziyuan.baidu.com/
   添加站点: https://pboo.top
   验证方式: HTML文件验证或DNS验证
   提交sitemap: https://pboo.top/sitemap.xml
   提交链接: 使用"链接提交"工具批量提交页面

4. 📌 360搜索站长平台
   访问: http://zhanzhang.so.com/
   添加站点: https://pboo.top
   验证方式: HTML文件验证

5. 📌 搜狗搜索站长平台
   访问: http://zhanzhang.sogou.com/
   添加站点: https://pboo.top
   验证方式: HTML文件验证

6. 📌 Yandex Webmaster (俄语地区)
   访问: https://webmaster.yandex.ru/
   添加站点: https://pboo.top
   验证方式: HTML文件验证

""")
    
    print("=" * 60)
    print("📋 SEO优化检查清单")
    print("=" * 60)
    print("""
✅ robots.txt - 已配置，允许所有爬虫访问
✅ sitemap.xml - 已配置，包含所有页面链接
✅ JSON-LD结构化数据 - 已添加LocalBusiness类型
✅ Canonical标签 - 已添加到首页
✅ OG标签 - 已添加社交分享优化
✅ 网站验证meta标签占位符 - 已添加到首页

待完成：
🔲 在Google Search Console验证站点
🔲 在百度搜索资源平台验证站点
🔲 在Bing Webmaster Tools验证站点
🔲 添加Google Analytics追踪代码
🔲 添加百度统计代码
""")


def main():
    print("=" * 60)
    print(f"网站搜索引擎提交工具")
    print(f"网站地址: {SITE_URL}")
    print(f"站点地图: {SITEMAP_URL}")
    print(f"提交时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 生成优化的robots.txt
    generate_robots()
    print()
    
    # 尝试ping搜索引擎
    ping_search_engines()
    
    # 打印提交指南
    print_submission_guide()
    
    # 保存提交日志
    log_file = f"search_engine_submit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_data = {
        "site_url": SITE_URL,
        "sitemap_url": SITEMAP_URL,
        "submit_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "guide_generated",
        "notes": "现代搜索引擎需要通过站长平台手动验证站点"
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 提交日志已保存到: {log_file}")
    print("\n=== 完成 ===")


if __name__ == '__main__':
    main()
