import { getContactInfo } from '@/lib/kv';
import ContactForm from './ContactForm';
import PublicLayout from '@/components/PublicLayout';

export const dynamic = 'force-dynamic';

export default async function ContactPage() {
  const contact = await getContactInfo();

  return (
    <PublicLayout>
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '60px 24px' }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, textAlign: 'center', marginBottom: 40 }}>在线预约咨询</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        {/* Contact Info */}
        <div style={{ padding: 32, borderRadius: 16, background: 'rgba(255,255,255,0.04)', border: '1px solid var(--c-border)' }}>
          <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 20 }}>联系方式</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16, fontSize: 15, color: 'var(--c-text-sec)' }}>
            <div>📞 电话：{contact.phone}</div>
            <div>✉️ 邮箱：{contact.email}</div>
            <div>📍 地址：{contact.address}</div>
            <div>💬 微信：{contact.wechat}</div>
            <div>🕐 时间：{contact.hours}</div>
          </div>
        </div>

        {/* Form */}
        <ContactForm />
      </div>
    </div>
    </PublicLayout>
  );
}
