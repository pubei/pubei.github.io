import { getAllProjects } from '@/lib/kv';
import Link from 'next/link';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function ProjectsListPage() {
  const projects = (await getAllProjects()).sort((a, b) => a.order - b.order);

  return (
    <PublicLayout>
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px' }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, textAlign: 'center', marginBottom: 40 }}>装修案例</h1>
      {projects.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--c-text-muted)' }}>暂无案例</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 20 }}>
          {projects.map((p) => (
            <Link key={p.id} href={`/projects/${p.id}`} style={{
              borderRadius: 16, overflow: 'hidden', background: 'rgba(255,255,255,0.04)',
              border: '1px solid var(--c-border)', transition: 'all 0.3s',
            }}>
              {p.cover && <img src={p.cover} alt={p.name} style={{ width: '100%', height: 200, objectFit: 'cover' }} />}
              <div style={{ padding: 18 }}>
                <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 6 }}>{p.name}</h2>
                <p style={{ fontSize: 13, color: 'var(--c-text-muted)' }}>{p.style} · {p.layout} · {p.area}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
    </PublicLayout>
  );
}
