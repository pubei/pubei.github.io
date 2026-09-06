'use client';

import { useState, useEffect } from 'react';
import type { ProjectItem } from '@/lib/types';

export default function ProjectsAdminPage() {
  const [items, setItems] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<ProjectItem | null>(null);
  const [form, setForm] = useState({ name: '', style: '', layout: '', area: '', address: '', images: '', cover: '', description: '', order: 0 });

  const fetchData = async () => {
    setLoading(true);
    const res = await fetch('/api/projects');
    const data = await res.json();
    if (data.success) setItems(data.data || []);
    setLoading(false);
  };
  useEffect(() => { fetchData(); }, []);

  const openForm = (item?: ProjectItem) => {
    if (item) {
      setEditing(item);
      setForm({ name: item.name, style: item.style, layout: item.layout, area: item.area, address: item.address,
        images: item.images.join('\n'), cover: item.cover, description: item.description, order: item.order });
    } else {
      setEditing(null);
      setForm({ name: '', style: '', layout: '', area: '', address: '', images: '', cover: '', description: '', order: items.length });
    }
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const images = form.images.split('\n').filter((l) => l.trim());
    const payload = { ...form, images, cover: form.cover || images[0] || '', id: editing?.id };
    const res = await fetch('/api/projects', {
      method: editing ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.success) { setShowForm(false); fetchData(); }
    else alert(data.error);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除？')) return;
    const res = await fetch(`/api/projects?id=${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) fetchData();
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700 }}>装修案例</h1>
        <button onClick={() => openForm()} style={btnPrimary}>+ 新增案例</button>
      </div>
      {loading ? <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p> :
        items.length === 0 ? <p style={{ color: 'var(--c-text-muted)' }}>暂无案例</p> :
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 14 }}>
          {items.map((p) => (
            <div key={p.id} style={{ borderRadius: 14, overflow: 'hidden', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--c-border)' }}>
              {p.cover && <img src={p.cover} alt={p.name} style={{ width: '100%', height: 140, objectFit: 'cover' }} />}
              <div style={{ padding: 14 }}>
                <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 4 }}>{p.name}</div>
                <div style={{ fontSize: 12, color: 'var(--c-text-muted)', marginBottom: 12 }}>{p.style} · {p.area}</div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <button onClick={() => openForm(p)} style={btnSmall}>编辑</button>
                  <button onClick={() => handleDelete(p.id)} style={{ ...btnSmall, color: '#ff6b6b', borderColor: 'rgba(255,107,107,0.3)' }}>删除</button>
                </div>
              </div>
            </div>
          ))}
        </div>}
      {showForm && (
        <div style={modalOverlay}>
          <div style={modalContent}>
            <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 20 }}>{editing ? '编辑案例' : '新增案例'}</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <F label="案例名称" value={form.name} onChange={(v) => setForm({ ...form, name: v })} required />
                <F label="装修风格" value={form.style} onChange={(v) => setForm({ ...form, style: v })} />
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
                <F label="户型" value={form.layout} onChange={(v) => setForm({ ...form, layout: v })} />
                <F label="面积" value={form.area} onChange={(v) => setForm({ ...form, area: v })} />
                <F label="排序" type="number" value={String(form.order)} onChange={(v) => setForm({ ...form, order: Number(v) })} />
              </div>
              <F label="项目地址" value={form.address} onChange={(v) => setForm({ ...form, address: v })} />
              <F label="封面图 URL" value={form.cover} onChange={(v) => setForm({ ...form, cover: v })} placeholder="https://..." />
              <TA label="图片集（每行一个 URL）" value={form.images} onChange={(v) => setForm({ ...form, images: v })} rows={4} />
              <TA label="案例描述" value={form.description} onChange={(v) => setForm({ ...form, description: v })} rows={4} />
              <div style={{ display: 'flex', gap: 12 }}>
                <button type="submit" style={{ ...btnPrimary, flex: 1 }}>{editing ? '保存' : '新增'}</button>
                <button type="button" onClick={() => setShowForm(false)} style={btnCancel}>取消</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

const btnPrimary: React.CSSProperties = { padding: '10px 20px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', border: 'none', borderRadius: 8, color: 'white', fontWeight: 600, cursor: 'pointer', fontSize: 14 };
const btnSmall: React.CSSProperties = { padding: '6px 14px', background: 'transparent', border: '1px solid var(--c-border-light)', borderRadius: 6, color: 'var(--c-text-sec)', cursor: 'pointer', fontSize: 13 };
const btnCancel: React.CSSProperties = { padding: '10px 20px', background: 'transparent', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text-sec)', cursor: 'pointer', fontSize: 14 };
const modalOverlay: React.CSSProperties = { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: 20 };
const modalContent: React.CSSProperties = { background: 'rgba(15,20,35,0.95)', backdropFilter: 'blur(20px)', border: '1px solid var(--c-border)', borderRadius: 18, padding: 32, width: '100%', maxWidth: 600, maxHeight: '90vh', overflowY: 'auto' };
const inputStyle: React.CSSProperties = { width: '100%', padding: '10px 14px', fontSize: 14, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text)', outline: 'none', fontFamily: 'inherit' };
function F({ label, value, onChange, type = 'text', required, placeholder }: { label: string; value: string; onChange: (v: string) => void; type?: string; required?: boolean; placeholder?: string }) {
  return <div><label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}{required && ' *'}</label>
    <input type={type} value={value} required={required} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} style={inputStyle} /></div>;
}
function TA({ label, value, onChange, rows = 4 }: { label: string; value: string; onChange: (v: string) => void; rows?: number }) {
  return <div><label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}</label>
    <textarea value={value} rows={rows} onChange={(e) => onChange(e.target.value)} style={{ ...inputStyle, resize: 'vertical' }} /></div>;
}
