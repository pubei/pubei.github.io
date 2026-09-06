import { getProjectById } from '@/lib/kv';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function ProjectDetailPage({ params }: { params: { id: string } }) {
  const project = await getProjectById(params.id);
  if (!project) notFound();

  return (
    <PublicLayout>
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '60px 24px' }}>
      <Link href="/projects" style={{ color: 'var(--c-primary)', fontSize: 14 }}>← 返回案例列表</Link>
      <div style={{ marginTop: 24 }}>
        <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 16 }}>{project.name}</h1>
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', marginBottom: 28, fontSize: 14, color: 'var(--c-text-sec)' }}>
          <span>🏠 风格：{project.style}</span>
          <span>📐 户型：{project.layout}</span>
          <span>📏 面积：{project.area}</span>
          <span>📍 {project.address}</span>
        </div>

        {project.images.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 12, marginBottom: 32 }}>
            {project.images.map((img, i) => (
              <img key={i} src={img} alt={`${project.name} ${i + 1}`} style={{ width: '100%', borderRadius: 12, aspectRatio: '4/3', objectFit: 'cover' }} />
            ))}
          </div>
        )}

        {project.description && (
          <p style={{ fontSize: 16, lineHeight: 1.9, color: 'var(--c-text-sec)', whiteSpace: 'pre-wrap' }}>{project.description}</p>
        )}

        <Link href="/contact" style={{ display: 'inline-block', marginTop: 40, padding: '14px 32px', background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', borderRadius: 30, color: 'white', fontWeight: 600 }}>
          预约类似案例 →
        </Link>
      </div>
    </div>
    </PublicLayout>
  );
}
