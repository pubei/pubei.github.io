import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllGallery, deleteGalleryItem } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const keyword = searchParams.get('q');
  let items = await getAllGallery();
  if (keyword) {
    const k = keyword.toLowerCase();
    items = items.filter((g) => g.name.toLowerCase().includes(k) || g.type.toLowerCase().includes(k));
  }
  items.sort((a, b) => b.createdAt - a.createdAt);
  return NextResponse.json({ success: true, data: items, total: items.length });
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    await deleteGalleryItem(id);
    await audit.remove('gallery', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
