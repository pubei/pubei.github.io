import { NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getStats } from '@/lib/kv';

export async function GET() {
  const stats = await getStats();
  return NextResponse.json({ success: true, data: stats });
}
