import os

new_footer_section = '''          <div class="footer-contact">
            <h4>联系我们</h4>
            <ul>
              <li><span class="footer-link-icon">📞</span> 电话：134-1227-7880</li>
              <li><span class="footer-link-icon">📱</span> 手机：13412277880</li>
              <li><span class="footer-link-icon">📍</span> 地址：浦北县小江街道XX路XX号</li>
              <li><span class="footer-link-icon">📧</span> 邮箱：contact@pboo.top</li>
            </ul>
          </div>
          
          <div class="footer-promises">
            <h4>服务承诺</h4>
            <ul>
              <li><span class="footer-link-icon">✅</span> 免费设计咨询</li>
              <li><span class="footer-link-icon">✅</span> 透明报价体系</li>
              <li><span class="footer-link-icon">✅</span> 准时交付保障</li>
              <li><span class="footer-link-icon">✅</span> 终身售后服务</li>
            </ul>
          </div>'''

old_footer_section1 = '''          <div class="footer-contact-section">
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

old_footer_section2 = '''        <div class="footer-contact-section">
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

for file in os.listdir('.'):
    if file.endswith('.html') and file != 'index.html':
        with open(file, 'r') as f:
            content = f.read()
        
        if old_footer_section1 in content:
            content = content.replace(old_footer_section1, new_footer_section)
            with open(file, 'w') as f:
                f.write(content)
            print(f'Updated (type1): {file}')
        elif old_footer_section2 in content:
            content = content.replace(old_footer_section2, new_footer_section)
            with open(file, 'w') as f:
                f.write(content)
            print(f'Updated (type2): {file}')
