#!/usr/bin/env python3
"""
网站搜索引擎提交脚本 - 将网站推送给各大搜索引擎，加快收录速度

支持的搜索引擎：
- Google Search Console
- Bing Webmaster Tools
- Baidu 百度搜索资源平台
- Yandex Webmaster
- 360 搜索
- Sogou 搜狗搜索
"""

import requests
import json
import time
from datetime import datetime

# 网站配置
SITE_URL = "https://pboo.top"
SITEMAP_URL = "https://pboo.top/sitemap.xml"

# 搜索引擎提交URL
SEARCH_ENGINES = {
    "google": {
        "name": "Google",
        "submit_url": "https://www.google.com/ping?sitemap={sitemap_url}",
        "description": "Google搜索索引提交"
    },
    "bing": {
        "name": "Bing",
        "submit_url": "https://www.bing.com/webmaster/ping.aspx?siteMap={sitemap_url}",
        "description": "Bing搜索索引提交"
    },
    "baidu": {
        "name": "百度",
        "submit_url": "http://ping.baidu.com/ping/RPC2",
        "method": "POST",
        "content_type": "application/json",
        "payload": {
            "method": "ping",
            "params": [
                SITE_URL,
                SITEMAP_URL
            ],
            "id": 1
        },
        "description": "百度搜索索引提交"
    },
    "yandex": {
        "name": "Yandex",
        "submit_url": "https://webmaster.yandex.ru/site/map.xml?url={sitemap_url}",
        "description": "Yandex搜索索引提交"
    },
    "so": {
        "name": "360搜索",
        "submit_url": "http://www.so.com/linksubmit?url={site_url}",
        "description": "360搜索链接提交"
    },
    "sogou": {
        "name": "搜狗搜索",
        "submit_url": "http://www.sogou.com/feedback/urlfeedback.php",
        "method": "POST",
        "content_type": "application/x-www-form-urlencoded",
        "payload": {
            "url": SITE_URL,
            "type": "url",
            "desc": "浦北装修设计公司 - 专业全屋定制与装修设计服务"
        },
        "description": "搜狗搜索链接提交"
    },
    "google_index": {
        "name": "Google Index",
        "submit_url": "https://indexing.googleapis.com/v3/urlNotifications:publish?key=AIzaSyCq6k6C2jVnqQ1Yx4a4Z8k8Z8k8Z8k8Z8k",
        "method": "POST",
        "content_type": "application/json",
        "payload": {
            "url": SITE_URL,
            "type": "URL_UPDATED"
        },
        "description": "Google Indexing API (需要API密钥)",
        "requires_key": True
    }
}


def submit_to_search_engine(name, config):
    """提交网站到搜索引擎"""
    try:
        url = config["submit_url"]
        method = config.get("method", "GET")
        
        # 替换URL中的占位符
        url = url.replace("{sitemap_url}", SITEMAP_URL)
        url = url.replace("{site_url}", SITE_URL)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            content_type = config.get("content_type", "application/json")
            headers["Content-Type"] = content_type
            payload = config.get("payload", {})
            if content_type == "application/json":
                response = requests.post(url, json=payload, headers=headers, timeout=10)
            else:
                response = requests.post(url, data=payload, headers=headers, timeout=10)
        else:
            return {"name": config["name"], "success": False, "error": "不支持的HTTP方法"}
        
        # 判断是否成功
        success = response.status_code in [200, 201, 202, 204]
        
        if success:
            # 检查百度的特殊响应
            if name == "baidu":
                try:
                    result = response.json()
                    success = result.get("result", {}).get("status", 0) == 0
                except:
                    pass
            
            # 检查搜狗的特殊响应
            if name == "sogou":
                success = "成功" in response.text or response.status_code == 200
        
        return {
            "name": config["name"],
            "success": success,
            "status_code": response.status_code,
            "response": response.text[:200] if response.text else "",
            "description": config["description"]
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "name": config["name"],
            "success": False,
            "error": str(e),
            "description": config["description"]
        }


def submit_all():
    """提交到所有搜索引擎"""
    print("=" * 60)
    print(f"网站搜索引擎提交工具")
    print(f"网站地址: {SITE_URL}")
    print(f"站点地图: {SITEMAP_URL}")
    print(f"提交时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    results = []
    total_success = 0
    total_failed = 0
    
    for engine_name, config in SEARCH_ENGINES.items():
        # 跳过需要API密钥的服务（需要用户配置）
        if config.get("requires_key", False):
            print(f"⏭️  {config['name']}: 需要API密钥，请手动配置")
            continue
        
        print(f"🔄 正在提交到 {config['name']}...")
        result = submit_to_search_engine(engine_name, config)
        results.append(result)
        
        if result["success"]:
            print(f"✅ {result['name']}: 提交成功")
            total_success += 1
        else:
            print(f"❌ {result['name']}: 提交失败 - {result.get('error', '')}")
            total_failed += 1
        
        # 避免请求过于频繁
        time.sleep(2)
        print()
    
    # 输出总结
    print("=" * 60)
    print("提交结果汇总:")
    print("=" * 60)
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {result['name']}: {result['description']}")
    
    print()
    print(f"成功: {total_success} | 失败: {total_failed}")
    print()
    
    # 输出手动提交指南
    print("=" * 60)
    print("手动提交指南（推荐）:")
    print("=" * 60)
    print("""
1. Google Search Console:
   访问: https://search.google.com/search-console/
   添加站点: https://pboo.top
   提交sitemap: https://pboo.top/sitemap.xml

2. Bing Webmaster Tools:
   访问: https://www.bing.com/webmasters/
   添加站点: https://pboo.top
   提交sitemap: https://pboo.top/sitemap.xml

3. 百度搜索资源平台:
   访问: https://ziyuan.baidu.com/
   添加站点: https://pboo.top
   提交sitemap: https://pboo.top/sitemap.xml

4. 360搜索站长平台:
   访问: http://zhanzhang.so.com/
   添加站点: https://pboo.top

5. 搜狗搜索站长平台:
   访问: http://zhanzhang.sogou.com/
   添加站点: https://pboo.top

6. Yandex Webmaster:
   访问: https://webmaster.yandex.ru/
   添加站点: https://pboo.top
""")
    
    # 保存提交日志
    log_file = f"search_engine_submit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_data = {
        "site_url": SITE_URL,
        "sitemap_url": SITEMAP_URL,
        "submit_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "results": results
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 提交日志已保存到: {log_file}")


def generate_robots():
    """生成优化的robots.txt"""
    robots_content = f"""User-agent: *
Allow: /
Disallow: /assets/js/
Disallow: /assets/css/
Disallow: /assets/images/news-bg-*.svg

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


if __name__ == '__main__':
    print("=== 开始网站搜索引擎提交 ===")
    print()
    
    # 生成优化的robots.txt
    generate_robots()
    print()
    
    # 提交到所有搜索引擎
    submit_all()
    
    print("\n=== 提交完成 ===")
