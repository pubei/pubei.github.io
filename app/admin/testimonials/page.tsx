'use client';

import { useState, useEffect } from 'react';
import type { Testimonial } from '@/lib/types';
import {
  Button, PageHeader, Card, Row, Badge, Modal, Input, Textarea, Switch, EmptyState, useToast, ConfirmDialog,
} from '@/components/AdminUI';
import ImageUpload from '@/components/ImageUpload';

export default function TestimonialsPage() {
  const [list, setList] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Testimonial | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const toast = useToast();

  const fetchList = async () => {
    setLoading(true);
    const res = await fetch('/api/testimonials');
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchList(); }, []);

  const openForm = (item?: Testimonial) => {
    setEditing(item || null);
    setForm(item ? { ...item } : {
      customer: '', project: '', rating: 5, content: '', avatar: '', order: 0, enabled: true,
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/testimonials', {
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
    const res = await fetch(`/api/testimonials?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    fetchList();
  };

  return (
    <div>
      <PageHeader title="客户评价" subtitle="管理客户口碑推荐"
        actions={<Button onClick={() => openForm()}>+ 新增评价</Button>} />

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无评价" hint="添加第一条客户评价" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 16 }}>
          {list.map((t) => (
            <Card key={t.id}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 }}>
                <div style={{ width: 48, height: 48, borderRadius: '50%', overflow: 'hidden', background: 'rgba(0,212,255,0.15)' }}>
                  {t.avatar && <img src={t.avatar} alt={t.customer} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600 }}>{t.customer}</div>
                  <div style={{ fontSize: 12, color: 'var(--c-text-muted)' }}>{t.project}</div>
                </div>
                <Badge tone={t.enabled ? 'success' : 'neutral'}>{t.enabled ? '显示' : '隐藏'}</Badge>
              </div>
              <div style={{ color: '#ffc107', fontSize: 14, marginBottom: 8 }}>
                {'★'.repeat(t.rating)}{'☆'.repeat(5 - t.rating)}
              </div>
              <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6, marginBottom: 12 }}>{t.content}</p>
              <div style={{ display: 'flex', gap: 8 }}>
                <Button size="sm" variant="secondary" onClick={() => openForm(t)}>编辑</Button>
                <Button size="sm" variant="danger" onClick={() => setDeleteId(t.id)}>删除</Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title={editing ? '编辑评价' : '新增评价'} width={600}
        footer={<><Button variant="secondary" onClick={() => setShowForm(false)}>取消</Button><Button onClick={handleSubmit}>{editing ? '保存' : '新增'}</Button></>}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="客户姓名" value={form.customer || ''} onChange={(e) => setForm({ ...form, customer: e.target.value })} required />
            <Input label="项目名称" value={form.project || ''} onChange={(e) => setForm({ ...form, project: e.target.value })} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>评分</label>
            <div style={{ display: 'flex', gap: 6 }}>
              {[1, 2, 3, 4, 5].map((r) => (
                <button key={r} type="button" onClick={() => setForm({ ...form, rating: r })} style={{
                  background: 'transparent', border: 'none', cursor: 'pointer', fontSize: 24,
                  color: r <= (form.rating || 5) ? '#ffc107' : 'rgba(255,255,255,0.2)',
                }}>★</button>
              ))}
            </div>
          </div>
          <Textarea label="评价内容" rows={4} value={form.content || ''} onChange={(e) => setForm({ ...form, content: e.target.value })} required />
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>客户头像</label>
            <ImageUpload value={form.avatar || ''} onChange={(url) => setForm({ ...form, avatar: url })} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="排序" type="number" value={form.order || 0} onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
            <div>
              <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6, marginTop: 10 }}>启用</label>
              <Switch checked={form.enabled !== false} onChange={(v) => setForm({ ...form, enabled: v })} />
            </div>
          </div>
        </form>
      </Modal>

      <ConfirmDialog open={!!deleteId} title="确认删除" message="确定删除这条客户评价吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
