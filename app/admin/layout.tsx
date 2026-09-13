import { isAuthenticated } from '@/lib/auth';
import AdminSidebar from './AdminSidebar';
import { ToastProvider } from '@/components/AdminUI';

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const authed = await isAuthenticated();
  if (!authed) {
    return <ToastProvider>{children}</ToastProvider>;
  }
  return (
    <ToastProvider>
      <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--c-bg)' }}>
        <AdminSidebar />
        <main style={{ flex: 1, padding: '24px', overflowY: 'auto' }}>
          {children}
        </main>
      </div>
    </ToastProvider>
  );
}
