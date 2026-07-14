import os
import re

new_inline_style = '''<link rel="stylesheet" href="assets/css/style.css?v=5">
  <style>
    .footer-content {
      display: grid !important;
      grid-template-columns: 280px 1fr 1fr !important;
      gap: 2.5rem !important;
    }
    .footer-brand {
      grid-column: span 1 !important;
    }
    .footer-links, .footer-services {
      grid-column: span 1 !important;
    }
    .footer-contact-section {
      grid-column: span 2 !important;
      display: grid !important;
      grid-template-columns: 1fr 1fr !important;
      gap: 2rem !important;
      align-items: start !important;
    }
    .promise-list {
      display: grid !important;
      grid-template-columns: 1fr 1fr !important;
      gap: 0.75rem !important;
    }
    .promise-item {
      display: flex !important;
      align-items: center !important;
      gap: 0.5rem !important;
    }
    .promise-icon {
      width: 32px !important;
      height: 32px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: rgba(123, 47, 247, 0.1) !important;
      border-radius: 50% !important;
      flex-shrink: 0 !important;
    }
    .promise-icon svg {
      width: 16px !important;
      height: 16px !important;
    }
    .promise-text {
      font-size: 0.85rem !important;
    }
    @media (max-width: 1024px) {
      .footer-content {
        grid-template-columns: 1fr 1fr !important;
        gap: 2rem !important;
      }
      .footer-brand {
        grid-column: span 2 !important;
      }
      .footer-contact-section {
        grid-column: span 2 !important;
      }
    }
    @media (max-width: 768px) {
      .footer-content {
        grid-template-columns: 1fr !important;
        gap: 1.5rem !important;
        text-align: center !important;
      }
      .footer-links, .footer-services {
        grid-column: span 1 !important;
      }
      .footer-contact-section {
        grid-template-columns: 1fr !important;
        text-align: center !important;
      }
      .promise-list {
        grid-template-columns: 1fr !important;
      }
      .promise-item {
        justify-content: center !important;
      }
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''

old_footer_section = '''          <div class="footer-contact">
            <h4>联系我们</h4>
            <div class="contact-list">
              <div class="contact-item">
                <span class="contact-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-2.2 2.2a15.056 15.056 0 01-6.59-6.59l2.2-2.21a.96.96 0 00.25-1.01A11.36 11.36 0 018.62 3.99C8.62 3.45 8.17 3 7.63 3H4.02C3.48 3 3 3.48 3 4.02c0 9.39 7.61 17 17 17 .54 0 1.02-.48 1.02-1.02v-3.6c0-.54-.45-.99-.99-.99z"/></svg>
                </span>
                <div>
                  <span class="contact-label">电话</span>
                  <span class="contact-value">134-1227-7880</span>
                </div>
              </div>
              <div class="contact-item">
                <span class="contact-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>
                </span>
                <div>
                  <span class="contact-label">手机</span>
                  <span class="contact-value">13412277880</span>
                </div>
              </div>
              <div class="contact-item">
                <span class="contact-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                </span>
                <div>
                  <span class="contact-label">地址</span>
                  <span class="contact-value">浦北县小江街道XX路XX号</span>
                </div>
              </div>
              <div class="contact-item">
                <span class="contact-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                </span>
                <div>
                  <span class="contact-label">邮箱</span>
                  <span class="contact-value">contact@pboo.top</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="footer-promises">
            <h4>服务承诺</h4>
            <div class="promise-list">
              <div class="promise-item">
                <span class="promise-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                </span>
                <span class="promise-text">免费设计咨询</span>
              </div>
              <div class="promise-item">
                <span class="promise-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>
                </span>
                <span class="promise-text">透明报价体系</span>
              </div>
              <div class="promise-item">
                <span class="promise-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>
                </span>
                <span class="promise-text">准时交付保障</span>
              </div>
              <div class="promise-item">
                <span class="promise-icon">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                </span>
                <span class="promise-text">终身售后服务</span>
              </div>
            </div>
          </div>'''

new_footer_section = '''          <div class="footer-contact-section">
            <div class="footer-contact">
              <h4>联系我们</h4>
              <div class="contact-list">
                <div class="contact-item">
                  <span class="contact-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-2.2 2.2a15.056 15.056 0 01-6.59-6.59l2.2-2.21a.96.96 0 00.25-1.01A11.36 11.36 0 018.62 3.99C8.62 3.45 8.17 3 7.63 3H4.02C3.48 3 3 3.48 3 4.02c0 9.39 7.61 17 17 17 .54 0 1.02-.48 1.02-1.02v-3.6c0-.54-.45-.99-.99-.99z"/></svg>
                  </span>
                  <div>
                    <span class="contact-label">电话</span>
                    <span class="contact-value">134-1227-7880</span>
                  </div>
                </div>
                <div class="contact-item">
                  <span class="contact-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>
                  </span>
                  <div>
                    <span class="contact-label">手机</span>
                    <span class="contact-value">13412277880</span>
                  </div>
                </div>
                <div class="contact-item">
                  <span class="contact-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                  </span>
                  <div>
                    <span class="contact-label">地址</span>
                    <span class="contact-value">浦北县小江街道XX路XX号</span>
                  </div>
                </div>
                <div class="contact-item">
                  <span class="contact-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                  </span>
                  <div>
                    <span class="contact-label">邮箱</span>
                    <span class="contact-value">contact@pboo.top</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="footer-promises">
              <h4>服务承诺</h4>
              <div class="promise-list">
                <div class="promise-item">
                  <span class="promise-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                  </span>
                  <span class="promise-text">免费设计咨询</span>
                </div>
                <div class="promise-item">
                  <span class="promise-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>
                  </span>
                  <span class="promise-text">透明报价体系</span>
                </div>
                <div class="promise-item">
                  <span class="promise-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg>
                  </span>
                  <span class="promise-text">准时交付保障</span>
                </div>
                <div class="promise-item">
                  <span class="promise-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                  </span>
                  <span class="promise-text">终身售后服务</span>
                </div>
              </div>
            </div>
          </div>'''

for file in os.listdir('.'):
    if file.endswith('.html') and file != 'index.html':
        with open(file, 'r') as f:
            content = f.read()
        
        content = re.sub(r'<link rel="stylesheet" href="assets/css/style.css[^"]*">', '<link rel="stylesheet" href="assets/css/style.css?v=5">', content)
        
        content = content.replace('<link rel="stylesheet" href="assets/css/style.css?v=5">\n  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">', new_inline_style)
        content = content.replace('<link rel="stylesheet" href="assets/css/style.css?v=5">\n  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">', new_inline_style)
        
        if old_footer_section in content:
            content = content.replace(old_footer_section, new_footer_section)
            with open(file, 'w') as f:
                f.write(content)
            print(f'Updated: {file}')
