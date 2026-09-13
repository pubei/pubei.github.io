'use client';

import { useState, useEffect } from 'react';
import type { AuditLog } from '@/lib/types';
import {
  PageHeader, Card, Badge, EmptyState, Button, useToast, ConfirmDialog,
} from '@/components/AdminUI';

const ACTION_TONE: Record<string, 'primary' | 'success' | 'warning' | 'danger' | 'neutral'> = {
  create: 'success', update: 'primary', delete: 'danger',
  login: 'primary', logout: 'neutral', export: 'warning', import: 'warning', reset: 'danger',
};

export default function AuditPage() {
  const [list, setList] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterModule, setFilterModule] = useState('all');
  const [filterAction, setFilterAction] = useState('all');
  const [showClear, setShowClear] = useState(false);
  const toast = useToast();

  const fetchList = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterModule !== 'all') params.set('module', filterModule);
    if (filterAction !== 'all') params.set('action', filterAction);
    params.set('limit', '200');
    const res = await fetch(`/api/audit?${params}`);
    const data = await res.json();
    setList(data.data || []);
    setLoading(false);
  };

  useEffect(() => { fetchList(); }, [filterModule, filterAction]);

  const handleClear = async () => {
    const res = await fetch('/api/audit', { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      toast.success('日志已清空');
      fetchList();
    } else toast.error(data.error || '操作失败');
    setShowClear(false);
  };

  const modules = ['all', 'news', 'service', 'project', 'lead', 'gallery', 'settings', 'banner', 'testimonial', 'faq', 'team', 'auth', 'backup'];
  const actions = ['all', 'create', 'update', 'delete', 'login', 'logout', 'export', 'import', 'reset'];

  return (
    <div>
      <PageHeader title="活动日志" subtitle={`共 ${list.length} 条记录`}
        actions={<Button variant="danger" onClick={() => setShowClear(true)}>清空日志</Button>} />

      <Card style={{ marginBottom: 16, padding: '14px 18px' }}>
        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
          <div>
            <label style={{ fontSize: 12, color: 'var(--c-text-muted)', marginRight: 8 }}>模块</label>
            <select value={filterModule} onChange={(e) => setFilterModule(e.target.value)} style={{ padding: '6px 10px', background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 6, color: 'var(--c-text)', fontSize: 13 }}>
              {modules.map((m) => <option key={m} value={m}>{m === 'all' ? '全部' : m}</option>)}
            </select>
          </div>
          <div>
            <label style={{ fontSize: 12, color: 'var(--c-text-muted)', marginRight: 8 }}>操作</label>
            <select value={filterAction} onChange={(e) => setFilterAction(e.target.value)} style={{ padding: '6px 10px', background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border-light)', borderRadius: 6, color: 'var(--c-text)', fontSize: 13 }}>
              {actions.map((a) => <option key={a} value={a}>{a === 'all' ? '全部' : a}</option>)}
            </select>
          </div>
        </div>
      </Card>

      {loading ? (
        <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>
      ) : list.length === 0 ? (
        <EmptyState title="暂无活动日志" hint="执行任何写操作后会在此记录" />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {list.map((log) => (
            <Card key={log.id} style={{ padding: '12px 18px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                <Badge tone={ACTION_TONE[log.action] || 'neutral'}>{log.action}</Badge>
                <span style={{ fontSize: 13, color: 'var(--c-text-sec)' }}>模块: <strong style={{ color: 'var(--c-text)' }}>{log.module}</strong></span>
                <span style={{ fontSize: 13, color: 'var(--c-text-sec)' }}>对象: <span style={{ color: 'var(--c-text)' }}>{log.target}</span></span>
                {log.detail && <span style={{ fontSize: 13, color: 'var(--c-text-muted)' }}>· {log.detail}</span>}
                <div style={{ flex: 1 }} />
                <span style={{ fontSize: 12, color: 'var(--c-text-muted)' }}>{new Date(log.at).toLocaleString('zh-CN')}</span>
              </div>
            </Card>
          ))}
        </div>
      )}

      <ConfirmDialog open={showClear} title="确认清空" message="将永久删除所有活动日志，确定继续吗？"
        onConfirm={handleClear} onCancel={() => setShowClear(false)} danger confirmText="清空" />
    </div>
  );
}
