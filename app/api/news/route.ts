import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllNews, getNewsList, createNews, updateNews, deleteNews } from '@/lib/kv';
import type { NewsItem } from '@/lib/types';

// GET 列表 / 详情
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const page = parseInt(searchParams.get('page') || '1', 10);
  const pageSize = parseInt(searchParams.get('pageSize') || '10', 10);
  const all = searchParams.get('all') === 'true'; // 后台用，返回所有（含未发布）

  if (id) {
    const items = await getAllNews();
    const item = items.find((n) => n.id === id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }

  if (all) {
    const items = await getAllNews();
    items.sort((a, b) => b.createdAt - a.createdAt);
    return NextResponse.json({ success: true, data: items, total: items.length });
  }

  const result = await getNewsList(page, pageSize, true);
  return NextResponse.json({ success: true, ...result });
}

// POST 新增
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const id = body.id || `n_${Date.now()}`;
    const news = await createNews({
      id,
      date: body.date || new Date().toISOString().slice(0, 10),
      category: body.category || '行业资讯',
      title: body.title,
      image: body.image || '',
      image_fallback: body.image_fallback || '',
      excerpt: body.excerpt || '',
      content: Array.isArray(body.content) ? body.content : [body.content],
      published: body.published !== false,
    });
    return NextResponse.json({ success: true, data: news });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

// PUT 编辑
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, ...updates } = body;
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    const updated = await updateNews(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: updated });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}

// DELETE 删除
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    if (!id) return NextResponse.json({ success: false, error: '缺少 id' }, { status: 400 });
    await deleteNews(id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
