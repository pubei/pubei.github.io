'use client';

import { useState } from 'react';

export default function ContactForm() {
  const [form, setForm] = useState({ name: '', phone: '', email: '', message: '' });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMsg('');

    // 简单校验
    if (!form.name || !form.phone) {
      setErrorMsg('请填写姓名和手机号');
      setStatus('error');
      return;
    }
    if (!/^1\d{10}$/.test(form.phone)) {
      setErrorMsg('请输入正确的11位手机号');
      setStatus('error');
      return;
    }

    // 防垃圾：检查姓名和留言
    const spamKeywords = ['广告', '推广', '代开发票', '刷单', '兼职'];
    const checkText = (form.name + form.message).toLowerCase();
    if (spamKeywords.some((k) => checkText.includes(k))) {
      setErrorMsg('提交内容包含违规信息');
      setStatus('error');
      return;
    }

    try {
      const web3Key = process.env.NEXT_PUBLIC_WEB3FORMS_KEY;
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          access_key: web3Key,
          姓名: form.name,
          手机号: form.phone,
          邮箱: form.email,
          留言: form.message,
          来源: '官网预约表单',
        }),
      });
      const data = await res.json();
      if (data.success) {
        setStatus('success');
        setForm({ name: '', phone: '', email: '', message: '' });
      } else {
        setErrorMsg('提交失败，请稍后重试');
        setStatus('error');
      }
    } catch {
      setErrorMsg('网络错误，请稍后重试');
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div style={{ padding: 32, borderRadius: 16, background: 'rgba(0,255,128,0.08)', border: '1px solid rgba(0,255,128,0.25)', textAlign: 'center' }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>✅</div>
        <h3 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>提交成功！</h3>
        <p style={{ color: 'var(--c-text-sec)' }}>我们会尽快与您联系，请保持电话畅通。</p>
        <button onClick={() => setStatus('idle')} style={{ marginTop: 16, padding: '8px 20px', background: 'transparent', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text-sec)', cursor: 'pointer' }}>
          再次提交
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} style={{ padding: 32, borderRadius: 16, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', display: 'flex', flexDirection: 'column', gap: 16 }}>
      <h2 style={{ fontSize: 20, fontWeight: 600 }}>预约咨询</h2>
      <input style={input} placeholder="姓名 *" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
      <input style={input} placeholder="手机号 *" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
      <input style={input} placeholder="邮箱" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <textarea style={{ ...input, minHeight: 100, resize: 'vertical' }} placeholder="留言" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} />
      {errorMsg && <div style={{ color: '#ff6b6b', fontSize: 13 }}>{errorMsg}</div>}
      <button type="submit" disabled={status === 'loading'} style={{ padding: '14px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', border: 'none', borderRadius: 10, color: 'white', fontWeight: 600, fontSize: 16, cursor: status === 'loading' ? 'not-allowed' : 'pointer', opacity: status === 'loading' ? 0.7 : 1 }}>
        {status === 'loading' ? '提交中...' : '提交预约'}
      </button>
    </form>
  );
}

const input: React.CSSProperties = {
  width: '100%', padding: '12px 16px', fontSize: 15,
  background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)',
  borderRadius: 10, color: 'var(--c-text)', outline: 'none', fontFamily: 'inherit',
};
