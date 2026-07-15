import os

new_version = '20'

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
updated = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('.css?v=9', f'.css?v={new_version}')
    content = content.replace('.css?v=14', f'.css?v={new_version}')
    content = content.replace('.css?v=15', f'.css?v={new_version}')
    content = content.replace('.css?v=16', f'.css?v={new_version}')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    updated += 1
    print(f'Updated: {html_file}')

print(f'\nTotal updated: {updated}/{len(html_files)}')
