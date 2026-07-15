import os
import re

nav_items = {
    '首页': {
        'href': 'index.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg></span>'
    },
    '服务项目': {
        'href': 'services.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75zM3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/></svg></span>'
    },
    '装修案例': {
        'href': 'projects.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></span>'
    },
    '公司新闻': {
        'href': 'news.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg></span>'
    },
    '关于我们': {
        'href': 'about.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg></span>'
    },
    '在线预约': {
        'href': 'contact.html',
        'icon': '<span class="nav-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm-2 14l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg></span>'
    }
}

nav_order = ['首页', '服务项目', '装修案例', '公司新闻', '关于我们', '在线预约']

def get_active_item(filename):
    if filename == 'index.html':
        return '首页'
    elif filename == 'services.html' or filename.startswith('service-detail-'):
        return '服务项目'
    elif filename == 'projects.html' or filename.startswith('project-detail-'):
        return '装修案例'
    elif filename == 'news.html' or filename.startswith('news-detail'):
        return '公司新闻'
    elif filename == 'about.html':
        return '关于我们'
    elif filename == 'contact.html':
        return '在线预约'
    return '首页'

def update_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    nav_start = content.find('<nav class="nav">')
    nav_end = content.find('</nav>', nav_start)
    
    if nav_start == -1 or nav_end == -1:
        return False
    
    filename = os.path.basename(filepath)
    active_item = get_active_item(filename)
    
    new_nav_items = []
    for item_name in nav_order:
        item_info = nav_items[item_name]
        is_active = active_item == item_name
        active_class = ' class="active"' if is_active else ''
        new_nav_items.append(f'<li class="nav-item"><a href="{item_info["href"]}"{active_class}>{item_info["icon"]}{item_name}</a></li>')
    
    new_nav_items_str = '\n            '.join(new_nav_items)
    
    new_nav = f'<nav class="nav">\n          <ul class="nav-list">\n            {new_nav_items_str}\n          </ul>\n        </nav>'
    
    new_content = content[:nav_start] + new_nav + content[nav_end+6:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
updated = 0

for html_file in html_files:
    if update_nav(html_file):
        updated += 1
        print(f'Updated: {html_file}')

print(f'\nTotal updated: {updated}/{len(html_files)}')
