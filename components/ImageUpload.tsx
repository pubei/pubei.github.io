'use client';

import { useState, useRef } from 'react';

interface ImageUploadProps {
  value: string;
  onChange: (url: string) => void;
  label?: string;
  placeholder?: string;
}

export default function ImageUpload({ value, onChange, label = '图片', placeholder = '粘贴图片 URL 或点击上传' }: ImageUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      if (data.success) {
        onChange(data.url);
      } else {
        setError(data.error || '上传失败');
      }
    } catch (err: any) {
      setError('网络错误: ' + (err.message || String(err)));
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handlePaste = async (e: React.ClipboardEvent<HTMLInputElement>) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      if (item.type.startsWith('image/')) {
        const file = item.getAsFile();
        if (file) {
          setUploading(true);
          setError('');
          try {
            const formData = new FormData();
            formData.append('file', file);
            const res = await fetch('/api/upload', { method: 'POST', body: formData });
            const data = await res.json();
            if (data.success) {
              onChange(data.url);
            } else {
              setError(data.error || '上传失败');
            }
          } catch (err: any) {
            setError('网络错误: ' + (err.message || String(err)));
          } finally {
            setUploading(false);
          }
          break;
        }
      }
    }
  };

  return (
    <div>
      <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>
        {label}
      </label>

      {/* 预览 */}
      {value && (
        <div style={{ position: 'relative', marginBottom: 10, borderRadius: 8, overflow: 'hidden', border: '1px solid var(--c-border-light)' }}>
          <img src={value} alt="预览" style={{ width: '100%', maxHeight: 200, objectFit: 'cover', display: 'block' }} />
          <button
            type="button"
            onClick={() => onChange('')}
            style={{
              position: 'absolute', top: 8, right: 8,
              width: 28, height: 28, borderRadius: '50%',
              background: 'rgba(0,0,0,0.7)', color: 'white',
              border: 'none', cursor: 'pointer', fontSize: 16, lineHeight: 1,
            }}
            title="移除图片"
          >
            ×
          </button>
        </div>
      )}

      {/* URL 输入 + 上传按钮 */}
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={value}
          placeholder={placeholder}
          onChange={(e) => onChange(e.target.value)}
          onPaste={handlePaste}
          style={{
            flex: 1, padding: '10px 14px', fontSize: 14,
            background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)',
            borderRadius: 8, color: 'var(--c-text)', outline: 'none',
          }}
        />
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          style={{
            padding: '10px 16px', fontSize: 14, cursor: uploading ? 'not-allowed' : 'pointer',
            background: uploading ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #00d4ff, #7b2ff7)',
            border: 'none', borderRadius: 8, color: 'white', fontWeight: 600, whiteSpace: 'nowrap',
          }}
        >
          {uploading ? '上传中...' : '📷 上传'}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      {error && <p style={{ color: '#ff6b6b', fontSize: 12, marginTop: 6 }}>{error}</p>}
      <p style={{ color: 'var(--c-text-muted)', fontSize: 11, marginTop: 6 }}>
        支持 JPG / PNG / WebP / GIF / SVG，最大 4MB。也可直接粘贴图片或 URL。
      </p>
    </div>
  );
}
