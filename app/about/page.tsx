import { getAboutInfo, getContactInfo } from '@/lib/kv';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function AboutPage() {
  const [about, contact] = await Promise.all([getAboutInfo(), getContactInfo()]);

  return (
    <PublicLayout>
    <div>
      <section style={{ maxWidth: 900, margin: '0 auto', padding: '60px 24px' }}>
        <h1 style={{ fontSize: 36, fontWeight: 700, textAlign: 'center', marginBottom: 24 }}>关于我们</h1>
        <p style={{ fontSize: 18, lineHeight: 1.9, color: 'var(--c-text-sec)', textAlign: 'center', marginBottom: 48 }}>{about.intro}</p>

        {/* Stats */}
        {about.stats.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 20, marginBottom: 56 }}>
            {about.stats.map((s, i) => (
              <div key={i} style={{ textAlign: 'center', padding: 24, borderRadius: 16, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)' }}>
                <div style={{ fontSize: 36, fontWeight: 800, background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>{s.value}</div>
                <div style={{ fontSize: 14, color: 'var(--c-text-muted)', marginTop: 6 }}>{s.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Commitments */}
        {about.commitments.length > 0 && (
          <div style={{ marginBottom: 56 }}>
            <h2 style={{ fontSize: 24, fontWeight: 600, textAlign: 'center', marginBottom: 24 }}>服务承诺</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center' }}>
              {about.commitments.map((c, i) => (
                <span key={i} style={{ padding: '8px 20px', borderRadius: 20, background: 'rgba(0,212,255,0.1)', border: '1px solid rgba(0,212,255,0.25)', fontSize: 14 }}>{c}</span>
              ))}
            </div>
          </div>
        )}

        {/* Vision */}
        {about.vision && (
          <div style={{ textAlign: 'center', padding: 40, borderRadius: 18, background: 'linear-gradient(135deg, rgba(0,212,255,0.08), rgba(123,47,247,0.08))', border: '1px solid var(--c-border)' }}>
            <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 12 }}>企业愿景</h2>
            <p style={{ fontSize: 16, color: 'var(--c-text-sec)', lineHeight: 1.8 }}>{about.vision}</p>
          </div>
        )}

        {/* History */}
        {about.history.length > 0 && (
          <div style={{ marginTop: 56 }}>
            <h2 style={{ fontSize: 24, fontWeight: 600, textAlign: 'center', marginBottom: 32 }}>发展历程</h2>
            <div style={{ position: 'relative', paddingLeft: 30 }}>
              <div style={{ position: 'absolute', left: 10, top: 0, bottom: 0, width: 2, background: 'var(--c-border)' }} />
              {about.history.map((h, i) => (
                <div key={i} style={{ position: 'relative', marginBottom: 24, paddingLeft: 20 }}>
                  <div style={{ position: 'absolute', left: -24, top: 6, width: 12, height: 12, borderRadius: '50%', background: 'var(--c-primary)' }} />
                  <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--c-primary)', marginBottom: 4 }}>{h.year}</div>
                  <div style={{ fontSize: 15, color: 'var(--c-text-sec)' }}>{h.event}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Contact */}
        <div style={{ marginTop: 56, textAlign: 'center', padding: 32, borderRadius: 16, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)' }}>
          <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 16 }}>联系我们</h2>
          <p style={{ fontSize: 16, marginBottom: 8 }}>📞 {contact.phone}</p>
          <p style={{ fontSize: 15, color: 'var(--c-text-sec)' }}>📍 {contact.address}</p>
        </div>
      </section>
    </div>
    </PublicLayout>
  );
}
