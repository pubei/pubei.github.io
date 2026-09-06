import { getContactInfo } from '@/lib/kv';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

export default async function Footer() {
  const contact = await getContactInfo();
  return (
    <footer style={{ background: 'rgba(10,14,23,0.95)', borderTop: '1px solid var(--c-border)', padding: '40px 24px', marginTop: 40 }}>
      <div style={{ maxWidth: 1100, margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 32 }}>
        <div>
          <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>联系我们</h3>
          <div style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 2 }}>
            <div>📞 {contact.phone}</div>
            <div>✉️ {contact.email}</div>
            <div>📍 {contact.address}</div>
            <div>🕐 {contact.hours}</div>
          </div>
        </div>
        <div>
          <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>快速导航</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13 }}>
            <Link href="/services" style={{ color: 'var(--c-text-sec)' }}>服务项目</Link>
            <Link href="/projects" style={{ color: 'var(--c-text-sec)' }}>装修案例</Link>
            <Link href="/news" style={{ color: 'var(--c-text-sec)' }}>公司新闻</Link>
            <Link href="/about" style={{ color: 'var(--c-text-sec)' }}>关于我们</Link>
          </div>
        </div>
        <div>
          <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>浦北装修设计</h3>
          <p style={{ fontSize: 13, color: 'var(--c-text-muted)', lineHeight: 1.7 }}>
            专业室内外装饰装修，全屋定制、新房装修、旧房翻新、软装设计，为您打造理想家居空间。
          </p>
        </div>
      </div>
      <div style={{ maxWidth: 1100, margin: '24px auto 0', paddingTop: 20, borderTop: '1px solid var(--c-border)', textAlign: 'center', fontSize: 12, color: 'var(--c-text-muted)' }}>
        © 2026 浦北装修设计 · pboo.top
      </div>
    </footer>
  );
}
