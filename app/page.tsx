import { getAllNews, getAllServices, getAllProjects, getContactInfo } from '@/lib/kv';
import Link from 'next/link';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function HomePage() {
  const [news, services, projects, contact] = await Promise.all([
    getAllNews(),
    getAllServices(),
    getAllProjects(),
    getContactInfo(),
  ]);

  const publishedNews = news.filter((n) => n.published).sort((a, b) => b.createdAt - a.createdAt).slice(0, 3);
  const sortedServices = services.sort((a, b) => a.order - b.order).slice(0, 6);
  const sortedProjects = projects.sort((a, b) => a.order - b.order).slice(0, 3);

  return (
    <PublicLayout>
    <div>
      {/* Hero */}
      <section style={heroStyle}>
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '80px 24px', textAlign: 'center' }}>
          <h1 style={{ fontSize: 'clamp(32px, 5vw, 56px)', fontWeight: 800, background: 'linear-gradient(135deg, #00d4ff, #7b2ff7 50%, #00ff80)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: 16 }}>
            浦北装修设计
          </h1>
          <p style={{ fontSize: 18, color: 'var(--c-text-sec)', marginBottom: 32, maxWidth: 600, margin: '0 auto 32px' }}>
            专业室内外装饰装修，全屋定制 · 新房装修 · 旧房翻新 · 软装设计
          </p>
          <Link href="/contact" style={ctaBtn}>免费预约咨询 →</Link>
        </div>
      </section>

      {/* Services */}
      {sortedServices.length > 0 && (
        <section style={sectionStyle}>
          <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
            <h2 style={sectionTitle}>服务项目</h2>
            <div style={grid3}>
              {sortedServices.map((s) => (
                <Link key={s.id} href={`/services/${s.id}`} style={cardStyle}>
                  <h3 style={{ fontSize: 17, fontWeight: 600, marginBottom: 8 }}>{s.name}</h3>
                  <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>{s.description}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Projects */}
      {sortedProjects.length > 0 && (
        <section style={{ ...sectionStyle, background: 'rgba(255,255,255,0.02)' }}>
          <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
            <h2 style={sectionTitle}>精选案例</h2>
            <div style={grid3}>
              {sortedProjects.map((p) => (
                <Link key={p.id} href={`/projects/${p.id}`} style={{ ...cardStyle, padding: 0, overflow: 'hidden' }}>
                  {p.cover && <img src={p.cover} alt={p.name} style={{ width: '100%', height: 180, objectFit: 'cover' }} />}
                  <div style={{ padding: 18 }}>
                    <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{p.name}</h3>
                    <p style={{ fontSize: 13, color: 'var(--c-text-muted)' }}>{p.style} · {p.area}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* News */}
      {publishedNews.length > 0 && (
        <section style={sectionStyle}>
          <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
            <h2 style={sectionTitle}>最新动态</h2>
            <div style={grid3}>
              {publishedNews.map((n) => (
                <Link key={n.id} href={`/news/${n.id}`} style={cardStyle}>
                  <div style={{ fontSize: 12, color: 'var(--c-primary)', marginBottom: 8 }}>{n.category} · {n.date}</div>
                  <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 8, lineHeight: 1.4 }}>{n.title}</h3>
                  <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>{n.excerpt}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section style={{ ...sectionStyle, background: 'linear-gradient(135deg, rgba(0,212,255,0.08), rgba(123,47,247,0.08))' }}>
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px', textAlign: 'center' }}>
          <h2 style={{ fontSize: 28, fontWeight: 700, marginBottom: 12 }}>准备好开始您的装修之旅了吗？</h2>
          <p style={{ color: 'var(--c-text-sec)', marginBottom: 24 }}>联系我们，获取免费设计方案与报价</p>
          <Link href="/contact" style={ctaBtn}>立即预约</Link>
        </div>
      </section>
    </div>
    </PublicLayout>
  );
}

const heroStyle: React.CSSProperties = { background: 'radial-gradient(ellipse at center, rgba(0,212,255,0.12), transparent 70%), var(--c-bg)', padding: '60px 0' };
const sectionStyle: React.CSSProperties = { padding: '20px 0' };
const sectionTitle: React.CSSProperties = { fontSize: 28, fontWeight: 700, textAlign: 'center', marginBottom: 36 };
const grid3: React.CSSProperties = { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 20 };
const cardStyle: React.CSSProperties = { display: 'block', padding: 24, borderRadius: 16, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)', transition: 'all 0.3s' };
const ctaBtn: React.CSSProperties = { display: 'inline-block', padding: '14px 32px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', borderRadius: 30, color: 'white', fontWeight: 600, fontSize: 16 };
