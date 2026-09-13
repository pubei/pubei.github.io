'use client';

/**
 * 共享 UI 组件库 - 暗色玻璃拟态风格
 * 所有新 admin 页面统一使用，与现有 app/admin/login 风格一致
 * 颜色：--c-bg #0a0e17 / --c-primary #00d4ff / --c-secondary #7b2ff7
 */
import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import ImageUpload from './ImageUpload';

// ==================== Button ====================
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost' | 'gradient';
type ButtonSize = 'sm' | 'md' | 'lg';
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  block?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
}
export function Button({
  variant = 'primary', size = 'md', block, loading, icon, children, disabled, ...rest
}: ButtonProps) {
  const base: React.CSSProperties = {
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 8,
    borderRadius: 10, cursor: disabled || loading ? 'not-allowed' : 'pointer',
    opacity: disabled || loading ? 0.65 : 1, transition: 'all 0.25s ease',
    border: '1px solid transparent', fontWeight: 600, fontFamily: 'inherit',
    whiteSpace: 'nowrap', userSelect: 'none',
  };
  if (block) base.width = '100%';
  if (size === 'sm') { base.padding = '6px 14px'; base.fontSize = 13; }
  else if (size === 'lg') { base.padding = '14px 24px'; base.fontSize = 16; }
  else { base.padding = '10px 20px'; base.fontSize = 14; }
  if (variant === 'primary' || variant === 'gradient') {
    base.background = 'linear-gradient(135deg, #00d4ff, #7b2ff7)';
    base.color = '#fff';
    base.border = 'none';
    base.boxShadow = '0 6px 20px rgba(0,212,255,0.25)';
  } else if (variant === 'secondary') {
    base.background = 'rgba(255,255,255,0.05)';
    base.color = 'var(--c-text)';
    base.borderColor = 'var(--c-border-light)';
  } else if (variant === 'danger') {
    base.background = 'rgba(255,107,107,0.1)';
    base.color = '#ff6b6b';
    base.borderColor = 'rgba(255,107,107,0.35)';
  } else { // ghost
    base.background = 'transparent';
    base.color = 'var(--c-text-sec)';
    base.borderColor = 'transparent';
  }
  return (
    <button style={base} disabled={disabled || loading} {...rest}>
      {loading ? <Spinner size={size === 'lg' ? 18 : 14} /> : icon}
      {children}
    </button>
  );
}

function Spinner({ size = 14 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{ animation: 'spin 1s linear infinite' }}>
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeOpacity="0.25" strokeWidth="4" />
      <path d="M4 12a8 8 0 018-8" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </svg>
  );
}

// ==================== IconButton ====================
interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  tone?: 'default' | 'danger' | 'primary';
}
export function IconButton({ label, tone = 'default', children, ...rest }: IconButtonProps) {
  const color = tone === 'danger' ? '#ff6b6b' : tone === 'primary' ? 'var(--c-primary)' : 'var(--c-text-sec)';
  const style: React.CSSProperties = {
    padding: '6px 10px', background: 'transparent', border: `1px solid ${tone === 'danger' ? 'rgba(255,107,107,0.3)' : 'var(--c-border-light)'}`,
    borderRadius: 6, color, cursor: 'pointer', fontSize: 13, display: 'inline-flex', alignItems: 'center', gap: 6,
    transition: 'all 0.2s',
  };
  return <button style={style} title={label} {...rest}>{children}<span>{label}</span></button>;
}

