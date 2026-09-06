'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/', label: '首页' },
  { href: '/services', label: '服务项目' },
  { href: '/projects', label: '装修案例' },
  { href: '/news', label: '公司新闻' },
  { href: '/about', label: '关于我们' },
  { href: '/contact', label: '在线预约' },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 100,
      background: 'rgba(10,14,23,0.85)', backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--c-border)',
    }}>
      <nav style={{ maxWidth: 1100, margin: '0 auto', padding: '14px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Link href="/" style={{ fontSize: 18, fontWeight: 700, background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          浦北装修设计
        </Link>
        <div style={{ display: 'flex', gap: 24 }}>
          {links.map((l) => {
            const active = pathname === l.href || (l.href !== '/' && pathname.startsWith(l.href));
            return (
              <Link key={l.href} href={l.href} style={{
                fontSize: 14, color: active ? 'var(--c-primary)' : 'var(--c-text-sec)',
                transition: 'color 0.2s',
              }}>
                {l.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
