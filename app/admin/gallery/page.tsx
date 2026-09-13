'use client';

import { useState, useEffect } from 'react';
import type { GalleryItem } from '@/lib/types';
import {
  Button, PageHeader, Card, EmptyState, SearchBar, useToast, ConfirmDialog,
} from '@/components/AdminUI';
import ImageUpload from '@/components/ImageUpload';

export default function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState('');
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [uploadUrl, setUploadUrl] = useState('');
  const toast = useToast();

  const loadGallery = async () => {
    setLoading(true);
    const res = await fetch('/api/gallery');
    const data = await res.json();
    setItems(data.data || []);
    setLoading(false);
  };

  useEffect(() => { loadGallery(); }, []);

  const handleDelete = async () => {
    if (!deleteId) return;
    const res = await fetch(`/api/gallery?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    loadGallery();
  };

  const filtered = items.filter((g) => !keyword || g.name.toLowerCase().includes(keyword.toLowerCase()));

  return (
    <div>
      <PageHeader title="图片库" subtitle={`共 ${items.length} 张图片`} />

      <Card style={{ marginBottom: 16, padding: '14px 18px' }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <SearchBar value={keyword} onChange={setKeyword} placeholder="搜索文件名" />
          <div style={{ flex: 1 }} />
          <div style={{ width: 400, maxWidth: '100%' }}>
            <ImageUpload label="上传新图片" value={uploadUrl} onChange={(url) => { setUploadUrl(url); if (url) { toast.success('已上传'); loadGallery(); setUploadUrl(''); } }} />
          </div>
        </div>
      </Card>

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : filtered.length === 0 ? (
        <EmptyState title="图库为空" hint="上传第一张图片开始" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
          {filtered.map((g) => (
            <Card key={g.id} style={{ padding: 0, overflow: 'hidden' }}>
              <div style={{ position: 'relative', paddingTop: '75%', background: 'rgba(0,0,0,0.3)' }}>
                <img src={g.url} alt={g.name} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }} />
                <button onClick={() => setDeleteId(g.id)} style={{
                  position: 'absolute', top: 8, right: 8, width: 28, height: 28, borderRadius: '50%',
                  background: 'rgba(0,0,0,0.7)', color: '#ff6b6b', border: 'none', cursor: 'pointer', fontSize: 16,
                }} title="删除">×</button>
              </div>
              <div style={{ padding: '10px 12px' }}>
                <div style={{ fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{g.name}</div>
                <div style={{ fontSize: 11, color: 'var(--c-text-muted)', marginTop: 2 }}>
                  {g.type.split('/')[1]?.toUpperCase()} · {(g.size / 1024).toFixed(1)}KB · {new Date(g.createdAt).toLocaleDateString('zh-CN')}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <ConfirmDialog open={!!deleteId} title="确认删除" message="删除后不可恢复，确定删除这张图片吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
