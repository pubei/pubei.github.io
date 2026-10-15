import os

def get_footer_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find('<footer')
    end = content.find('</footer>') + len('</footer>')
    return content[start:end] if start != -1 and end != -1 else None

home_footer = get_footer_content('index.html')
if not home_footer:
    print("首页未找到页脚")
    exit()

home_footer_clean = home_footer.strip()

mismatched = []
for filename in os.listdir('.'):
    if filename.endswith('.html') and filename != 'index.html':
        footer = get_footer_content(filename)
        if footer:
            footer_clean = footer.strip()
            if footer_clean != home_footer_clean:
                mismatched.append(filename)
                print(f"⚠️  {filename}: 页脚与首页不一致")
        else:
            mismatched.append(filename)
            print(f"❌  {filename}: 未找到页脚")

if not mismatched:
    print("✅ 所有页面的页脚都与首页一致")
else:
    print(f"\n共 {len(mismatched)} 个页面页脚不一致")