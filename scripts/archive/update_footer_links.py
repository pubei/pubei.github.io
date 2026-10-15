import os

html_files = [
    'services.html', 'projects.html', 'about.html', 'contact.html',
    'faq.html', 'privacy.html', 'terms.html',
    'service-detail-custom.html', 'service-detail-new.html', 'service-detail-renovation.html',
    'service-detail-soft.html', 'service-detail-smart.html', 'service-detail-partial.html',
    'project-detail-1.html', 'project-detail-2.html', 'project-detail-3.html',
    'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html'
]

old_text = '装修案例</a></li>\n              <li><a href="about.html">'
new_text = '装修案例</a></li>\n              <li><a href="news.html"><span class="footer-link-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg></span> 公司新闻</a></li>\n              <li><a href="about.html">'

for filename in html_files:
    filepath = os.path.join('/Users/mac/Downloads/static', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filename}")
        else:
            print(f"No match or already updated: {filename}")

print("\nDone!")