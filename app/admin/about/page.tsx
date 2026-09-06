'use client';

import { useState, useEffect } from 'react';
import type { AboutInfo } from '@/lib/types';

export default function AboutAdminPage() {
  const [form, setForm] = useState<AboutInfo>({ intro: '', vision: '', stats: [], commitments: [], history: [] });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch('/api/about').then((r) => r.json()).then((d) => { if (d.success) setForm(d.data); });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/about', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form),
    });
    const data = await res.json();
    if (data.success) { setSaved(true); setTimeout(() => setSaved(false), 2000); }
  };

  const statsStr = form.stats.map((s) => `${s.label}|${s.value}`).join('\n');
  const commitmentsStr = form.commitments.join('\n');
  const historyStr = form.history.map((h) => `${h.year}|${h.event}`).join('\n');

  return (
    <div>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 24 }}>公司资料</h1>
      <form onSubmit={handleSubmit} style={{ maxWidth: 640, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <TA label="公司简介" value={form.intro} onChange={(v) => setForm({ ...form, intro: v })} rows={4} />
        <TA label="公司愿景" value={form.vision} onChange={(v) => setForm({ ...form, vision: v })} rows={2} />
        <TA label="统计数据（每行：标签|数值，如：服务客户|500+）" value={statsStr} onChange={(v) => setForm({ ...form, stats: v.split('\n').filter((l) => l.includes('|')).map((l) => { const [label, value] = l.split('|'); return { label, value }; }) })} rows={5} />
        <TA label="服务承诺（每行一条）" value={commitmentsStr} onChange={(v) => setForm({ ...form, commitments: v.split('\n').filter((l) => l.trim()) })} rows={4} />
        <TA label="发展历程（每行：年份|事件，如：2014|公司成立）" value={historyStr} onChange={(v) => setForm({ ...form, history: v.split('\n').filter((l) => l.includes('|')).map((l) => { const [year, event] = l.split('|'); return { year, event }; }) })} rows={5} />
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
function TA({ label, value, onChange, rows = 4 }: { label: string; value: string; onChange: (v: string) => void; rows?: number }) {
  return <div><label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>{label}</label>
    <textarea value={value} rows={rows} onChange={(e) => onChange(e.target.value)} style={{ ...inputStyle, resize: 'vertical' }} /></div>;
}
