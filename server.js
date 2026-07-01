const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const DATA_FILE = path.join(__dirname, 'data.json');
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';
const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'dev-token-please-change';

function loadData() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (e) {
    return { projects: [], messages: [] };
  }
}
function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

const app = express();
app.use(bodyParser.json());
app.use(require('cors')());
app.use(express.static(path.join(__dirname, 'public')));

// API: 获取作品
app.get('/api/projects', (req, res) => {
  const data = loadData();
  res.json(data.projects);
});

// API: 新增作品（简单权限，需 x-admin-token）
app.post('/api/projects', (req, res) => {
  const token = req.headers['x-admin-token'];
  if (token !== ADMIN_TOKEN) return res.status(401).json({ error: 'unauthorized' });
  const data = loadData();
  const nextId = (data.projects.reduce((a,b)=>Math.max(a,b.id||0),0) || 0) + 1;
  const p = { id: nextId, title: req.body.title||'Untitled', description: req.body.description||'', image: req.body.image||'' };
  data.projects.push(p);
  saveData(data);
  res.json(p);
});

// API: 联系表单
app.post('/api/contact', (req, res) => {
  const { name, phone, email, message } = req.body;
  if (!name || !message) return res.status(400).json({ error: 'name and message required' });
  const data = loadData();
  const item = { id: Date.now(), name, phone, email, message, createdAt: new Date().toISOString() };
  data.messages.push(item);
  saveData(data);
  res.json({ ok: true });
});

// API: 管理登录（演示）
app.post('/api/login', (req, res) => {
  const { password } = req.body;
  if (password === ADMIN_PASSWORD) {
    return res.json({ token: ADMIN_TOKEN });
  } else {
    return res.status(403).json({ error: 'invalid' });
  }
});

// API: 获取留言（admin）
app.get('/api/messages', (req, res) => {
  const token = req.headers['x-admin-token'];
  if (token !== ADMIN_TOKEN) return res.status(401).json({ error: 'unauthorized' });
  const data = loadData();
  res.json(data.messages);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Server running on http://localhost:' + PORT);
});
