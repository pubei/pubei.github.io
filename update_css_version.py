import os
import re

for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, 'r') as f:
            content = f.read()
        
        content = re.sub(r'<link rel="stylesheet" href="assets/css/style.css[^"]*">', '<link rel="stylesheet" href="assets/css/style.css?v=6">', content)
        
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        
        with open(file, 'w') as f:
            f.write(content)
        
        print(f'Updated: {file}')
