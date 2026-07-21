#!/usr/bin/env python3
import os

inline_style = '''<section class="project-gallery">
      <style>
        .project-gallery .gallery-wrapper { display: flex; flex-direction: column; gap: 20px; align-items: center !important; }
        .project-gallery .gallery-main { width: 100% !important; max-width: 100% !important; }
        .project-gallery .gallery-thumbs { display: flex; flex-direction: row !important; gap: 12px; width: 100% !important; justify-content: center !important; flex-wrap: wrap; }
        .project-gallery .thumb-item { width: 150px !important; height: 100px !important; }
        .project-gallery .thumb-item:hover, .project-gallery .thumb-item.active { transform: scale(1.05) !important; }
      </style>
      <div class="container">
        <div class="gallery-wrapper">'''

files = ['project-detail-1.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '<section class="project-gallery">' in content and 'project-gallery .gallery-wrapper' not in content:
            content = content.replace('<section class="project-gallery">\n      <div class="container">\n        <div class="gallery-wrapper">', inline_style)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'Added inline styles: {file}')

print('Done!')
