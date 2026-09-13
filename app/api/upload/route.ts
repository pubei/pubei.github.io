import { NextRequest, NextResponse } from 'next/server';
import { addGalleryItem } from '@/lib/kv';
import { audit } from '@/lib/audit';

export const runtime = 'nodejs';

const MAX_SIZE = 4 * 1024 * 1024; // 4MB (Vercel serverless limit)
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml'];

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;

    if (!file) {
      return NextResponse.json({ success: false, error: '未上传文件' }, { status: 400 });
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      return NextResponse.json(
        { success: false, error: `不支持的文件类型: ${file.type}` },
        { status: 400 }
      );
    }

    if (file.size > MAX_SIZE) {
      return NextResponse.json(
        { success: false, error: `文件过大 (${(file.size / 1024 / 1024).toFixed(1)}MB)，最大 4MB` },
        { status: 400 }
      );
    }

    // 转换为 base64 data URL
    const buffer = Buffer.from(await file.arrayBuffer());
    const base64 = buffer.toString('base64');
    const dataUrl = `data:${file.type};base64,${base64}`;

    // 生成唯一 ID
    const imageId = `img_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const url = dataUrl;

    // 将图片元数据存入 KV 便于后台图库管理（复用 lib/kv.ts 的封装，避免重复实现）
    try {
      await addGalleryItem({
        id: imageId,
        type: file.type,
        size: file.size,
        name: file.name,
        url,
        createdAt: Date.now(),
      });
    } catch {
      // KV 存储失败不影响上传主流程
    }

    await audit.create('gallery', imageId, `上传图片 ${file.name}`);

    return NextResponse.json({
      success: true,
      url,
      id: imageId,
      name: file.name,
      size: file.size,
    });
  } catch (e: any) {
    return NextResponse.json(
      { success: false, error: '上传失败: ' + (e.message || String(e)) },
      { status: 500 }
    );
  }
}

// 允许 CORS
export async function OPTIONS() {
  return new NextResponse(null, { status: 204 });
}
