'use client';

import { useState, useEffect } from 'react';
import type { TeamMember } from '@/lib/types';
import {
  Button, PageHeader, Card, Badge, Modal, Input, Textarea, Switch, EmptyState, useToast, ConfirmDialog,
} from '@/components/AdminUI';
import ImageUpload from '@/components/ImageUpload';

export default function TeamPage() {
  const [list, setList] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<TeamMember | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const [skillInput, setSkillInput] = useState('');
  const toast = useToast();

  const fetchList = async () => {
    setLoading(true);
    const res = await fetch('/api/team');
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchList(); }, []);

  const openForm = (item?: TeamMember) => {
    setEditing(item || null);
    setForm(item ? { ...item, skills: item.skills || [] } : {
      name: '', role: '', avatar: '', bio: '', skills: [], order: 0, enabled: true,
    });
    setSkillInput('');
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/team', {
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
    const res = await fetch(`/api/team?id=${deleteId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已删除');
    else toast.error(data.error || '删除失败');
    setDeleteId(null);
    fetchList();
  };

  const addSkill = () => {
    const s = skillInput.trim();
    if (s && !form.skills.includes(s)) {
      setForm({ ...form, skills: [...form.skills, s] });
    }
    setSkillInput('');
  };

  return (
    <div>
      <PageHeader title="团队成员" subtitle="管理设计师与工程师团队展示"
        actions={<Button onClick={() => openForm()}>+ 新增成员</Button>} />

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无成员" hint="添加第一位团队成员" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
          {list.map((m) => (
            <Card key={m.id}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                <div style={{ width: 96, height: 96, borderRadius: '50%', overflow: 'hidden', marginBottom: 12, background: 'linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,47,247,0.2))' }}>
                  {m.avatar && <img src={m.avatar} alt={m.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
                </div>
                <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 2 }}>{m.name}</h3>
                <p style={{ fontSize: 13, color: 'var(--c-primary)', marginBottom: 8 }}>{m.role}</p>
                <Badge tone={m.enabled ? 'success' : 'neutral'}>{m.enabled ? '显示' : '隐藏'}</Badge>
                <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6, marginTop: 10, marginBottom: 10 }}>{m.bio}</p>
                {m.skills?.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, justifyContent: 'center', marginBottom: 12 }}>
                    {m.skills.map((s, i) => <Badge key={i} tone="primary">{s}</Badge>)}
                  </div>
                )}
                <div style={{ display: 'flex', gap: 8 }}>
                  <Button size="sm" variant="secondary" onClick={() => openForm(m)}>编辑</Button>
                  <Button size="sm" variant="danger" onClick={() => setDeleteId(m.id)}>删除</Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title={editing ? '编辑成员' : '新增成员'} width={600}
        footer={<><Button variant="secondary" onClick={() => setShowForm(false)}>取消</Button><Button onClick={handleSubmit}>{editing ? '保存' : '新增'}</Button></>}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <Input label="姓名" value={form.name || ''} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <Input label="职位" value={form.role || ''} onChange={(e) => setForm({ ...form, role: e.target.value })} placeholder="如：首席设计师" />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>头像</label>
            <ImageUpload value={form.avatar || ''} onChange={(url) => setForm({ ...form, avatar: url })} />
          </div>
          <Textarea label="个人简介" rows={3} value={form.bio || ''} onChange={(e) => setForm({ ...form, bio: e.target.value })} />
          <div>
            <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>技能标签</label>
            <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
              <input value={skillInput} onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSkill(); } }}
                placeholder="输入技能后回车"
                style={{ flex: 1, padding: '10px 14px', fontSize: 14, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 8, color: 'var(--c-text)' }} />
              <Button size="sm" variant="secondary" type="button" onClick={addSkill}>添加</Button>
            </div>
            {form.skills?.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {form.skills.map((s: string, i: number) => (
                  <span key={i} onClick={() => setForm({ ...form, skills: form.skills.filter((_: string, idx: number) => idx !== i) })} style={{
                    padding: '4px 10px', borderRadius: 999, fontSize: 12, cursor: 'pointer',
                    background: 'rgba(0,212,255,0.15)', color: '#00d4ff', border: '1px solid rgba(0,212,255,0.3)',
                  }}>{s} ×</span>
                ))}
              </div>
            )}
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

      <ConfirmDialog open={!!deleteId} title="确认删除" message="确定删除这位团队成员吗？"
        onConfirm={handleDelete} onCancel={() => setDeleteId(null)} danger />
    </div>
  );
}
