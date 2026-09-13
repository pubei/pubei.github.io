'use client';

import { useState } from 'react';
import {
  PageHeader, Card, Button, useToast, ConfirmDialog, EmptyState,
} from '@/components/AdminUI';

export default function BackupPage() {
  const [exporting, setExporting] = useState(false);
  const [importing, setImporting] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [showReset, setShowReset] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const toast = useToast();

  const handleExport = async () => {
    setExporting(true);
    try {
      const res = await fetch('/api/backup');
      const data = await res.json();
      if (data.success) {
        const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pubei-backup-${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
        toast.success('已导出备份');
      } else toast.error(data.error || '导出失败');
    } catch (e: any) {
      toast.error('导出失败: ' + e.message);
    }
    setExporting(false);
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImporting(true);
    try {
      const text = await file.text();
      const backup = JSON.parse(text);
      setPreview(JSON.stringify(backup, null, 2).slice(0, 500) + (JSON.stringify(backup).length > 500 ? '\n...' : ''));
      const res = await fetch('/api/backup', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(backup),
      });
      const data = await res.json();
      if (data.success) toast.success('已恢复备份');
      else toast.error(data.error || '恢复失败');
    } catch (e: any) {
      toast.error('文件解析失败: ' + e.message);
    }
    setImporting(false);
    e.target.value = '';
  };

  const handleReset = async () => {
    setResetting(true);
    const res = await fetch('/api/backup', { method: 'DELETE' });
    const data = await res.json();
    if (data.success) toast.success('已重置数据');
    else toast.error(data.error || '重置失败');
    setResetting(false);
    setShowReset(false);
  };

  return (
    <div>
      <PageHeader title="数据备份" subtitle="导出、恢复和重置系统数据" />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 16 }}>
        <Card>
          <div style={{ fontSize: 40, marginBottom: 12 }}>📤</div>
          <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8 }}>导出备份</h3>
          <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6, marginBottom: 16 }}>
            将所有业务数据（新闻、服务、案例、咨询、图库、设置、Banner、评价、FAQ、团队、日志）打包为 JSON 文件下载到本地。
          </p>
          <Button block loading={exporting} onClick={handleExport}>导出全量备份</Button>
        </Card>

        <Card>
          <div style={{ fontSize: 40, marginBottom: 12 }}>📥</div>
          <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8 }}>恢复备份</h3>
          <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6, marginBottom: 16 }}>
            上传之前导出的 JSON 备份文件，将数据恢复到系统中。<strong style={{ color: '#ff6b6b' }}>会覆盖现有同名数据</strong>。
          </p>
          <label style={{ display: 'block' }}>
            <input type="file" accept="application/json" onChange={handleImport} style={{ display: 'none' }} />
            <Button block loading={importing} variant="secondary" onClick={(e: any) => e.currentTarget.parentElement.querySelector('input').click()}>选择备份文件</Button>
          </label>
          {preview && (
            <pre style={{ marginTop: 12, padding: 12, background: 'rgba(0,0,0,0.3)', borderRadius: 8, fontSize: 12, color: 'var(--c-text-sec)', overflow: 'auto', maxHeight: 200 }}>{preview}</pre>
          )}
        </Card>

        <Card>
          <div style={{ fontSize: 40, marginBottom: 12 }}>⚠️</div>
          <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8, color: '#ff6b6b' }}>重置数据</h3>
          <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6, marginBottom: 16 }}>
            清空所有业务数据（保留联系信息、关于信息、站点设置）。此操作<strong style={{ color: '#ff6b6b' }}>不可恢复</strong>，请务必先导出备份。
          </p>
          <Button block variant="danger" onClick={() => setShowReset(true)}>重置全部数据</Button>
        </Card>
      </div>

      <ConfirmDialog open={showReset} title="危险操作" message="将清空所有业务数据且不可恢复，请确认已导出备份。是否继续？"
        onConfirm={handleReset} onCancel={() => setShowReset(false)} danger confirmText="确认重置" />
    </div>
  );
}
