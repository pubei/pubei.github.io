import { getServiceById } from '@/lib/kv';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function ServiceDetailPage({ params }: { params: { id: string } }) {
  const service = await getServiceById(params.id);
  if (!service) notFound();

  return (
    <PublicLayout>
    <div style={{ maxWidth: 900, margin: '0 auto', padding: '60px 24px' }}>
      <Link href="/services" style={{ color: 'var(--c-primary)', fontSize: 14 }}>← 返回服务列表</Link>
      <div style={{ marginTop: 24 }}>
        {service.image && <img src={service.image} alt={service.name} style={{ width: '100%', borderRadius: 14, marginBottom: 28, maxHeight: 400, objectFit: 'cover' }} />}
        <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 16 }}>{service.name}</h1>
        <p style={{ fontSize: 17, color: 'var(--c-text-sec)', lineHeight: 1.8, marginBottom: 32 }}>{service.description}</p>

        {service.features.length > 0 && (
          <div style={{ marginBottom: 32 }}>
            <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 16 }}>服务特点</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {service.features.map((f, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 15, color: 'var(--c-text-sec)' }}>
                  <span style={{ color: 'var(--c-accent)' }}>✓</span> {f}
                </div>
              ))}
            </div>
          </div>
        )}

        {service.process.length > 0 && (
          <div>
            <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 16 }}>服务流程</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {service.process.map((p, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <span style={{ width: 28, height: 28, borderRadius: '50%', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 13, flexShrink: 0 }}>{i + 1}</span>
                  <span style={{ fontSize: 15, color: 'var(--c-text-sec)' }}>{p}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <Link href="/contact" style={{ display: 'inline-block', marginTop: 40, padding: '14px 32px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', borderRadius: 30, color: 'white', fontWeight: 600 }}>
          预约此服务 →
        </Link>
      </div>
    </div>
    </PublicLayout>
  );
}
