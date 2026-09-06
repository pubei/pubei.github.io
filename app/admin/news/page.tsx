'use client';

import { useState, useEffect } from 'react';
import type { NewsItem } from '@/lib/types';

export default function NewsAdminPage() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<NewsItem | null>(null);
  const [form, setForm] = useState({
    title: '', category: '全屋定制', image: '', excerpt: '', content: '',
    date: new Date().toISOString().slice(0, 10), published: true,
  });

  const fetchNews = async () => {
    setLoading(true);
    const res = await fetch('/api/news?all=true');
    const data = await res.json();
    if (data.success) setNews(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchNews(); }, []);

  const openForm = (item?: NewsItem) => {
    if (item) {
      setEditing(item);
      setForm({
        title: item.title, category: item.category, image: item.image,
        excerpt: item.excerpt, content: Array.isArray(item.content) ? item.content.join('\n') : item.content,
        date: item.date, published: item.published,
      });
    } else {
      setEditing(null);
      setForm({
        title: '', category: '全屋定制', image: '', excerpt: '', content: '',
        date: new Date().toISOString().slice(0, 10), published: true,
      });
    }
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      ...form,
      content: form.content.split('\n').filter((l) => l.trim()),
      id: editing?.id,
    };
    const res = await fetch('/api/news', {
      method: editing ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.success) {
      setShowForm(false);
      fetchNews();
    } else {
      alert(data.error);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除这条新闻吗？')) return;
    const res = await fetch(`/api/news?id=${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) fetchNews();
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700 }}>新闻管理</h1>
        <button onClick={() => openForm()} style={btnPrimary}>+ 发布新闻</button>
      </div>

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : news.length === 0 ? (
        <p style={{ color: 'var(--c-text-muted)' }}>暂无新闻</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {news.map((n) => (
            <div key={n.id} style={rowStyle}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 500, fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{n.title}</div>
                <div style={{ fontSize: 12, color: 'var(--c-text-muted)', marginTop: 4 }}>
                  {n.category} · {n.date} {!n.published && '· 未发布'}
                </div>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button onClick={() => openForm(n)} style={btnSmall}>编辑</button>
                <button onClick={() => handleDelete(n.id)} style={{ ...btnSmall, color: '#ff6b6b', borderColor: 'rgba(255,107,107,0.3)' }}>删除</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showForm && (
        <div style={modalOverlay}>
          <div style={modalContent}>
            <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 20 }}>{editing ? '编辑新闻' : '发布新闻'}</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <InputField label="标题" value={form.title} onChange={(v) => setForm({ ...form, title: v })} required />
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <SelectField label="分类" value={form.category} onChange={(v) => setForm({ ...form, category: v })}
                  options={['全屋定制', '装修设计', '行业资讯', '公司动态']} />
                <InputField label="日期" type="date" value={form.date} onChange={(v) => setForm({ ...form, date: v })} />
              </div>
              <InputField label="封面图 URL" value={form.image} onChange={(v) => setForm({ ...form, image: v })} placeholder="https://..." />
              <TextareaField label="摘要" value={form.excerpt} onChange={(v) => setForm({ ...form, excerpt: v })} rows={2} />
              <TextareaField label="正文（每行一段）" value={form.content} onChange={(v) => setForm({ ...form, content: v })} rows={8} />
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14, cursor: 'pointer' }}>
                <input type="checkbox" checked={form.published} onChange={(e) => setForm({ ...form, published: e.target.checked })} />
                立即发布
              </label>
              <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
                <button type="submit" style={{ ...btnPrimary, flex: 1 }}>{editing ? '保存' : '发布'}</button>
                <button type="button" onClick={() => setShowForm(false)} style={btnCancel}>取消</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

// 可复用样式和组件
const btnPrimary: React.CSSProperties = {
  padding: '10px 20px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)',
  border: 'none', borderRadius: 8, color: 'white', fontWeight: 600, cursor: 'pointer', fontSize: 14,
};
const btnSmall: React.CSSProperties = {
  padding: '6px 14px', background: 'transparent', border: '1px solid var(--c-border-light)',
  borderRadius: 6, color: 'var(--c-text-sec)', cursor: 'pointer', fontSize: 13,
};
const btnCancel: React.CSSProperties = {
  padding: '10px 20px', background: 'transparent', border: '1px solid var(--c-border-light)',
  borderRadius: 8, color: 'var(--c-text-sec)', cursor: 'pointer', fontSize: 14,
};
const rowStyle: React.CSSProperties = {
  display: 'flex', alignItems: 'center', gap: 12,
  padding: '14px 18px', borderRadius: 12,
  background: 'rgba(255,255,255,0.03)', border: '1px solid var(--c-border)',
};
const modalOverlay: React.CSSProperties = {
  position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
  display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: 20,
};
const modalContent: React.CSSProperties = {
  background: 'rgba(15,20,35,0.95)', backdropFilter: 'blur(20px)',
  border: '1px solid var(--c-border)', borderRadius: 18, padding: 32,
  width: '100%', maxWidth: 600, maxHeight: '90vh', overflowY: 'auto',
};

function InputField({ label, value, onChange, type = 'text', required, placeholder }: {
  label: string; value: string; onChange: (v: string) => void; type?: string; required?: boolean; placeholder?: string;
}) {
  return (
    <div>
      <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}{required && ' *'}</label>
      <input type={type} value={value} required={required} placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        style={inputStyle} />
    </div>
  );
}

function SelectField({ label, value, onChange, options }: {
  label: string; value: string; onChange: (v: string) => void; options: string[];
}) {
  return (
    <div>
      <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)} style={inputStyle}>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );
}

function TextareaField({ label, value, onChange, rows = 4 }: {
  label: string; value: string; onChange: (v: string) => void; rows?: number;
}) {
  return (
    <div>
      <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}</label>
      <textarea value={value} rows={rows} onChange={(e) => onChange(e.target.value)}
        style={{ ...inputStyle, resize: 'vertical', fontFamily: 'inherit' }} />
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  width: '100%', padding: '10px 14px', fontSize: 14,
  background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)',
  borderRadius: 8, color: 'var(--c-text)', outline: 'none',
};
