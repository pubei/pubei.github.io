import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAuditLogs, clearAuditLogs } from '@/lib/kv';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const limit = parseInt(searchParams.get('limit') || '100', 10);
  const module = searchParams.get('module');
  const action = searchParams.get('action');
  let items = await getAuditLogs(limit);
  if (module && module !== 'all') items = items.filter((l) => l.module === module);
  if (action && action !== 'all') items = items.filter((l) => l.action === action);
  return NextResponse.json({ success: true, data: items, total: items.length });
}

export async function DELETE() {
  await clearAuditLogs();
  return NextResponse.json({ success: true });
}
