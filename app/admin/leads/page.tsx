'use client';

import { useState, useEffect } from 'react';
import type { Lead, LeadStatus } from '@/lib/types';
import {
  Button, PageHeader, Card, Row, Badge, Modal, Input, Textarea, Select,
  SearchBar, EmptyState, useToast, ConfirmDialog,
} from '@/components/AdminUI';

const STATUS_LABEL: Record<LeadStatus, string> = {
  new: '新咨询', following: '跟进中', won: '已签单', lost: '已失单', archived: '已归档',
};
const STATUS_TONE: Record<LeadStatus, 'primary' | 'warning' | 'success' | 'danger' | 'neutral'> = {
  new: 'primary', following: 'warning', won: 'success', lost: 'danger', archived: 'neutral',
};
const SERVICE_OPTIONS = ['全屋定制', '新房装修', '旧房翻新', '局部改造', '软装配饰', '智能家居', '水电改造', '监理服务'];

export default function LeadsPage() {
  const [list, setList] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState('');
  const [filter, setFilter] = useState<LeadStatus | 'all'>('all');
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Lead | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const toast = useToast();

  const fetchLeads = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filter !== 'all') params.set('status', filter);
    if (keyword) params.set('q', keyword);
    const res = await fetch(`/api/leads?${params}`);
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchLeads(); }, [filter, keyword]);

  const openForm = (item?: Lead) => {
    setEditing(item || null);
    setForm(item ? { ...item } : {
      name: '', phone: '', email: '', service: '全屋定制', area: '', budget: '',
      appointmentTime: '', message: '', source: '手动录入', status: 'new', notes: [],
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/leads', {
      method: editing ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, id: editing?.id }),
    });
    const data = await res.json();
    if (data.success) {
      toast.success(editing ? '已更新客户咨询' : '已新增客户咨询');
      setShowForm(false);
      fetchLeads();
    } else {
      toast.error(data.error || '操作失败');
    }
  };

  const handleStatusChange = async (id: string, status: LeadStatus) => {
    await fetch('/api/leads', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, status }),
    });
    toast.success('状态已更新');
    fetchLeads();
  };

  const handleDelete = async () => {
    if (!deleteId) return;
    const res = await fetch(`/api/leads?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    fetchLeads();
  };

  return (
    <div>
      <PageHeader title="客户咨询" subtitle="管理所有客户咨询与预约线索"
        actions={<Button onClick={() => openForm()}>+ 新增咨询</Button>} />

      <Card style={{ marginBottom: 16, padding: '14px 18px' }}>
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          <SearchBar value={keyword} onChange={setKeyword} placeholder="搜索姓名 / 手机 / 服务" />
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {(['all', 'new', 'following', 'won', 'lost', 'archived'] as const).map((s) => (
              <button key={s} onClick={() => setFilter(s)} style={{
                padding: '6px 14px', borderRadius: 999, fontSize: 13, cursor: 'pointer',
                background: filter === s ? 'linear-gradient(135deg, #00d4ff, #7b2ff7)' : 'rgba(255,255,255,0.05)',
                color: filter === s ? '#fff' : 'var(--c-text-sec)',
                border: filter === s ? 'none' : '1px solid var(--c-border-light)',
                transition: 'all 0.2s',
              }}>{s === 'all' ? '全部' : STATUS_LABEL[s]}</button>
            ))}
          </div>
        </div>
      </Card>

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无客户咨询" hint="点击右上角新增咨询" />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {list.map((l) => (
            <Row key={l.id} style={{ flexWrap: 'wrap' }}>
              <div style={{ flex: 1, minWidth: 200 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                  <span style={{ fontWeight: 600, fontSize: 15 }}>{l.name}</span>
                  <Badge tone={STATUS_TONE[l.status]}>{STATUS_LABEL[l.status]}</Badge>
                </div>
                <div style={{ fontSize: 13, color: 'var(--c-text-muted)' }}>
                  📞 {l.phone} · 🛠 {l.service || '未填写'} · 🕐 {new Date(l.createdAt).toLocaleString('zh-CN')}
                </div>
                {l.message && <div style={{ fontSize: 13, color: 'var(--c-text-sec)', marginTop: 4, lineHeight: 1.5 }}>{l.message}</div>}
              </div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <select value={l.status} onChange={(e) => handleStatusChange(l.id, e.target.value as LeadStatus)} style={{
                  padding: '6px 10px', borderRadius: 6, fontSize: 12,
                  background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', color: 'var(--c-text)',
                }}>
                  {Object.entries(STATUS_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                </select>
                <Button size="sm" variant="secondary" onClick={() => openForm(l)}>详情</Button>
                <Button size="sm" variant="danger" onClick={() => setDeleteId(l.id)}>删除</Button>
              </div>
            </Row>
          ))}
        </div>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title={editing ? '编辑咨询' : '新增咨询'} width={640}
        footer={<>
          <Button variant="secondary" onClick={() => setShowForm(false)}>取消</Button>
          <Button onClick={handleSubmit}>{editing ? '保存' : '新增'}</Button>
        </>}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="客户姓名" value={form.name || ''} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <Input label="联系电话" value={form.phone || ''} onChange={(e) => setForm({ ...form, phone: e.target.value })} required />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="邮箱" value={form.email || ''} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <Select label="意向服务" value={form.service || ''} onChange={(e) => setForm({ ...form, service: e.target.value })}
              options={SERVICE_OPTIONS.map((s) => ({ value: s, label: s }))} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
            <Input label="面积" value={form.area || ''} onChange={(e) => setForm({ ...form, area: e.target.value })} />
            <Input label="预算" value={form.budget || ''} onChange={(e) => setForm({ ...form, budget: e.target.value })} />
            <Input label="期望时间" type="date" value={form.appointmentTime || ''} onChange={(e) => setForm({ ...form, appointmentTime: e.target.value })} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Select label="状态" value={form.status || 'new'} onChange={(e) => setForm({ ...form, status: e.target.value })}
              options={Object.entries(STATUS_LABEL).map(([k, v]) => ({ value: k, label: v }))} />
            <Input label="来源" value={form.source || ''} onChange={(e) => setForm({ ...form, source: e.target.value })} />
          </div>
          <Textarea label="需求/备注" rows={3} value={form.message || ''} onChange={(e) => setForm({ ...form, message: e.target.value })} />
        </form>
      </Modal>

      <ConfirmDialog open={!!deleteId} title="确认删除" message="删除后不可恢复，确定删除这条客户咨询吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
