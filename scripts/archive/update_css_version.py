#!/usr/bin/env python3
import os

files = [
    'index.html', 'project-detail-1.html', 'project-detail-2.html',
    'project-detail-3.html', 'project-detail-4.html', 'project-detail-5.html',
    'project-detail-6.html', 'privacy.html', 'faq.html',
    'service-detail-renovation.html', 'services.html', 'service-detail-custom.html',
    'service-detail-new.html', 'service-detail-partial.html', 'service-detail-soft.html',
    'service-detail-smart.html', 'service-detail-electrical.html', 'service-detail-supervision.html',
    'about.html', 'contact.html', 'news.html', 'news-detail.html',
    'projects.html', 'sitemap.html', 'terms.html'
]

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace('style.css?v=25', 'style.css?v=26')
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated: {file}')

print('Done!')
