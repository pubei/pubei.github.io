import { getNewsById } from '@/lib/kv';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function NewsDetailPage({ params }: { params: { id: string } }) {
  const news = await getNewsById(params.id);
  if (!news) notFound();

  return (
    <PublicLayout>
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '60px 24px' }}>
      <Link href="/news" style={{ color: 'var(--c-primary)', fontSize: 14 }}>← 返回新闻列表</Link>
      <article style={{ marginTop: 24 }}>
        <div style={{ fontSize: 13, color: 'var(--c-primary)', marginBottom: 12 }}>{news.category} · {news.date}</div>
        <h1 style={{ fontSize: 30, fontWeight: 700, marginBottom: 24, lineHeight: 1.3 }}>{news.title}</h1>
        {news.image && <img src={news.image} alt={news.title} style={{ width: '100%', borderRadius: 14, marginBottom: 28 }} />}
        <div style={{ fontSize: 16, lineHeight: 1.9, color: 'var(--c-text-sec)' }}>
          {news.content.map((para, i) => (
            <p key={i} style={{ marginBottom: 16 }}>{para}</p>
          ))}
        </div>
      </article>
    </div>
    </PublicLayout>
  );
}
