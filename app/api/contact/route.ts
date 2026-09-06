import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getContactInfo, updateContactInfo } from '@/lib/kv';

export async function GET() {
  const info = await getContactInfo();
  return NextResponse.json({ success: true, data: info });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const info = await updateContactInfo({
      phone: body.phone || '',
      email: body.email || '',
      address: body.address || '',
      wechat: body.wechat || '',
      hours: body.hours || '',
      lat: body.lat || '',
      lng: body.lng || '',
    });
    return NextResponse.json({ success: true, data: info });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
