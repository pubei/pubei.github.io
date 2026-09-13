import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { exportAll, importAll, resetAll } from '@/lib/kv';
import { audit } from '@/lib/audit';

// 导出全量备份
export async function GET() {
  try {
    const backup = await exportAll();
    return NextResponse.json({ success: true, data: backup });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

// 导入恢复
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    if (!body || !body.data) return NextResponse.json({ success: false, error: '备份格式错误' }, { status: 400 });
    await importAll(body);
    await audit.import('backup', 'all', `恢复备份 ${new Date(body.exportedAt || Date.now()).toLocaleString('zh-CN')}`);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

// 重置（清空所有业务数据，保留 contact:info / about:info / settings:site）
export async function DELETE() {
  try {
    await resetAll();
    await audit.reset('backup', 'all', '重置全部数据');
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
