#!/usr/bin/env python3
import os

zoom_script = '''\n  mainImg.addEventListener('click', function() {\n    var lightbox = document.createElement('div');\n    lightbox.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:zoom-out;animation:fadeIn 0.3s ease;';\n    lightbox.innerHTML = '<img src=\"' + this.src + '\" style=\"max-width:90%;max-height:90%;object-fit:contain;border-radius:8px;animation:scaleIn 0.3s ease;\" alt=\"放大查看\">';\n    \n    var closeBtn = document.createElement('button');\n    closeBtn.innerHTML = '&times;';\n    closeBtn.style.cssText = 'position:absolute;top:20px;right:20px;width:48px;height:48px;background:rgba(255,255,255,0.1);border:none;border-radius:50%;color:white;font-size:28px;cursor:pointer;transition:all 0.3s ease;';\n    closeBtn.onmouseover = function() { this.style.background = 'rgba(255,255,255,0.2)'; };\n    closeBtn.onmouseout = function() { this.style.background = 'rgba(255,255,255,0.1)'; };\n    lightbox.appendChild(closeBtn);\n    \n    var style = document.createElement('style');\n    style.innerHTML = '@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}@keyframes scaleIn{from{transform:scale(0.9);opacity:0;}to{transform:scale(1);opacity:1;}}';\n    document.head.appendChild(style);\n    \n    lightbox.onclick = function(e) {\n      if (e.target === lightbox || e.target === closeBtn) {\n        lightbox.style.opacity = '0';\n        setTimeout(function() {\n          document.body.removeChild(lightbox);\n          document.head.removeChild(style);\n        }, 300);\n      }\n    };\n    \n    document.body.appendChild(lightbox);\n  });\n});\n</script>'''

files = ['project-detail-1.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'gallery-main-img' in content and 'mainImg.addEventListener' not in content:
            content = content.replace('});\n</script>', zoom_script)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'Added zoom: {file}')

print('Done!')
