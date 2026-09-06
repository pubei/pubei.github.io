// 数据迁移脚本 - 将现有新闻数据导入 Vercel KV
// 运行方式: node scripts/seed.mjs
// 需要环境变量: KV_REST_API_URL, KV_REST_API_TOKEN

import { kv } from '@vercel/kv';
import { readFileSync } from 'fs';

const newsData = JSON.parse(readFileSync('./assets/data/news-data.json', 'utf-8'));

// 转换数据格式
const newsItems = newsData.map((item, idx) => ({
  id: item.id || `news_${Date.now()}_${idx}`,
  date: item.date,
  category: item.category || '行业资讯',
  title: item.title,
  image: item.image || '',
  image_fallback: item.image_fallback ? item.image_fallback.replace('assets/', '/') : '',
  excerpt: item.excerpt || '',
  content: Array.isArray(item.content) ? item.content : [item.content],
  published: true,
  createdAt: new Date(item.date).getTime() || Date.now() - idx * 86400000,
  updatedAt: Date.now(),
}));

console.log(`准备导入 ${newsItems.length} 条新闻...`);

try {
  await kv.set('news:all', newsItems);
  console.log(`✓ 成功导入 ${newsItems.length} 条新闻到 KV`);
} catch (e) {
  console.error('导入失败:', e.message);
  process.exit(1);
}

// 验证
const verify = await kv.get('news:all');
console.log(`✓ 验证: KV 中现有 ${verify.length} 条新闻`);
