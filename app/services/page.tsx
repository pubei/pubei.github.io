import { getAllServices } from '@/lib/kv';
import Link from 'next/link';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function ServicesListPage() {
  const services = (await getAllServices()).sort((a, b) => a.order - b.order);

  return (
    <PublicLayout>
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, textAlign: 'center', marginBottom: 40 }}>服务项目</h1>
      {services.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--c-text-muted)' }}>暂无服务</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 20 }}>
          {services.map((s) => (
            <Link key={s.id} href={`/services/${s.id}`} style={{
              padding: 28, borderRadius: 16, background: 'rgba(255,255,255,0.04)',
              border: '1px solid var(--c-border)', transition: 'all 0.3s',
            }}>
              <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 12 }}>{s.name}</h2>
              <p style={{ fontSize: 14, color: 'var(--c-text-sec)', lineHeight: 1.6, marginBottom: 16 }}>{s.description}</p>
              {s.features.slice(0, 3).map((f, i) => (
                <div key={i} style={{ fontSize: 13, color: 'var(--c-text-muted)', marginBottom: 6 }}>✓ {f}</div>
              ))}
            </Link>
          ))}
        </div>
      )}
    </div>
    </PublicLayout>
  );
}
