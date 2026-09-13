'use client';

import { useState, useEffect } from 'react';
import type { Banner } from '@/lib/types';
import {
  Button, PageHeader, Card, Row, Badge, Modal, Input, Textarea, Switch, EmptyState, useToast, ConfirmDialog,
} from '@/components/AdminUI';
import ImageUpload from '@/components/ImageUpload';

export default function BannersPage() {
  const [list, setList] = useState<Banner[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Banner | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const toast = useToast();

  const fetchList = async () => {
    setLoading(true);
    const res = await fetch('/api/banners');
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchList(); }, []);

  const openForm = (item?: Banner) => {
    setEditing(item || null);
    setForm(item ? { ...item } : {
      title: '', subtitle: '', image: '', link: '', ctaText: '立即咨询', order: 0, enabled: true,
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/banners', {
      method: editing ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, id: editing?.id }),
    });
    const data = await res.json();
    if (data.success) {
      toast.success(editing ? '已保存' : '已新增');
      setShowForm(false);
      fetchList();
    } else toast.error(data.error || '操作失败');
  };

  const handleDelete = async () => {
    if (!deleteId) return;
    const res = await fetch(`/api/banners?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    fetchList();
  };

  const toggle = async (b: Banner) => {
    await fetch('/api/banners', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: b.id, enabled: !b.enabled }),
    });
    fetchList();
  };

  return (
    <div>
      <PageHeader title="首页 Banner" subtitle="管理首页焦点图轮播"
        actions={<Button onClick={() => openForm()}>+ 新增 Banner</Button>} />

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无 Banner" hint="新增第一张焦点图" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 16 }}>
          {list.map((b) => (
            <Card key={b.id} style={{ padding: 0, overflow: 'hidden' }}>
              <div style={{ position: 'relative', paddingTop: '40%' }}>
                {b.image ? (
                  <img src={b.image} alt={b.title} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }} />
                ) : (
                  <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--c-text-muted)', background: 'rgba(0,0,0,0.3)' }}>无图片</div>
                )}
                <div style={{ position: 'absolute', top: 8, left: 8 }}>
                  <Badge tone={b.enabled ? 'success' : 'neutral'}>{b.enabled ? '启用' : '禁用'}</Badge>
                </div>
              </div>
              <div style={{ padding: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{b.title}</h3>
                <p style={{ fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 8, lineHeight: 1.5 }}>{b.subtitle}</p>
                <div style={{ fontSize: 12, color: 'var(--c-text-muted)', marginBottom: 12 }}>排序: {b.order} · 按钮: {b.ctaText}</div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <Button size="sm" variant="secondary" onClick={() => openForm(b)}>编辑</Button>
                  <Button size="sm" variant="ghost" onClick={() => toggle(b)}>{b.enabled ? '禁用' : '启用'}</Button>
                  <Button size="sm" variant="danger" onClick={() => setDeleteId(b.id)}>删除</Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title={editing ? '编辑 Banner' : '新增 Banner'} width={640}
        footer={<><Button variant="secondary" onClick={() => setShowForm(false)}>取消</Button><Button onClick={handleSubmit}>{editing ? '保存' : '新增'}</Button></>}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <Input label="标题" value={form.title || ''} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <Textarea label="副标题" rows={2} value={form.subtitle || ''} onChange={(e) => setForm({ ...form, subtitle: e.target.value })} />
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>背景图</label>
            <ImageUpload value={form.image || ''} onChange={(url) => setForm({ ...form, image: url })} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="链接 URL" value={form.link || ''} onChange={(e) => setForm({ ...form, link: e.target.value })} placeholder="/services" />
            <Input label="按钮文字" value={form.ctaText || ''} onChange={(e) => setForm({ ...form, ctaText: e.target.value })} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="排序 (越小越前)" type="number" value={form.order || 0} onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
            <div>
              <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6, marginTop: 10 }}>启用</label>
              <Switch checked={form.enabled !== false} onChange={(v) => setForm({ ...form, enabled: v })} />
            </div>
          </div>
        </form>
      </Modal>

      <ConfirmDialog open={!!deleteId} title="确认删除" message="删除后不可恢复，确定删除这个 Banner 吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
