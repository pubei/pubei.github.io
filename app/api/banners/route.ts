import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllBanners, getBannerById, createBanner, updateBanner, deleteBanner } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  if (id) {
    const item = await getBannerById(id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }
  const items = await getAllBanners();
  items.sort((a, b) => a.order - b.order);
  return NextResponse.json({ success: true, data: items });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const item = await createBanner({
      title: body.title || '',
      subtitle: body.subtitle || '',
      image: body.image || '',
      link: body.link || '',
      ctaText: body.ctaText || '立即咨询',
      order: body.order || 0,
      enabled: body.enabled !== false,
    });
    await audit.create('banner', item.id, `新增 Banner ${item.title}`);
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
    const updated = await updateBanner(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    await audit.update('banner', id, `更新 Banner ${updated.title}`);
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
    await deleteBanner(id);
    await audit.remove('banner', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
