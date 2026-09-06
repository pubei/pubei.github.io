import { NextRequest, NextResponse } from 'next/server';
import { verifyPassword, signToken, setAuthCookie } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    const { password } = await request.json();
    if (!password) {
      return NextResponse.json({ success: false, error: '请输入密码' }, { status: 400 });
    }
    const valid = await verifyPassword(password);
    if (!valid) {
      return NextResponse.json({ success: false, error: '密码错误' }, { status: 401 });
    }
    const token = await signToken();
    setAuthCookie(token);
    return NextResponse.json({ success: true });
  } catch (e) {
    return NextResponse.json({ success: false, error: '服务器错误' }, { status: 500 });
  }
}
