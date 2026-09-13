'use client';

import { useState, useEffect } from 'react';
import type { SiteSettings } from '@/lib/types';
import {
  Button, PageHeader, Card, Input, Textarea, Switch, useToast,
} from '@/components/AdminUI';
import ImageUpload from '@/components/ImageUpload';

export default function SettingsPage() {
  const [settings, setSettings] = useState<SiteSettings | null>(null);
  const [saving, setSaving] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetch('/api/settings').then((r) => r.json()).then((d) => d.success && setSettings(d.data));
  }, []);

  const handleSave = async () => {
    if (!settings) return;
    setSaving(true);
    const res = await fetch('/api/settings', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    const data = await res.json();
    if (data.success) toast.success('设置已保存');
    else toast.error(data.error || '保存失败');
    setSaving(false);
  };

  if (!settings) return <p style={{ color: 'var(--c-text-muted)' }}>加载中...</p>;

  return (
    <div>
      <PageHeader title="站点设置" subtitle="SEO 元数据、社交链接、公告等全局配置"
        actions={<Button onClick={handleSave} loading={saving}>保存设置</Button>} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 16 }}>
        <Card>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 16 }}>SEO 元数据</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <Input label="页面标题 (meta title)" value={settings.metaTitle} onChange={(e) => setSettings({ ...settings, metaTitle: e.target.value })} />
            <Textarea label="页面描述 (meta description)" rows={3} value={settings.metaDescription} onChange={(e) => setSettings({ ...settings, metaDescription: e.target.value })} />
            <Input label="关键词 (keywords)" value={settings.metaKeywords} onChange={(e) => setSettings({ ...settings, metaKeywords: e.target.value })} hint="多个关键词用英文逗号分隔" />
            <div>
              <label style={{ display: 'block', fontSize: 13, color: 'var(--c-text-sec)', marginBottom: 6 }}>OG 分享图</label>
              <ImageUpload value={settings.ogImage} onChange={(url) => setSettings({ ...settings, ogImage: url })} />
            </div>
          </div>
        </Card>

        <Card>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 16 }}>站点信息</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <Input label="Favicon 路径" value={settings.favicon} onChange={(e) => setSettings({ ...settings, favicon: e.target.value })} />
            <Input label="备案号 (ICP)" value={settings.icp} onChange={(e) => setSettings({ ...settings, icp: e.target.value })} placeholder="如：桂ICP备20XXXXXX号" />
            <Textarea label="统计代码" rows={4} value={settings.analyticsCode} onChange={(e) => setSettings({ ...settings, analyticsCode: e.target.value })} hint="百度统计、Google Analytics 等" />
          </div>
        </Card>

        <Card>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 16 }}>顶部公告</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <Switch checked={settings.announcementEnabled} onChange={(v) => setSettings({ ...settings, announcementEnabled: v })} label="启用公告条" />
            <Textarea label="公告内容" rows={3} value={settings.announcement} onChange={(e) => setSettings({ ...settings, announcement: e.target.value })} />
          </div>
        </Card>

        <Card>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 16 }}>社交链接</h3>
          {settings.social.map((s, i) => (
            <div key={i} style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr auto', gap: 8, marginBottom: 10 }}>
              <Input value={s.label} onChange={(e) => {
                const social = [...settings.social]; social[i] = { ...social[i], label: e.target.value };
                setSettings({ ...settings, social });
              }} placeholder="名称" />
              <Input value={s.url} onChange={(e) => {
                const social = [...settings.social]; social[i] = { ...social[i], url: e.target.value };
                setSettings({ ...settings, social });
              }} placeholder="链接" />
              <Input value={s.icon} onChange={(e) => {
                const social = [...settings.social]; social[i] = { ...social[i], icon: e.target.value };
                setSettings({ ...settings, social });
              }} placeholder="图标" />
              <Button size="sm" variant="danger" onClick={() => setSettings({ ...settings, social: settings.social.filter((_, idx) => idx !== i) })}>×</Button>
            </div>
          ))}
          <Button size="sm" variant="secondary" onClick={() => setSettings({ ...settings, social: [...settings.social, { label: '', url: '', icon: '' }] })}>+ 添加链接</Button>
        </Card>
      </div>
    </div>
  );
}
