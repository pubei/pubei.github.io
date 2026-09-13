import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllFAQs, getFAQById, createFAQ, updateFAQ, deleteFAQ } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  if (id) {
    const item = await getFAQById(id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }
  const items = await getAllFAQs();
  items.sort((a, b) => a.order - b.order);
  return NextResponse.json({ success: true, data: items });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const item = await createFAQ({
      question: body.question || '',
      answer: body.answer || '',
      category: body.category || '通用',
      order: body.order || 0,
      enabled: body.enabled !== false,
    });
    await audit.create('faq', item.id, `新增 FAQ ${item.question.slice(0, 20)}`);
    return NextResponse.json({ success: true, data: item });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, ...updates } = body;
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    const updated = await updateFAQ(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    await audit.update('faq', id, '更新 FAQ');
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
    await deleteFAQ(id);
    await audit.remove('faq', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
