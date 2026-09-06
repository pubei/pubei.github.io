'use client';

import { useState, useEffect } from 'react';
import type { ContactInfo } from '@/lib/types';

export default function ContactAdminPage() {
  const [form, setForm] = useState<ContactInfo>({ phone: '', email: '', address: '', wechat: '', hours: '', lat: '', lng: '' });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch('/api/contact').then((r) => r.json()).then((d) => { if (d.success) setForm(d.data); });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/contact', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form),
    });
    const data = await res.json();
    if (data.success) { setSaved(true); setTimeout(() => setSaved(false), 2000); }
  };

  return (
    <div>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 24 }}>联系资料</h1>
      <form onSubmit={handleSubmit} style={{ maxWidth: 560, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <F label="公司电话" value={form.phone} onChange={(v) => setForm({ ...form, phone: v })} placeholder="134-1227-7880" />
        <F label="邮箱" value={form.email} onChange={(v) => setForm({ ...form, email: v })} placeholder="contact@pboo.top" />
        <F label="公司地址" value={form.address} onChange={(v) => setForm({ ...form, address: v })} />
        <F label="微信号" value={form.wechat} onChange={(v) => setForm({ ...form, wechat: v })} />
        <F label="营业时间" value={form.hours} onChange={(v) => setForm({ ...form, hours: v })} placeholder="周一至周日 09:00 - 18:00" />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <F label="纬度" value={form.lat || ''} onChange={(v) => setForm({ ...form, lat: v })} />
          <F label="经度" value={form.lng || ''} onChange={(v) => setForm({ ...form, lng: v })} />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <button type="submit" style={btnPrimary}>保存</button>
          {saved && <span style={{ color: '#00ff80', fontSize: 14 }}>✓ 已保存</span>}
        </div>
      </form>
    </div>
  );
}

const btnPrimary: React.CSSProperties = { padding: '10px 28px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', border: 'none', borderRadius: 8, color: 'white', fontWeight: 600, cursor: 'pointer', fontSize: 14 };
const inputStyle: React.CSSProperties = { width: '100%', padding: '10px 14px', fontSize: 14, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text)', outline: 'none', fontFamily: 'inherit' };
function F({ label, value, onChange, placeholder }: { label: string; value: string; onChange: (v: string) => void; placeholder?: string }) {
  return <div><label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}</label>
    <input value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} style={inputStyle} /></div>;
}
