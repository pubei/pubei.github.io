import { getStats, getAllNews } from '@/lib/kv';

export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  const stats = await getStats();
  const allNews = await getAllNews();
  const recentNews = allNews.sort((a, b) => b.createdAt - a.createdAt).slice(0, 5);

  const cards = [
    { label: '新闻总数', value: stats.totalNews, color: '#00d4ff', href: '/admin/news' },
    { label: '服务项目', value: stats.totalServices, color: '#7b2ff7', href: '/admin/services' },
    { label: '装修案例', value: stats.totalProjects, color: '#00ff80', href: '/admin/projects' },
  ];

  return (
    <div>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 24 }}>Dashboard</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 32 }}>
        {cards.map((c) => (
          <a key={c.label} href={c.href} style={{
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid var(--c-border)',
            borderRadius: 16, padding: 24,
            display: 'block', transition: 'all 0.3s',
          }}>
            <div style={{ fontSize: 36, fontWeight: 800, color: c.color, marginBottom: 8 }}>{c.value}</div>
            <div style={{ color: 'var(--c-text-sec)', fontSize: 14 }}>{c.label}</div>
          </a>
        ))}
      </div>

      <div style={{
        background: 'rgba(255,255,255,0.04)',
        border: '1px solid var(--c-border)',
        borderRadius: 16, padding: 24,
      }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>最新新闻</h2>
        {recentNews.length === 0 ? (
          <p style={{ color: 'var(--c-text-muted)' }}>暂无新闻</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {recentNews.map((n) => (
              <a key={n.id} href={`/admin/news`} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 16px', borderRadius: 10,
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid var(--c-border)',
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
