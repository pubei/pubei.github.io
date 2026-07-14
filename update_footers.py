import os

def get_footer_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find('<footer')
    end = content.find('</footer>') + len('</footer>')
    return content[start:end], start, end

home_footer, _, _ = get_footer_content('index.html')

updated_count = 0
for filename in os.listdir('.'):
    if filename.endswith('.html') and filename != 'index.html':
        footer, start, end = get_footer_content(filename)
        if footer:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content[:start] + home_footer + content[end:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            print(f"✅ {filename}: 页脚已更新")

print(f"\n共更新 {updated_count} 个页面")