// ==================== Input / Textarea / Select ====================
const fieldBase: React.CSSProperties = {
  width: '100%', padding: '10px 14px', fontSize: 14,
  background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)',
  borderRadius: 8, color: 'var(--c-text)', outline: 'none', fontFamily: 'inherit',
  transition: 'all 0.2s',
};
interface FieldProps {
  label?: string;
  required?: boolean;
  hint?: string;
  error?: string;
}
export function Input({ label, required, hint, error, ...rest }: FieldProps & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div>
      {label && <label style={labelStyle}>{label}{required && ' *'}</label>}
      <input style={{ ...fieldBase, ...(rest.style || {}) }} {...rest} onFocus={(e) => { e.target.style.borderColor = 'var(--c-primary)'; rest.onFocus?.(e); }} onBlur={(e) => { e.target.style.borderColor = 'var(--c-border-light)'; rest.onBlur?.(e); }} />
      {hint && <p style={hintStyle}>{hint}</p>}
      {error && <p style={errorStyle}>{error}</p>}
    </div>
  );
}
export function Textarea({ label, required, hint, rows = 4, ...rest }: FieldProps & React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <div>
      {label && <label style={labelStyle}>{label}{required && ' *'}</label>}
      <textarea rows={rows} style={{ ...fieldBase, resize: 'vertical', fontFamily: 'inherit' }} {...rest} />
      {hint && <p style={hintStyle}>{hint}</p>}
    </div>
  );
}
export function Select({ label, required, options, ...rest }: FieldProps & React.SelectHTMLAttributes<HTMLSelectElement> & { options: { value: string; label: string }[] }) {
  return (
    <div>
      {label && <label style={labelStyle}>{label}{required && ' *'}</label>}
      <select style={fieldBase} {...rest}>
        {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  );
}

// ==================== Switch ====================
export function Switch({ checked, onChange, label }: { checked: boolean; onChange: (v: boolean) => void; label?: string }) {
  return (
    <label style={{ display: 'inline-flex', alignItems: 'center', gap: 10, cursor: 'pointer', userSelect: 'none' }}>
      <span onClick={() => onChange(!checked)} style={{
        width: 44, height: 24, borderRadius: 12, position: 'relative', transition: 'background 0.25s',
        background: checked ? 'linear-gradient(135deg, #00d4ff, #7b2ff7)' : 'rgba(255,255,255,0.15)',
      }}>
        <span style={{
          position: 'absolute', top: 2, left: checked ? 22 : 2, width: 20, height: 20, borderRadius: '50%',
          background: '#fff', transition: 'left 0.25s', boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
        }} />
      </span>
      {label && <span style={{ fontSize: 14, color: 'var(--c-text-sec)' }}>{label}</span>}
    </label>
  );
}

// ==================== Card ====================
export function Card({ children, style, hover }: { children: React.ReactNode; style?: React.CSSProperties; hover?: boolean }) {
  return (
    <div style={{
      background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16,
      padding: 24, backdropFilter: 'blur(20px)', transition: 'all 0.3s ease',
      ...(hover ? { cursor: 'pointer' } : {}),
      ...style,
    }}>
      {children}
    </div>
  );
}

// ==================== PageHeader ====================
export function PageHeader({ title, subtitle, actions }: { title: string; subtitle?: string; actions?: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, flexWrap: 'wrap', gap: 12 }}>
      <div>
        <h1 style={{ fontSize: 24, fontWeight: 700, margin: 0 }}>{title}</h1>
        {subtitle && <p style={{ fontSize: 13, color: 'var(--c-text-muted)', marginTop: 4 }}>{subtitle}</p>}
      </div>
      {actions && <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>{actions}</div>}
    </div>
  );
}

// ==================== EmptyState ====================
export function EmptyState({ title = '暂无数据', hint, action }: { title?: string; hint?: string; action?: React.ReactNode }) {
  return (
    <div style={{ textAlign: 'center', padding: '60px 24px', color: 'var(--c-text-muted)' }}>
      <div style={{ fontSize: 48, marginBottom: 12, opacity: 0.3 }}>📭</div>
      <p style={{ fontSize: 15, marginBottom: 4 }}>{title}</p>
      {hint && <p style={{ fontSize: 13, marginBottom: 16 }}>{hint}</p>}
      {action}
    </div>
  );
}

// ==================== Badge ====================
type BadgeTone = 'primary' | 'success' | 'warning' | 'danger' | 'neutral';
export function Badge({ tone = 'neutral', children }: { tone?: BadgeTone; children: React.ReactNode }) {
  const tones: Record<BadgeTone, React.CSSProperties> = {
    primary: { background: 'rgba(0,212,255,0.15)', color: '#00d4ff', border: '1px solid rgba(0,212,255,0.3)' },
    success: { background: 'rgba(0,255,128,0.12)', color: '#00ff80', border: '1px solid rgba(0,255,128,0.3)' },
    warning: { background: 'rgba(255,193,7,0.12)', color: '#ffc107', border: '1px solid rgba(255,193,7,0.3)' },
    danger: { background: 'rgba(255,107,107,0.12)', color: '#ff6b6b', border: '1px solid rgba(255,107,107,0.3)' },
    neutral: { background: 'rgba(255,255,255,0.06)', color: 'var(--c-text-sec)', border: '1px solid var(--c-border)' },
  };
  return <span style={{ display: 'inline-block', padding: '3px 10px', borderRadius: 999, fontSize: 12, ...tones[tone] }}>{children}</span>;
}

// ==================== Modal ====================
export function Modal({ open, onClose, title, children, footer, width = 600 }: {
  open: boolean; onClose: () => void; title: string; children: React.ReactNode; footer?: React.ReactNode; width?: number;
}) {
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div onClick={onClose} style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: 20,
    }}>
      <div onClick={(e) => e.stopPropagation()} style={{
        background: 'rgba(15,20,35,0.95)', backdropFilter: 'blur(24px)',
        border: '1px solid var(--c-border)', borderRadius: 18, padding: 32,
        width: '100%', maxWidth: width, maxHeight: '90vh', overflowY: 'auto',
        animation: 'modalIn 0.25s ease',
      }}>
        <style>{`@keyframes modalIn{from{opacity:0;transform:scale(0.95) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}`}</style>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ fontSize: 20, fontWeight: 700, margin: 0 }}>{title}</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--c-text-muted)', cursor: 'pointer', fontSize: 22, lineHeight: 1 }}>×</button>
        </div>
        <div>{children}</div>
        {footer && <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', marginTop: 24 }}>{footer}</div>}
      </div>
    </div>
  );
}

