import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAboutInfo, updateAboutInfo } from '@/lib/kv';

export async function GET() {
  const info = await getAboutInfo();
  return NextResponse.json({ success: true, data: info });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const info = await updateAboutInfo({
      intro: body.intro || '',
      vision: body.vision || '',
      stats: Array.isArray(body.stats) ? body.stats : [],
      commitments: Array.isArray(body.commitments) ? body.commitments : [],
      history: Array.isArray(body.history) ? body.history : [],
    });
    return NextResponse.json({ success: true, data: info });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
