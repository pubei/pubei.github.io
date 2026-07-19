#!/usr/bin/env python3
import os
import re

files = [
    'index.html', 'project-detail-1.html', 'privacy.html', 'faq.html',
    'service-detail-renovation.html', 'services.html', 'service-detail-custom.html',
    'project-detail-6.html', 'service-detail-smart.html', 'news-detail.html',
    'service-detail-partial.html', 'projects.html', 'project-detail-5.html',
    'project-detail-4.html', 'terms.html', 'sitemap.html', 'contact.html',
    'about.html', 'project-detail-3.html', 'service-detail-soft.html',
    'service-detail-new.html', 'project-detail-2.html'
]

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace('style.css?v=20', 'style.css?v=21')
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file}")

print("Done")
