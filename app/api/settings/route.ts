import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getSettings, updateSettings } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET() {
  const info = await getSettings();
  return NextResponse.json({ success: true, data: info });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const info = await updateSettings({
      metaTitle: body.metaTitle,
      metaDescription: body.metaDescription,
      metaKeywords: body.metaKeywords,
      ogImage: body.ogImage,
      favicon: body.favicon,
      analyticsCode: body.analyticsCode,
      icp: body.icp,
      social: Array.isArray(body.social) ? body.social : [],
      announcement: body.announcement,
      announcementEnabled: body.announcementEnabled,
    });
    await audit.update('settings', 'site', '更新站点设置');
    return NextResponse.json({ success: true, data: info });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
