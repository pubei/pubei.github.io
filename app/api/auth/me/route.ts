import { NextResponse } from 'next/server';
import { isAuthenticated } from '@/lib/auth';

export async function GET() {
  return NextResponse.json({ success: true, authenticated: isAuthenticated() });
}
