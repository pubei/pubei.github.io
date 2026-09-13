import { NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getKVStatus, getStats } from '@/lib/kv';

export async function GET() {
  const startedAt = Date.now();
  try {
    const [kvStatus, stats] = await Promise.all([getKVStatus(), getStats()]);
    return NextResponse.json({
      success: true,
      data: {
        status: 'ok',
        timestamp: startedAt,
        latencyMs: Date.now() - startedAt,
        kv: kvStatus,
        stats,
        version: '1.0',
      },
    });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message, status: 'error' }, { status: 500 });
  }
}
