import { getAllNews } from '@/lib/kv';
import Link from 'next/link';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function NewsListPage() {
  const allNews = await getAllNews();
  const published = allNews.filter((n) => n.published).sort((a, b) => b.createdAt - a.createdAt);

  return (
    <PublicLayout>
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, textAlign: 'center', marginBottom: 40 }}>公司新闻</h1>
      {published.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--c-text-muted)' }}>暂无新闻</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {published.map((n) => (
            <Link key={n.id} href={`/news/${n.id}`} style={{
              display: 'flex', gap: 20, padding: 20, borderRadius: 14,
              background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)',
              transition: 'all 0.3s',
            }}>
              {n.image && <img src={n.image} alt={n.title} style={{ width: 160, height: 100, objectFit: 'cover', borderRadius: 8 }} />}
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, color: 'var(--c-primary)', marginBottom: 6 }}>{n.category} · {n.date}</div>
                <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>{n.title}</h2>
                <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>{n.excerpt}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
    </PublicLayout>
  );
}
