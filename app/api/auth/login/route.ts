import { NextRequest, NextResponse } from 'next/server';
import { verifyCredentials, signToken, setAuthCookie } from '@/lib/auth';
import { audit } from '@/lib/audit';

export async function POST(request: NextRequest) {
  try {
    const { username, password } = await request.json();
    if (!username || !password) {
      return NextResponse.json({ success: false, error: '请输入账号和密码' }, { status: 400 });
    }
    const valid = await verifyCredentials(username, password);
    if (!valid) {
      return NextResponse.json({ success: false, error: '账号或密码错误' }, { status: 401 });
    }
    const token = await signToken();
    setAuthCookie(token);
    await audit.login(username);
    return NextResponse.json({ success: true });
  } catch (e) {
    return NextResponse.json({ success: false, error: '服务器错误' }, { status: 500 });
  }
}
