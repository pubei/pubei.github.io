import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllLeads, getLeadById, createLead, updateLead, deleteLead } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const status = searchParams.get('status');
  const keyword = searchParams.get('q');
  if (id) {
    const item = await getLeadById(id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }
  let items = await getAllLeads();
  if (status && status !== 'all') items = items.filter((l) => l.status === status);
  if (keyword) {
    const k = keyword.toLowerCase();
    items = items.filter((l) => l.name.toLowerCase().includes(k) || l.phone.includes(k) || (l.service || '').toLowerCase().includes(k));
  }
  items.sort((a, b) => b.createdAt - a.createdAt);
  return NextResponse.json({ success: true, data: items, total: items.length });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const lead = await createLead({
      name: body.name || '未命名',
      phone: body.phone || '',
      email: body.email || '',
      service: body.service || '',
      area: body.area || '',
      budget: body.budget || '',
      appointmentTime: body.appointmentTime || '',
      message: body.message || '',
      source: body.source || '手动录入',
      status: body.status || 'new',
      notes: Array.isArray(body.notes) ? body.notes : [],
      order: body.order || 0,
    });
    await audit.create('lead', lead.id, `新增客户 ${lead.name}`);
    return NextResponse.json({ success: true, data: lead });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, ...updates } = body;
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    const updated = await updateLead(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    await audit.update('lead', id, `更新客户 ${updated.name}`);
    return NextResponse.json({ success: true, data: updated });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    await deleteLead(id);
    await audit.remove('lead', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
