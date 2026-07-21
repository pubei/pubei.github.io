#!/usr/bin/env python3
import os

gallery_css = '''\n\n.project-gallery{padding:40px 0;}.gallery-wrapper{display:flex;gap:20px;align-items:flex-start;}.gallery-main{flex:1;position:relative;border-radius:12px;overflow:hidden;background:rgba(255,255,255,0.04);min-height:400px;}.gallery-main-image{width:100%;height:450px;object-fit:cover;transition:opacity 0.3s ease;}.gallery-overlay{position:absolute;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity 0.3s ease;cursor:zoom-in;}.gallery-main:hover .gallery-overlay{opacity:1;}.gallery-zoom{font-size:48px;color:white;font-weight:300;}.gallery-thumbs{display:flex;flex-direction:column;gap:12px;width:120px;flex-shrink:0;}.thumb-item{width:120px;height:80px;border-radius:8px;overflow:hidden;cursor:pointer;border:2px solid transparent;transition:all 0.3s ease;position:relative;}.thumb-item:hover{border-color:rgba(0,212,255,0.5);transform:translateX(-4px);}.thumb-item.active{border-color:#00d4ff !important;box-shadow:0 0 15px rgba(0,212,255,0.5) !important;transform:translateX(-4px);}.thumb-item img{width:100%;height:100%;object-fit:cover;}.thumb-label{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,0.9),transparent);color:white;font-size:0.75rem;padding:8px 6px;text-align:center;}@media (max-width:768px){.gallery-wrapper{flex-direction:column;}.gallery-thumbs{flex-direction:row;width:100%;overflow-x:auto;padding-bottom:10px;}.thumb-item{flex-shrink:0;}.gallery-main-image{height:300px;}}'''

gallery_js = '''\n\n<script>\ndocument.addEventListener('DOMContentLoaded', function() {\n  var thumbItems = document.querySelectorAll('.thumb-item');\n  var mainImg = document.getElementById('gallery-main-img');\n  \n  thumbItems.forEach(function(item) {\n    item.addEventListener('click', function() {\n      thumbItems.forEach(function(i) { i.classList.remove('active'); });\n      this.classList.add('active');\n      \n      var newSrc = this.dataset.src;\n      mainImg.style.opacity = '0.5';\n      \n      var tempImg = new Image();\n      tempImg.onload = function() {\n        mainImg.src = newSrc;\n        mainImg.style.opacity = '1';\n      };\n      tempImg.onerror = function() {\n        mainImg.style.opacity = '1';\n      };\n      tempImg.src = newSrc;\n    });\n  });\n});\n</script>'''

files = ['project-detail-1.html', 'project-detail-2.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'gallery-main' in content:
            if '.project-gallery' not in content:
                content = content.replace('</style>', gallery_css + '\n</style>')
            
            if 'gallery-main-img' in content and 'thumb-item.addEventListener' not in content:
                content = content.replace('</footer>', '</footer>' + gallery_js)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'Updated: {file}')
        else:
            print(f'Skip (no gallery): {file}')

print('Done!')
