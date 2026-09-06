import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-change-in-production-please-use-long';

async function verifyTokenEdge(token: string): Promise<boolean> {
  try {
    await jwtVerify(token, new TextEncoder().encode(JWT_SECRET));
    return true;
  } catch {
    return false;
  }
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('admin_token')?.value;
  const authed = token ? await verifyTokenEdge(token) : false;

  // 保护 /admin 下除登录页外的所有页面
  if (pathname.startsWith('/admin') && pathname !== '/admin/login') {
    if (!authed) {
      const url = request.nextUrl.clone();
      url.pathname = '/admin/login';
      return NextResponse.redirect(url);
    }
  }

  // 保护 /api 写接口
  const isWriteApi = pathname.startsWith('/api') && pathname !== '/api/auth/login';
  if (isWriteApi) {
    const method = request.method;
    if (method !== 'GET' && method !== 'OPTIONS') {
      if (!authed) {
        return NextResponse.json({ success: false, error: '未授权' }, { status: 401 });
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*', '/api/:path*'],
};
