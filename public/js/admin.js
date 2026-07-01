// 简单后台登录与获取留言/新增作品（仅用于演示）
document.addEventListener('DOMContentLoaded', () => {
  const btnLogin = document.getElementById('btnLogin');
  const loginResult = document.getElementById('loginResult');
  const manageBox = document.getElementById('manageBox');
  const loginBox = document.getElementById('loginBox');

  const token = localStorage.getItem('ADMIN_TOKEN');
  if (token) {
    showManage(token);
  }

  btnLogin && btnLogin.addEventListener('click', async () => {
    const pwd = document.getElementById('adminPassword').value;
    const res = await fetch('/api/login', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ password: pwd }) });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('ADMIN_TOKEN', data.token);
      showManage(data.token);
    } else {
      loginResult.textContent = '登录失败';
    }
  });

  async function showManage(token) {
    loginBox.style.display = 'none';
    manageBox.style.display = 'block';
    loadMessages(token);
    document.getElementById('btnAddProj').addEventListener('click', async () => {
      const title = document.getElementById('projTitle').value;
      const image = document.getElementById('projImage').value;
      const desc = document.getElementById('projDesc').value;
      const res = await fetch('/api/projects', {
        method:'POST',
        headers:{'Content-Type':'application/json','x-admin-token': token},
        body: JSON.stringify({ title, image, description: desc })
      });
      if (res.ok) {
        alert('新增成功，刷新作品页查看。');
        document.getElementById('projTitle').value='';
        document.getElementById('projImage').value='';
        document.getElementById('projDesc').value='';
      } else {
        alert('新增失败');
      }
    });
  }

  async function loadMessages(token) {
    const list = document.getElementById('messagesList');
    list.innerHTML = '<p>加载中…</p>';
    try {
      const res = await fetch('/api/messages', { headers: { 'x-admin-token': token }});
      if (!res.ok) throw new Error('unauth');
      const data = await res.json();
      if (!data.length) list.innerHTML = '<p>暂无留言。</p>';
      else {
        list.innerHTML = '';
        data.forEach(m => {
          const el = document.createElement('div');
          el.className = 'glass card';
          el.innerHTML = `<strong>${m.name}</strong> <small>${new Date(m.createdAt).toLocaleString()}</small><p>${m.message}</p><p>电话：${m.phone||'-'} 邮箱：${m.email||'-'}</p>`;
          list.appendChild(el);
        });
      }
    } catch (e) {
      list.innerHTML = '<p>加载失败（可能未登录）</p>';
    }
  }
});
