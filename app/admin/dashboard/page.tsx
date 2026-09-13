import { getStats, getAllNews, getAllLeads, getAuditLogs, getKVStatus } from '@/lib/kv';

export const dynamic = 'force-dynamic';

const icons = {
  news: '📰', services: '🛠', projects: '🏗', leads: '💬', gallery: '🖼', testimonials: '⭐',
};

const gradients = {
  news: 'linear-gradient(135deg, #00d4ff, #0066ff)',
  services: 'linear-gradient(135deg, #7b2ff7, #b06ab3)',
  projects: 'linear-gradient(135deg, #00ff80, #00d4ff)',
  leads: 'linear-gradient(135deg, #ff8e53, #ff6b6b)',
  gallery: 'linear-gradient(135deg, #ffc107, #ff9800)',
  testimonials: 'linear-gradient(135deg, #e91e63, #7b2ff7)',
};

const STATUS_LABEL: Record<string, string> = {
  new: '新咨询', following: '跟进中', won: '已签单', lost: '已失单', archived: '已归档',
};

export default async function DashboardPage() {
  const [stats, allNews, allLeads, auditLogs, kvStatus] = await Promise.all([
    getStats(),
    getAllNews(),
    getAllLeads(),
    getAuditLogs(8),
    getKVStatus(),
  ]);
  const recentNews = allNews.sort((a, b) => b.createdAt - a.createdAt).slice(0, 5);
  const recentLeads = allLeads.sort((a, b) => b.createdAt - a.createdAt).slice(0, 5);

  const cards = [
    { label: '新闻总数', value: stats.totalNews, sub: `${stats.publishedNews} 已发布`, href: '/admin/news', key: 'news' as const },
    { label: '服务项目', value: stats.totalServices, sub: '个服务', href: '/admin/services', key: 'services' as const },
    { label: '装修案例', value: stats.totalProjects, sub: '个案例', href: '/admin/projects', key: 'projects' as const },
    { label: '客户咨询', value: stats.totalLeads, sub: `${stats.newLeads} 条新咨询`, href: '/admin/leads', key: 'leads' as const },
    { label: '图片库', value: stats.totalGallery, sub: '张图片', href: '/admin/gallery', key: 'gallery' as const },
    { label: '客户评价', value: stats.totalTestimonials, sub: '条评价', href: '/admin/testimonials', key: 'testimonials' as const },
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 28, fontWeight: 800, margin: 0, background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Dashboard
        </h1>
        <p style={{ color: 'var(--c-text-muted)', fontSize: 14, marginTop: 4 }}>
          欢迎回来，{new Date().toLocaleDateString('zh-CN', { weekday: 'long', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* 顶部统计卡 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16, marginBottom: 32 }}>
        {cards.map((c) => (
          <a key={c.key} href={c.href} style={{
            background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16,
            padding: 24, position: 'relative', overflow: 'hidden', transition: 'all 0.3s ease',
            display: 'block', textDecoration: 'none', color: 'inherit',
          }}>
            <div style={{
              position: 'absolute', top: -20, right: -20, width: 100, height: 100, borderRadius: '50%',
              background: gradients[c.key], opacity: 0.15, filter: 'blur(20px)',
            }} />
            <div style={{ fontSize: 32, marginBottom: 8, opacity: 0.85 }}>{icons[c.key]}</div>
            <div style={{
              fontSize: 36, fontWeight: 800, marginBottom: 4,
              background: gradients[c.key], WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            }}>{c.value}</div>
            <div style={{ color: 'var(--c-text-sec)', fontSize: 13 }}>{c.label}</div>
            <div style={{ color: 'var(--c-text-muted)', fontSize: 11, marginTop: 4 }}>{c.sub}</div>
          </a>
        ))}
      </div>

      {/* 中部：最近 leads + 最近审计 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 16, marginBottom: 24 }}>
        <div style={{
          background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600, margin: 0 }}>💬 最近咨询</h2>
            <a href="/admin/leads" style={{ fontSize: 13, color: 'var(--c-primary)' }}>全部 →</a>
          </div>
          {recentLeads.length === 0 ? (
            <p style={{ color: 'var(--c-text-muted)', fontSize: 14 }}>暂无咨询</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {recentLeads.map((l) => (
                <a key={l.id} href="/admin/leads" style={{
                  display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px', borderRadius: 10,
                  background: 'rgba(255,255,255,0.02)', border: '1px solid var(--c-border)',
                  textDecoration: 'none', color: 'inherit',
                }}>
                  <span style={{ fontWeight: 500, fontSize: 14, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{l.name}</span>
                  <span style={{ fontSize: 12, color: 'var(--c-text-muted)' }}>{l.service || '未填写'}</span>
                  <span style={{
                    padding: '2px 8px', borderRadius: 999, fontSize: 11,
                    background: l.status === 'new' ? 'rgba(0,212,255,0.15)' : l.status === 'won' ? 'rgba(0,255,128,0.12)' : 'rgba(255,255,255,0.06)',
                    color: l.status === 'new' ? '#00d4ff' : l.status === 'won' ? '#00ff80' : 'var(--c-text-sec)',
                  }}>{STATUS_LABEL[l.status] || l.status}</span>
                </a>
              ))}
            </div>
          )}
        </div>

        <div style={{
          background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600, margin: 0 }}>📋 最近活动</h2>
            <a href="/admin/audit" style={{ fontSize: 13, color: 'var(--c-primary)' }}>全部 →</a>
          </div>
          {auditLogs.length === 0 ? (
            <p style={{ color: 'var(--c-text-muted)', fontSize: 14 }}>暂无活动</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {auditLogs.map((log) => (
                <div key={log.id} style={{
                  display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 10,
                  background: 'rgba(255,255,255,0.02)', border: '1px solid var(--c-border)',
                }}>
                  <span style={{
                    padding: '2px 8px', borderRadius: 999, fontSize: 11,
                    background: log.action === 'create' ? 'rgba(0,255,128,0.12)'
                      : log.action === 'delete' ? 'rgba(255,107,107,0.12)'
                      : log.action === 'update' ? 'rgba(0,212,255,0.12)'
                      : 'rgba(255,255,255,0.06)',
                    color: log.action === 'create' ? '#00ff80'
                      : log.action === 'delete' ? '#ff6b6b'
                      : log.action === 'update' ? '#00d4ff'
                      : 'var(--c-text-sec)',
                  }}>{log.action}</span>
                  <span style={{ fontSize: 13, color: 'var(--c-text-sec)' }}>{log.module}</span>
                  <span style={{ fontSize: 12, color: 'var(--c-text-muted)', marginLeft: 'auto' }}>
                    {new Date(log.at).toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit', month: 'numeric', day: 'numeric' })}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 底部：系统状态 + 快捷操作 */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div style={{
          background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24,
        }}>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>⚙️ 系统状态</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
              <span style={{ color: 'var(--c-text-sec)' }}>数据库</span>
              <span style={{ color: kvStatus.connected ? '#00ff80' : '#ff6b6b' }}>
                {kvStatus.connected ? '✓' : '✕'} {kvStatus.mode === 'kv' ? 'Vercel KV 已连接' : '内存模式'}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
              <span style={{ color: 'var(--c-text-sec)' }}>内容总数</span>
              <span style={{ color: 'var(--c-text)' }}>
                {stats.totalNews + stats.totalServices + stats.totalProjects + stats.totalFAQs + stats.totalTeam + stats.totalTestimonials + stats.totalBanners} 条
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
              <span style={{ color: 'var(--c-text-sec)' }}>图片库</span>
              <span style={{ color: 'var(--c-text)' }}>{stats.totalGallery} 张</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
              <span style={{ color: 'var(--c-text-sec)' }}>服务器时间</span>
              <span style={{ color: 'var(--c-text)' }}>{new Date().toLocaleString('zh-CN')}</span>
            </div>
          </div>
        </div>

        <div style={{
          background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24,
        }}>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>⚡ 快捷操作</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <a href="/admin/news" style={quickBtn}>📰 发布新闻</a>
            <a href="/admin/leads" style={quickBtn}>💬 新增咨询</a>
            <a href="/admin/banners" style={quickBtn}>🖼 添加 Banner</a>
            <a href="/admin/team" style={quickBtn}>👥 添加成员</a>
            <a href="/admin/settings" style={quickBtn}>⚙️ 站点设置</a>
            <a href="/admin/backup" style={quickBtn}>💾 导出备份</a>
          </div>
        </div>
      </div>

      {/* 最新新闻 */}
      <div style={{
        background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', borderRadius: 16, padding: 24, marginTop: 24,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600, margin: 0 }}>📰 最新新闻</h2>
          <a href="/admin/news" style={{ fontSize: 13, color: 'var(--c-primary)' }}>管理 →</a>
        </div>
        {recentNews.length === 0 ? (
          <p style={{ color: 'var(--c-text-muted)' }}>暂无新闻</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {recentNews.map((n) => (
              <a key={n.id} href="/admin/news" style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 16px', borderRadius: 10, textDecoration: 'none', color: 'inherit',
                background: 'rgba(255,255,255,0.02)', border: '1px solid var(--c-border)',
              }}>
                <span style={{ fontSize: 14, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{n.title}</span>
                <span style={{ fontSize: 12, color: 'var(--c-text-muted)', marginLeft: 16 }}>{n.date}</span>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const quickBtn: React.CSSProperties = {
  padding: '12px 14px', borderRadius: 10, fontSize: 13, fontWeight: 500,
  background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)',
  color: 'var(--c-text)', textAlign: 'center', textDecoration: 'none',
  transition: 'all 0.2s',
};
