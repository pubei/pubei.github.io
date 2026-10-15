import os

old_font_links = [
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">'
]

new_font_links = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
updated = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old_link in old_font_links:
        if old_link in content:
            content = content.replace(old_link, new_font_links)
            modified = True
    
    if modified:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'Updated: {html_file}')

print(f'\nTotal updated: {updated}/{len(html_files)}')
