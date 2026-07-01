// 负责项目列表加载与联系表单提交
document.addEventListener('DOMContentLoaded', () => {
  const projectsList = document.getElementById('projectsList');
  if (projectsList) loadProjects(projectsList);

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(contactForm).entries());
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
      });
      const result = document.getElementById('contactResult');
      if (res.ok) {
        result.textContent = '留言已发送，我们会尽快联系您。';
        contactForm.reset();
      } else {
        const err = await res.json();
        result.textContent = '发送失败: ' + (err.error||res.statusText);
      }
    });
  }
});

async function loadProjects(container){
  container.innerHTML = '<p>加载中…</p>';
  try {
    const res = await fetch('/api/projects');
    const list = await res.json();
    if (!list.length) container.innerHTML = '<p>暂无作品，稍后更新。</p>';
    else {
      container.innerHTML = '';
      list.forEach(p => {
        const card = document.createElement('article');
        card.className = 'project glass';
        card.innerHTML = `
          <img src="${p.image}" alt="${escapeHtml(p.title)}" />
          <div class="meta">
            <h4>${escapeHtml(p.title)}</h4>
            <p>${escapeHtml(p.description)}</p>
          </div>
        `;
        container.appendChild(card);
      });
    }
  } catch (e) {
    container.innerHTML = '<p>加载失败</p>';
  }
}

function escapeHtml(s=''){ return s.replaceAll && s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;') || s; }