// ==================== ConfirmDialog ====================
export function ConfirmDialog({ open, title, message, onConfirm, onCancel, confirmText = '确定', danger }: {
  open: boolean; title: string; message: string; onConfirm: () => void; onCancel: () => void; confirmText?: string; danger?: boolean;
}) {
  return (
    <Modal open={open} onClose={onCancel} title={title} width={440}
      footer={<>
        <Button variant="secondary" onClick={onCancel}>取消</Button>
        <Button variant={danger ? 'danger' : 'primary'} onClick={onConfirm}>{confirmText}</Button>
      </>}>
      <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>{message}</p>
    </Modal>
  );
}

// ==================== Toast ====================
interface ToastItem { id: string; type: 'success' | 'error' | 'info'; message: string; }
const ToastContext = createContext<(type: ToastItem['type'], message: string) => void>(() => {});
export function useToast() {
  const fn = useContext(ToastContext);
  return {
    success: (m: string) => fn('success', m),
    error: (m: string) => fn('error', m),
    info: (m: string) => fn('info', m),
  };
}
export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const push = useCallback((type: ToastItem['type'], message: string) => {
    const id = `t_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
    setItems((prev) => [...prev, { id, type, message }]);
    setTimeout(() => setItems((prev) => prev.filter((t) => t.id !== id)), 3500);
  }, []);
  const colors: Record<ToastItem['type'], string> = {
    success: 'linear-gradient(135deg, #00ff80, #00d4ff)',
    error: 'linear-gradient(135deg, #ff6b6b, #ff8e53)',
    info: 'linear-gradient(135deg, #00d4ff, #7b2ff7)',
  };
  const icons: Record<ToastItem['type'], string> = { success: '✓', error: '✕', info: 'ℹ' };
  return (
    <ToastContext.Provider value={push}>
      {children}
      <div style={{ position: 'fixed', top: 24, right: 24, zIndex: 2000, display: 'flex', flexDirection: 'column', gap: 10 }}>
        {items.map((t) => (
          <div key={t.id} style={{
            display: 'flex', alignItems: 'center', gap: 10, padding: '12px 18px', borderRadius: 12,
            background: 'rgba(15,20,35,0.95)', backdropFilter: 'blur(20px)', border: '1px solid var(--c-border)',
            boxShadow: '0 10px 40px rgba(0,0,0,0.5)', fontSize: 14, minWidth: 240,
            animation: 'toastIn 0.3s ease',
          }}>
            <style>{`@keyframes toastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}`}</style>
            <span style={{
              width: 22, height: 22, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: colors[t.type], color: '#fff', fontSize: 13, fontWeight: 700, flexShrink: 0,
            }}>{icons[t.type]}</span>
            <span style={{ color: 'var(--c-text)' }}>{t.message}</span>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

// ==================== Table ====================
export function Table<T>({ columns, rows, rowKey, actions }: {
  columns: { key: keyof T | string; label: string; render?: (row: T) => React.ReactNode; width?: string }[];
  rows: T[];
  rowKey: (row: T) => string;
  actions?: (row: T) => React.ReactNode;
}) {
  return (
    <div style={{ overflowX: 'auto', borderRadius: 12, border: '1px solid var(--c-border)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
        <thead>
          <tr style={{ background: 'rgba(255,255,255,0.04)' }}>
            {columns.map((c) => <th key={String(c.key)} style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: 'var(--c-text-sec)', fontSize: 13, width: c.width }}>{c.label}</th>)}
            {actions && <th style={{ padding: '12px 16px', textAlign: 'right', fontWeight: 600, color: 'var(--c-text-sec)', fontSize: 13 }}>操作</th>}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr><td colSpan={columns.length + (actions ? 1 : 0)} style={{ padding: 40, textAlign: 'center', color: 'var(--c-text-muted)' }}>暂无数据</td></tr>
          )}
          {rows.map((row) => (
            <tr key={rowKey(row)} style={{ borderTop: '1px solid var(--c-border)', transition: 'background 0.2s' }}>
              {columns.map((c) => (
                <td key={String(c.key)} style={{ padding: '12px 16px', color: 'var(--c-text)' }}>
                  {c.render ? c.render(row) : String((row as any)[c.key] ?? '')}
                </td>
              ))}
              {actions && <td style={{ padding: '12px 16px', textAlign: 'right' }}>{actions(row)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ==================== Pagination ====================
export function Pagination({ page, pageSize, total, onChange }: { page: number; pageSize: number; total: number; onChange: (p: number) => void }) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  if (totalPages <= 1) return null;
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: 6, marginTop: 20 }}>
      <Button size="sm" variant="secondary" disabled={page <= 1} onClick={() => onChange(page - 1)}>上一页</Button>
      <span style={{ padding: '6px 12px', fontSize: 13, color: 'var(--c-text-sec)', display: 'inline-flex', alignItems: 'center' }}>
        {page} / {totalPages}
      </span>
      <Button size="sm" variant="secondary" disabled={page >= totalPages} onClick={() => onChange(page + 1)}>下一页</Button>
    </div>
  );
}

// ==================== SearchBar ====================
export function SearchBar({ value, onChange, placeholder = '搜索...' }: { value: string; onChange: (v: string) => void; placeholder?: string }) {
  return (
    <input
      value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder}
      style={{ ...fieldBase, width: 240, marginBottom: 0 }}
    />
  );
}

// ==================== Tabs ====================
export function Tabs({ tabs, active, onChange }: { tabs: { key: string; label: string }[]; active: string; onChange: (k: string) => void }) {
  return (
    <div style={{ display: 'flex', gap: 4, borderBottom: '1px solid var(--c-border)', marginBottom: 20, flexWrap: 'wrap' }}>
      {tabs.map((t) => {
        const isActive = t.key === active;
        return (
          <button key={t.key} onClick={() => onChange(t.key)} style={{
            padding: '10px 18px', background: 'transparent', border: 'none', cursor: 'pointer',
            color: isActive ? 'var(--c-primary)' : 'var(--c-text-sec)', fontSize: 14, fontWeight: isActive ? 600 : 400,
            borderBottom: isActive ? '2px solid var(--c-primary)' : '2px solid transparent',
            transition: 'all 0.2s', marginBottom: -1,
          }}>{t.label}</button>
        );
      })}
    </div>
  );
}

// ==================== StatCard ====================
export function StatCard({ label, value, icon, gradient, href }: {
  label: string; value: string | number; icon?: React.ReactNode; gradient?: string; href?: string;
}) {
  const style: React.CSSProperties = {
    background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24,
    position: 'relative', overflow: 'hidden', transition: 'all 0.3s ease', cursor: href ? 'pointer' : 'default',
  };
  const inner = (
    <>
      <div style={{
        position: 'absolute', top: -20, right: -20, width: 100, height: 100, borderRadius: '50%',
        background: gradient || 'linear-gradient(135deg, #00d4ff, #7b2ff7)', opacity: 0.15, filter: 'blur(20px)',
      }} />
      {icon && <div style={{ marginBottom: 10, opacity: 0.8 }}>{icon}</div>}
      <div style={{ fontSize: 36, fontWeight: 800, background: gradient || 'linear-gradient(135deg, #00d4ff, #7b2ff7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: 4 }}>{value}</div>
      <div style={{ color: 'var(--c-text-sec)', fontSize: 13 }}>{label}</div>
    </>
  );
  if (href) return <a href={href} style={style}>{inner}</a>;
  return <div style={style}>{inner}</div>;
}

// ==================== ActionBar ====================
export function ActionBar({ left, right }: { left?: React.ReactNode; right?: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, gap: 12, flexWrap: 'wrap' }}>
      <div>{left}</div>
      <div style={{ display: 'flex', gap: 8 }}>{right}</div>
    </div>
  );
}

// ==================== Row ====================
export function Row({ children, onClick, style }: { children: React.ReactNode; onClick?: () => void; style?: React.CSSProperties }) {
  return (
    <div onClick={onClick} style={{
      display: 'flex', alignItems: 'center', gap: 12, padding: '14px 18px', borderRadius: 12,
      background: 'rgba(255,255,255,0.03)', border: '1px solid var(--c-border)',
      transition: 'all 0.2s', cursor: onClick ? 'pointer' : 'default', ...style,
    }}>
      {children}
    </div>
  );
}

// ==================== FormField (re-export ImageUpload for forms) ====================
export function ImageField({ label = '图片', value, onChange }: { label?: string; value: string; onChange: (v: string) => void }) {
  return <ImageUpload label={label} value={value} onChange={onChange} />;
}

// ==================== styles ====================
const labelStyle: React.CSSProperties = {
  display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6,
};
const hintStyle: React.CSSProperties = {
  fontSize: 12, color: 'var(--c-text-muted)', marginTop: 6,
};
const errorStyle: React.CSSProperties = {
  fontSize: 12, color: '#ff6b6b', marginTop: 6,
};
