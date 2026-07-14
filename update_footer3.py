import os

new_footer_section = '''        <div class="footer-contact-section">
          <div class="footer-contact">
            <h4>联系我们</h4>
            <div class="contact-list">
              <div class="contact-item"><span class="contact-icon">📞</span><div><span class="contact-label">电话</span><span class="contact-value">134-1227-7880</span></div></div>
              <div class="contact-item"><span class="contact-icon">📱</span><div><span class="contact-label">手机</span><span class="contact-value">13412277880</span></div></div>
              <div class="contact-item"><span class="contact-icon">📍</span><div><span class="contact-label">地址</span><span class="contact-value">浦北县小江街道XX路XX号</span></div></div>
              <div class="contact-item"><span class="contact-icon">📧</span><div><span class="contact-label">邮箱</span><span class="contact-value">contact@pboo.top</span></div></div>
            </div>
          </div>
          
          <div class="footer-promises">
            <h4>服务承诺</h4>
            <div class="promise-list">
              <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">免费设计咨询</span></div>
              <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">透明报价体系</span></div>
              <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">准时交付保障</span></div>
              <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">终身售后服务</span></div>
            </div>
          </div>
        </div>'''

old_footer_section = '''        <div class="footer-contact">
          <h4>联系我们</h4>
          <div class="contact-list">
            <div class="contact-item"><span class="contact-icon">📞</span><div><span class="contact-label">电话</span><span class="contact-value">134-1227-7880</span></div></div>
            <div class="contact-item"><span class="contact-icon">📱</span><div><span class="contact-label">手机</span><span class="contact-value">13412277880</span></div></div>
            <div class="contact-item"><span class="contact-icon">📍</span><div><span class="contact-label">地址</span><span class="contact-value">浦北县小江街道XX路XX号</span></div></div>
            <div class="contact-item"><span class="contact-icon">📧</span><div><span class="contact-label">邮箱</span><span class="contact-value">contact@pboo.top</span></div></div>
          </div>
        </div>
        
        <div class="footer-promises">
          <h4>服务承诺</h4>
          <div class="promise-list">
            <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">免费设计咨询</span></div>
            <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">透明报价体系</span></div>
            <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">准时交付保障</span></div>
            <div class="promise-item"><span class="promise-icon">✅</span><span class="promise-text">终身售后服务</span></div>
          </div>
        </div>'''

for file in os.listdir('.'):
    if file.endswith('.html') and file.startswith('service-detail'):
        with open(file, 'r') as f:
            content = f.read()
        
        if old_footer_section in content:
            content = content.replace(old_footer_section, new_footer_section)
            with open(file, 'w') as f:
                f.write(content)
            print(f'Updated: {file}')
