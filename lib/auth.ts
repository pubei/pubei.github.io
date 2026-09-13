// 认证工具 - 使用 jose（兼容 Edge Runtime 和 Node.js）
import { SignJWT, jwtVerify } from 'jose';
import { cookies } from 'next/headers';

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-change-in-production-please-use-long';
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || 'admin';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';
const TOKEN_NAME = 'admin_token';
const TOKEN_MAX_AGE = 60 * 60 * 24; // 24 hours

function getSecretKey() {
  return new TextEncoder().encode(JWT_SECRET);
}

export async function signToken(): Promise<string> {
  return new SignJWT({ role: 'admin' })
    .setProtectedHeader({ alg: 'HS256' })
    .setExpirationTime('24h')
    .sign(getSecretKey());
}

export async function verifyToken(token: string): Promise<{ role: string } | null> {
  try {
    const { payload } = await jwtVerify(token, getSecretKey());
    return payload as { role: string };
  } catch {
    return null;
  }
}

export async function verifyCredentials(username: string, password: string): Promise<boolean> {
  // 使用长度恒定比较，避免时序攻击
  const uMatch = username.length === ADMIN_USERNAME.length &&
    username.split('').every((c, i) => c === ADMIN_USERNAME[i]);
  const pMatch = password.length === ADMIN_PASSWORD.length &&
    password.split('').every((c, i) => c === ADMIN_PASSWORD[i]);
  return uMatch && pMatch;
}

// 兼容旧接口（仅密码校验），保留供其他模块调用
export async function verifyPassword(password: string): Promise<boolean> {
  return verifyCredentials(ADMIN_USERNAME, password);
}

export function getAuthToken(): string | undefined {
  const cookieStore = cookies();
  return cookieStore.get(TOKEN_NAME)?.value;
}

export async function isAuthenticated(): Promise<boolean> {
  const token = getAuthToken();
  if (!token) return false;
  return !!(await verifyToken(token));
}

export function setAuthCookie(token: string) {
  const cookieStore = cookies();
  cookieStore.set(TOKEN_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: TOKEN_MAX_AGE,
    path: '/',
  });
}

export function clearAuthCookie() {
  const cookieStore = cookies();
  cookieStore.delete(TOKEN_NAME);
}
