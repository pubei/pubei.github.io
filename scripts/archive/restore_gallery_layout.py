#!/usr/bin/env python3
import os

old_style = '''<section class="project-gallery">
      <style>
        .project-gallery .gallery-wrapper { display: flex; flex-direction: column; gap: 20px; align-items: center !important; }
        .project-gallery .gallery-main { width: 100% !important; max-width: 100% !important; }
        .project-gallery .gallery-thumbs { display: flex; flex-direction: row !important; gap: 12px; width: 100% !important; justify-content: center !important; flex-wrap: wrap; }
        .project-gallery .thumb-item { width: 150px !important; height: 100px !important; }
        .project-gallery .thumb-item:hover, .project-gallery .thumb-item.active { transform: scale(1.05) !important; }
      </style>'''

new_style = '''<section class="project-gallery">
      <style>
        .project-gallery .gallery-wrapper { display: flex !important; flex-direction: row !important; gap: 20px !important; align-items: flex-start !important; }
        .project-gallery .gallery-main { flex: 1 !important; position: relative; border-radius: 12px; overflow: hidden; background: rgba(255,255,255,0.04); min-height: 400px; }
        .project-gallery .gallery-thumbs { display: flex !important; flex-direction: column !important; gap: 12px !important; width: 120px !important; flex-shrink: 0 !important; }
        .project-gallery .thumb-item { width: 120px !important; height: 80px !important; border-radius: 8px; overflow: hidden; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease; position: relative; }
        .project-gallery .thumb-item:hover { border-color: rgba(0,212,255,0.5); transform: translateX(-4px); }
        .project-gallery .thumb-item.active { border-color: #00d4ff !important; box-shadow: 0 0 15px rgba(0,212,255,0.5) !important; transform: translateX(-4px); }
        .project-gallery .thumb-item img { width: 100%; height: 100%; object-fit: cover; }
        .project-gallery .thumb-label { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); color: white; font-size: 0.75rem; padding: 8px 6px; text-align: center; }
        .project-gallery .gallery-main-image { width: 100%; height: 450px; object-fit: cover; transition: opacity 0.3s ease; }
        .project-gallery .gallery-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease; cursor: zoom-in; }
        .project-gallery .gallery-main:hover .gallery-overlay { opacity: 1; }
        .project-gallery .gallery-zoom { font-size: 48px; color: white; font-weight: 300; }
        @media (max-width: 768px) { .project-gallery .gallery-wrapper { flex-direction: column !important; } .project-gallery .gallery-thumbs { flex-direction: row !important; width: 100% !important; overflow-x: auto; padding-bottom: 10px; } .project-gallery .thumb-item { flex-shrink: 0; } .project-gallery .gallery-main-image { height: 300px; } }
      </style>'''

files = ['project-detail-1.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_style in content:
            content = content.replace(old_style, new_style)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'Restored layout: {file}')

print('Done!')
