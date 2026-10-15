import os

old_link = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
new_link = '<link rel="icon" href="/assets/images/logo.svg" type="image/svg+xml">'

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
updated = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_link in content:
        content = content.replace(old_link, new_link)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'Updated: {html_file}')

print(f'\nTotal updated: {updated}/{len(html_files)}')