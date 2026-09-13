import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllTestimonials, getTestimonialById, createTestimonial, updateTestimonial, deleteTestimonial } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  if (id) {
    const item = await getTestimonialById(id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }
  const items = await getAllTestimonials();
  items.sort((a, b) => a.order - b.order);
  return NextResponse.json({ success: true, data: items });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const item = await createTestimonial({
      customer: body.customer || '',
      project: body.project || '',
      rating: Number(body.rating) || 5,
      content: body.content || '',
      avatar: body.avatar || '',
      order: body.order || 0,
      enabled: body.enabled !== false,
    });
    await audit.create('testimonial', item.id, `新增评价 ${item.customer}`);
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
    const updated = await updateTestimonial(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    await audit.update('testimonial', id, `更新评价 ${updated.customer}`);
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
    await deleteTestimonial(id);
    await audit.remove('testimonial', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
