'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useState } from 'react';

interface MenuItem {
  href: string;
  label: string;
  icon: string;
}
interface MenuGroup {
  title: string;
  items: MenuItem[];
}

const menuGroups: MenuGroup[] = [
  {
    title: '概览',
    items: [{ href: '/admin/dashboard', label: 'Dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' }],
  },
  {
    title: '内容管理',
    items: [
      { href: '/admin/news', label: '新闻管理', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
      { href: '/admin/services', label: '服务项目', icon: 'M20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75zM3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z' },
      { href: '/admin/projects', label: '装修案例', icon: 'M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z' },
      { href: '/admin/banners', label: '首页 Banner', icon: 'M4 4h16v12H4V4zm0 14h16M6 20h2m8 0h2M8 20v2m8-2v2' },
      { href: '/admin/testimonials', label: '客户评价', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.196-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.783-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' },
      { href: '/admin/faqs', label: 'FAQ 管理', icon: 'M8.228 9C8.228 7.895 9.296 7 11 7c1.704 0 2.772.895 2.772 2 0 .621-.371 1.07-.665 1.402-.243.275-.51.563-.51.961v.637m0 1.5v1m5.273-9A9 9 0 11.528 9.028' },
    ],
  },
  {
    title: '客户管理',
    items: [
      { href: '/admin/leads', label: '客户咨询', icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' },
    ],
  },
  {
    title: '资源管理',
    items: [
      { href: '/admin/gallery', label: '图片库', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
      { href: '/admin/team', label: '团队成员', icon: 'M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m6-1.13a4 4 0 10-4-4 4 4 0 004 4zm6 0a3 3 0 10-3-3' },
    ],
  },
  {
    title: '系统',
    items: [
      { href: '/admin/contact', label: '联系资料', icon: 'M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z' },
      { href: '/admin/about', label: '公司资料', icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z' },
      { href: '/admin/settings', label: '站点设置', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065zM15 12a3 3 0 11-6 0 3 3 0 016 0z' },
      { href: '/admin/audit', label: '活动日志', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
      { href: '/admin/backup', label: '数据备份', icon: 'M4 7v10a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2zm0 0V5a2 2 0 012-2h12a2 2 0 012 2v2M8 11h8' },
      { href: '/admin/api-docs', label: 'API 文档', icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4' },
    ],
  },
];

export default function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    router.push('/admin/login');
  };

  return (
    <aside style={{
      width: collapsed ? 64 : 230,
      background: 'linear-gradient(180deg, rgba(15,20,35,0.95), rgba(10,14,23,0.98))',
      backdropFilter: 'blur(20px)',
      borderRight: '1px solid var(--c-border)',
      display: 'flex',
      flexDirection: 'column',
      padding: '20px 0',
      transition: 'width 0.3s ease',
      position: 'sticky',
      top: 0,
      height: '100vh',
      overflowY: 'auto',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px', marginBottom: 20 }}>
        {!collapsed && (
          <div style={{ fontSize: 15, fontWeight: 700, background: 'linear-gradient(135deg, #00d4ff, #7b2ff7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            浦北后台
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          style={{ background: 'transparent', border: 'none', color: 'var(--c-text-muted)', cursor: 'pointer', fontSize: 18 }}
        >
          {collapsed ? '»' : '«'}
        </button>
      </div>

      <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 14, padding: '0 10px' }}>
        {menuGroups.map((group) => (
          <div key={group.title}>
            {!collapsed && (
              <div style={{
                fontSize: 10, fontWeight: 700, color: 'var(--c-text-muted)',
                padding: '0 12px', marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1,
              }}>{group.title}</div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {group.items.map((item) => {
                const active = pathname === item.href;
                return (
                  <Link key={item.href} href={item.href} title={collapsed ? item.label : undefined} style={{
                    display: 'flex', alignItems: 'center', gap: 12,
                    padding: '9px 12px', borderRadius: 10,
                    background: active ? 'rgba(0,212,255,0.12)' : 'transparent',
                    border: active ? '1px solid rgba(0,212,255,0.25)' : '1px solid transparent',
                    color: active ? 'var(--c-primary)' : 'var(--c-text-sec)',
                    transition: 'all 0.2s', fontSize: 13,
                  }}>
                    <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}>
                      <path d={item.icon} />
                    </svg>
                    {!collapsed && <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.label}</span>}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      <div style={{ padding: '0 10px', marginTop: 'auto', paddingTop: 20 }}>
        <button
          onClick={handleLogout}
          title={collapsed ? '退出登录' : undefined}
          style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: '10px 12px', borderRadius: 10,
            background: 'transparent', border: '1px solid transparent',
            color: 'var(--c-text-muted)', cursor: 'pointer', fontSize: 13,
            width: '100%', transition: 'all 0.2s',
          }}
        >
          <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}>
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
          </svg>
          {!collapsed && <span>退出登录</span>}
        </button>
      </div>
    </aside>
  );
}
