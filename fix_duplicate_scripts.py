#!/usr/bin/env python3
import os

files = ['project-detail-1.html', 'project-detail-3.html', 
         'project-detail-4.html', 'project-detail-6.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'thumb-item.addEventListener' in content and 'thumbItems.forEach(item =>' in content:
            pattern = r'\n\n  <script>\n    document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\n      const thumbItems = document\.querySelectorAll\(\'.thumb-item\'\);\n      const mainImg = document\.getElementById\(\'gallery-main-img\'\);\n      \n      thumbItems\.forEach\(item => \{\n        item\.addEventListener\(\'click\', function\(\) \{\n          thumbItems\.forEach\(i => i\.classList\.remove\(\'active\'\)\);\n          this\.classList\.add\(\'active\'\);\n          mainImg\.src = this\.dataset\.src;\n        \}\);\n      \}\);\n    \}\);\n  </script>'
            
            new_content = content.replace(pattern, '')
            
            if new_content != content:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed duplicate script: {file}')

print('Done!')
