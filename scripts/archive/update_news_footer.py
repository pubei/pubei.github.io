import os

html_files = [
    'index.html', 'services.html', 'projects.html', 'about.html', 'contact.html',
    'faq.html', 'privacy.html', 'terms.html',
    'service-detail-custom.html', 'service-detail-new.html', 'service-detail-renovation.html',
    'service-detail-soft.html', 'service-detail-smart.html', 'service-detail-partial.html',
    'project-detail-1.html', 'project-detail-2.html', 'project-detail-3.html',
    'project-detail-4.html', 'project-detail-5.html', 'project-detail-6.html'
]

old_link = '''              <li><span class="footer-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg></span><a href="about.html">关于我们</a></li>'''

new_link = '''              <li><span class="footer-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg></span><a href="news.html">公司新闻</a></li>
              <li><span class="footer-link-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg></span><a href="about.html">关于我们</a></li>'''

for filename in html_files:
    filepath = os.path.join('/Users/mac/Downloads/static', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_link in content and new_link not in content:
            content = content.replace(old_link, new_link)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filename}")
        else:
            print(f"Already updated or no match: {filename}")

print("\nDone!")