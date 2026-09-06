'use client';

import { useState, useEffect } from 'react';
import type { ServiceItem } from '@/lib/types';

export default function ServicesAdminPage() {
  const [items, setItems] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<ServiceItem | null>(null);
  const [form, setForm] = useState({ name: '', icon: '', image: '', description: '', features: '', process: '', order: 0 });

  const fetchData = async () => {
    setLoading(true);
    const res = await fetch('/api/services');
    const data = await res.json();
    if (data.success) setItems(data.data || []);
    setLoading(false);
  };
  useEffect(() => { fetchData(); }, []);

  const openForm = (item?: ServiceItem) => {
    if (item) {
      setEditing(item);
      setForm({ name: item.name, icon: item.icon, image: item.image, description: item.description,
        features: item.features.join('\n'), process: item.process.join('\n'), order: item.order });
    } else {
      setEditing(null);
      setForm({ name: '', icon: '', image: '', description: '', features: '', process: '', order: items.length });
    }
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      ...form,
      features: form.features.split('\n').filter((l) => l.trim()),
      process: form.process.split('\n').filter((l) => l.trim()),
      id: editing?.id,
    };
    const res = await fetch('/api/services', {
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
    const res = await fetch(`/api/services?id=${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) fetchData();
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700 }}>服务项目</h1>
        <button onClick={() => openForm()} style={btnPrimary}>+ 新增服务</button>
      </div>
      {loading ? <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p> :
        items.length === 0 ? <p style={{ color: 'var(--c-text-muted)' }}>暂无服务项目</p> :
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 14 }}>
          {items.map((s) => (
            <div key={s.id} style={cardStyle}>
              <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 6 }}>{s.name}</div>
              <div style={{ fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 12, minHeight: 36 }}>{s.description}</div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button onClick={() => openForm(s)} style={btnSmall}>编辑</button>
                <button onClick={() => handleDelete(s.id)} style={{ ...btnSmall, color: '#ff6b6b', borderColor: 'rgba(255,107,107,0.3)' }}>删除</button>
              </div>
            </div>
          ))}
        </div>}
      {showForm && (
        <div style={modalOverlay}>
          <div style={modalContent}>
            <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 20 }}>{editing ? '编辑服务' : '新增服务'}</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <F label="服务名称" value={form.name} onChange={(v) => setForm({ ...form, name: v })} required />
                <F label="排序" type="number" value={String(form.order)} onChange={(v) => setForm({ ...form, order: Number(v) })} />
              </div>
              <F label="图标 SVG path" value={form.icon} onChange={(v) => setForm({ ...form, icon: v })} placeholder="M3 12h18..." />
              <F label="封面图 URL" value={form.image} onChange={(v) => setForm({ ...form, image: v })} placeholder="https://..." />
              <TA label="描述" value={form.description} onChange={(v) => setForm({ ...form, description: v })} rows={2} />
              <TA label="服务特点（每行一条）" value={form.features} onChange={(v) => setForm({ ...form, features: v })} rows={4} />
              <TA label="服务流程（每行一步）" value={form.process} onChange={(v) => setForm({ ...form, process: v })} rows={4} />
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
const cardStyle: React.CSSProperties = { padding: 18, borderRadius: 14, background: 'rgba(255,255,255,0.03)', border: '1px solid var(--c-border)' };
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
