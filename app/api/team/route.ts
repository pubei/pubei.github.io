import { NextRequest, NextResponse } from 'next/server';
export const dynamic = 'force-dynamic';
import { getAllTeam, getTeamMemberById, createTeamMember, updateTeamMember, deleteTeamMember } from '@/lib/kv';
import { audit } from '@/lib/audit';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  if (id) {
    const item = await getTeamMemberById(id);
    if (!item) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    return NextResponse.json({ success: true, data: item });
  }
  const items = await getAllTeam();
  items.sort((a, b) => a.order - b.order);
  return NextResponse.json({ success: true, data: items });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const item = await createTeamMember({
      name: body.name || '',
      role: body.role || '',
      avatar: body.avatar || '',
      bio: body.bio || '',
      skills: Array.isArray(body.skills) ? body.skills : [],
      order: body.order || 0,
      enabled: body.enabled !== false,
    });
    await audit.create('team', item.id, `新增成员 ${item.name}`);
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
    const updated = await updateTeamMember(id, updates);
    if (!updated) return NextResponse.json({ success: false, error: '未找到' }, { status: 404 });
    await audit.update('team', id, `更新成员 ${updated.name}`);
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
    await deleteTeamMember(id);
    await audit.remove('team', id);
    return NextResponse.json({ success: true });
  } catch (e: any) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
