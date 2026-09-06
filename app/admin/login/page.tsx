'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });
      const data = await res.json();
      if (data.success) {
        router.push('/admin/dashboard');
        router.refresh();
      } else {
        setError(data.error || '登录失败');
      }
    } catch {
      setError('网络错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(ellipse at top, rgba(0,212,255,0.15), transparent 60%), var(--c-bg)',
      padding: 24,
    }}>
      <div style={{
        width: '100%',
        maxWidth: 400,
        background: 'rgba(15,20,35,0.8)',
        backdropFilter: 'blur(24px)',
        border: '1px solid var(--c-border)',
        borderRadius: 20,
        padding: 40,
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
      }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{
            width: 56, height: 56, margin: '0 auto 16px',
            borderRadius: 16,
            background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <svg width={28} height={28} viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" />
              <path d="M7 11V7a5 5 0 0110 0v4" />
            </svg>
          </div>
          <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 6 }}>后台管理</h1>
          <p style={{ color: 'var(--c-text-muted)', fontSize: 14 }}>请输入管理员密码</p>
        </div>

        <form onSubmit={handleSubmit}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="管理员密码"
            autoFocus
            style={{
              width: '100%', padding: '14px 16px', fontSize: 15,
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid var(--c-border-light)',
              borderRadius: 10, color: 'var(--c-text)',
              outline: 'none', transition: 'all 0.2s',
              marginBottom: 16,
            }}
            onFocus={(e) => { e.target.style.borderColor = 'var(--c-primary)'; }}
            onBlur={(e) => { e.target.style.borderColor = 'var(--c-border-light)'; }}
          />
          {error && (
            <div style={{ color: '#ff6b6b', fontSize: 13, marginBottom: 12, textAlign: 'center' }}>{error}</div>
          )}
          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%', padding: '14px', fontSize: 15, fontWeight: 600,
              background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)',
              border: 'none', borderRadius: 10, color: 'white',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1, transition: 'all 0.2s',
            }}
          >
            {loading ? '登录中...' : '登 录'}
          </button>
        </form>

        <p style={{ textAlign: 'center', color: 'var(--c-text-muted)', fontSize: 12, marginTop: 24 }}>
          © 2026 浦北装修设计
        </p>
      </div>
    </div>
  );
}
