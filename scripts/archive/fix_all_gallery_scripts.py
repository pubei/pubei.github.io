#!/usr/bin/env python3
import os

new_script = '''<script>
document.addEventListener('DOMContentLoaded', function() {
  var thumbItems = document.querySelectorAll('.thumb-item');
  var mainImg = document.getElementById('gallery-main-img');
  var galleryMain = document.querySelector('.gallery-main');
  
  mainImg.style.transition = 'opacity 0.3s ease';
  
  thumbItems.forEach(function(item) {
    item.addEventListener('click', function(e) {
      e.stopPropagation();
      thumbItems.forEach(function(i) { i.classList.remove('active'); });
      this.classList.add('active');
      
      var newSrc = this.dataset.src;
      mainImg.style.opacity = '0.5';
      
      var tempImg = new Image();
      tempImg.onload = function() {
        mainImg.src = newSrc;
        mainImg.style.opacity = '1';
      };
      tempImg.onerror = function() {
        mainImg.style.opacity = '1';
      };
      tempImg.src = newSrc;
    });
  });
  
  galleryMain.addEventListener('click', function() {
    var lightbox = document.createElement('div');
    lightbox.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:zoom-out;animation:fadeIn 0.3s ease;';
    lightbox.innerHTML = '<img src=\"' + mainImg.src + '\" style=\"max-width:90%;max-height:90%;object-fit:contain;border-radius:8px;animation:scaleIn 0.3s ease;\" alt=\"放大查看\">';
    
    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = 'position:absolute;top:20px;right:20px;width:48px;height:48px;background:rgba(255,255,255,0.1);border:none;border-radius:50%;color:white;font-size:28px;cursor:pointer;transition:all 0.3s ease;';
    closeBtn.onmouseover = function() { this.style.background = 'rgba(255,255,255,0.2)'; };
    closeBtn.onmouseout = function() { this.style.background = 'rgba(255,255,255,0.1)'; };
    lightbox.appendChild(closeBtn);
    
    var style = document.createElement('style');
    style.innerHTML = '@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}@keyframes scaleIn{from{transform:scale(0.9);opacity:0;}to{transform:scale(1);opacity:1;}}';
    document.head.appendChild(style);
    
    lightbox.onclick = function(e) {
      if (e.target === lightbox || e.target === closeBtn) {
        lightbox.style.opacity = '0';
        setTimeout(function() {
          document.body.removeChild(lightbox);
          document.head.removeChild(style);
        }, 300);
      }
    };
    
    document.body.appendChild(lightbox);
  });
});
</script>'''

files = ['project-detail-1.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'gallery-main-img' in content:
            old_script_start = content.find('<script>\ndocument.addEventListener')
            old_script_end = content.find('</script>\n  <script src="assets/js/main.js">')
            
            if old_script_start != -1 and old_script_end != -1:
                new_content = content[:old_script_start] + new_script + content[old_script_end:]
                
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f'Fixed: {file}')

print('Done!')
