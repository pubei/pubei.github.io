'use client';

import { useState, useEffect } from 'react';
import type { FAQItem } from '@/lib/types';
import {
  Button, PageHeader, Card, Badge, Modal, Input, Textarea, Switch, EmptyState, useToast, ConfirmDialog,
} from '@/components/AdminUI';

const CATEGORIES = ['通用', '价格', '工艺', '材料', '工期', '售后', '其他'];

export default function FAQsPage() {
  const [list, setList] = useState<FAQItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<FAQItem | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const toast = useToast();

  const fetchList = async () => {
    setLoading(true);
    const res = await fetch('/api/faqs');
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchList(); }, []);

  const openForm = (item?: FAQItem) => {
    setEditing(item || null);
    setForm(item ? { ...item } : { question: '', answer: '', category: '通用', order: 0, enabled: true });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/faqs', {
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
    const res = await fetch(`/api/faqs?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    fetchList();
  };

  return (
    <div>
      <PageHeader title="FAQ 管理" subtitle="管理常见问题解答"
        actions={<Button onClick={() => openForm()}>+ 新增 FAQ</Button>} />

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无 FAQ" hint="添加第一条常见问题" />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {list.map((f) => (
            <Card key={f.id} style={{ padding: '16px 20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 8 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
                    <Badge tone="primary">{f.category}</Badge>
                    <Badge tone={f.enabled ? 'success' : 'neutral'}>{f.enabled ? '显示' : '隐藏'}</Badge>
                  </div>
                  <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 6 }}>Q: {f.question}</h3>
                  <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>A: {f.answer}</p>
                </div>
                <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
                  <Button size="sm" variant="secondary" onClick={() => openForm(f)}>编辑</Button>
                  <Button size="sm" variant="danger" onClick={() => setDeleteId(f.id)}>删除</Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title={editing ? '编辑 FAQ' : '新增 FAQ'} width={600}
        footer={<><Button variant="secondary" onClick={() => setShowForm(false)}>取消</Button><Button onClick={handleSubmit}>{editing ? '保存' : '新增'}</Button></>}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <Input label="问题" value={form.question || ''} onChange={(e) => setForm({ ...form, question: e.target.value })} required />
          <Textarea label="答案" rows={5} value={form.answer || ''} onChange={(e) => setForm({ ...form, answer: e.target.value })} required />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>分类</label>
              <select value={form.category || '通用'} onChange={(e) => setForm({ ...form, category: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', fontSize: 14, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text)' }}>
                {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <Input label="排序" type="number" value={form.order || 0} onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>启用</label>
            <Switch checked={form.enabled !== false} onChange={(v) => setForm({ ...form, enabled: v })} />
          </div>
        </form>
      </Modal>

      <ConfirmDialog open={!!deleteId} title="确认删除" message="确定删除这条 FAQ 吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
