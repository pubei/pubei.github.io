import { PageHeader, Card, Badge } from '@/components/AdminUI';

export const dynamic = 'force-dynamic';

interface Endpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  desc: string;
  auth?: boolean;
}

const groups: { name: string; endpoints: Endpoint[] }[] = [
  {
    name: '认证',
    endpoints: [
      { method: 'POST', path: '/api/auth/login', desc: '管理员登录（无需鉴权）' },
      { method: 'POST', path: '/api/auth/logout', desc: '退出登录' },
      { method: 'GET', path: '/api/auth/me', desc: '查询登录状态' },
    ],
  },
  {
    name: '新闻管理',
    endpoints: [
      { method: 'GET', path: '/api/news', desc: '获取新闻列表 / 详情 (?id= / ?page= / ?all=)' },
      { method: 'POST', path: '/api/news', desc: '新增新闻', auth: true },
      { method: 'PUT', path: '/api/news', desc: '编辑新闻', auth: true },
      { method: 'DELETE', path: '/api/news?id=', desc: '删除新闻', auth: true },
    ],
  },
  {
    name: '服务管理',
    endpoints: [
      { method: 'GET', path: '/api/services', desc: '获取服务列表 / 详情 (?id=)' },
      { method: 'POST', path: '/api/services', desc: '新增服务', auth: true },
      { method: 'PUT', path: '/api/services', desc: '编辑服务', auth: true },
      { method: 'DELETE', path: '/api/services?id=', desc: '删除服务', auth: true },
    ],
  },
  {
    name: '案例管理',
    endpoints: [
      { method: 'GET', path: '/api/projects', desc: '获取案例列表 / 详情 (?id=)' },
      { method: 'POST', path: '/api/projects', desc: '新增案例', auth: true },
      { method: 'PUT', path: '/api/projects', desc: '编辑案例', auth: true },
      { method: 'DELETE', path: '/api/projects?id=', desc: '删除案例', auth: true },
    ],
  },
  {
    name: '客户咨询 CRM',
    endpoints: [
      { method: 'GET', path: '/api/leads', desc: '获取咨询列表 (?status= / ?q= / ?id=)' },
      { method: 'POST', path: '/api/leads', desc: '新增咨询', auth: true },
      { method: 'PUT', path: '/api/leads', desc: '编辑咨询 / 改状态', auth: true },
      { method: 'DELETE', path: '/api/leads?id=', desc: '删除咨询', auth: true },
    ],
  },
  {
    name: '图片库',
    endpoints: [
      { method: 'GET', path: '/api/gallery', desc: '获取图片列表 (?q=)' },
      { method: 'POST', path: '/api/upload', desc: '上传图片（multipart/form-data）', auth: true },
      { method: 'DELETE', path: '/api/gallery?id=', desc: '删除图片', auth: true },
    ],
  },
  {
    name: '站点设置 / SEO',
    endpoints: [
      { method: 'GET', path: '/api/settings', desc: '获取站点设置' },
      { method: 'PUT', path: '/api/settings', desc: '更新站点设置', auth: true },
    ],
  },
  {
    name: '首页 Banner',
    endpoints: [
      { method: 'GET', path: '/api/banners', desc: '获取 Banner 列表 (?id=)' },
      { method: 'POST', path: '/api/banners', desc: '新增 Banner', auth: true },
      { method: 'PUT', path: '/api/banners', desc: '编辑 Banner', auth: true },
      { method: 'DELETE', path: '/api/banners?id=', desc: '删除 Banner', auth: true },
    ],
  },
  {
    name: '客户评价',
    endpoints: [
      { method: 'GET', path: '/api/testimonials', desc: '获取评价列表 (?id=)' },
      { method: 'POST', path: '/api/testimonials', desc: '新增评价', auth: true },
      { method: 'PUT', path: '/api/testimonials', desc: '编辑评价', auth: true },
      { method: 'DELETE', path: '/api/testimonials?id=', desc: '删除评价', auth: true },
    ],
  },
  {
    name: 'FAQ',
    endpoints: [
      { method: 'GET', path: '/api/faqs', desc: '获取 FAQ 列表 (?id=)' },
      { method: 'POST', path: '/api/faqs', desc: '新增 FAQ', auth: true },
      { method: 'PUT', path: '/api/faqs', desc: '编辑 FAQ', auth: true },
      { method: 'DELETE', path: '/api/faqs?id=', desc: '删除 FAQ', auth: true },
    ],
  },
  {
    name: '团队成员',
    endpoints: [
      { method: 'GET', path: '/api/team', desc: '获取团队列表 (?id=)' },
      { method: 'POST', path: '/api/team', desc: '新增成员', auth: true },
      { method: 'PUT', path: '/api/team', desc: '编辑成员', auth: true },
      { method: 'DELETE', path: '/api/team?id=', desc: '删除成员', auth: true },
    ],
  },
  {
    name: '联系 / 关于',
    endpoints: [
      { method: 'GET', path: '/api/contact', desc: '获取联系信息' },
      { method: 'PUT', path: '/api/contact', desc: '更新联系信息', auth: true },
      { method: 'GET', path: '/api/about', desc: '获取关于信息' },
      { method: 'PUT', path: '/api/about', desc: '更新关于信息', auth: true },
    ],
  },
  {
    name: '活动日志',
    endpoints: [
      { method: 'GET', path: '/api/audit', desc: '获取日志 (?module= / ?action= / ?limit=)' },
      { method: 'DELETE', path: '/api/audit', desc: '清空日志', auth: true },
    ],
  },
  {
    name: '数据备份',
    endpoints: [
      { method: 'GET', path: '/api/backup', desc: '导出全量备份', auth: true },
      { method: 'POST', path: '/api/backup', desc: '导入备份', auth: true },
      { method: 'DELETE', path: '/api/backup', desc: '重置数据', auth: true },
    ],
  },
  {
    name: '统计 / 健康检查',
    endpoints: [
      { method: 'GET', path: '/api/stats', desc: '获取统计摘要' },
      { method: 'GET', path: '/api/health', desc: '健康检查 + KV 状态' },
    ],
  },
];

const methodTone = {
  GET: 'primary', POST: 'success', PUT: 'warning', DELETE: 'danger',
} as const;

export default function ApiDocsPage() {
  return (
    <div>
      <PageHeader title="API 文档" subtitle={`共 ${groups.reduce((acc, g) => acc + g.endpoints.length, 0)} 个端点`} />

      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        {groups.map((g) => (
          <div key={g.name}>
            <h2 style={{ fontSize: 17, fontWeight: 700, marginBottom: 12, paddingBottom: 8, borderBottom: '1px solid var(--c-border)' }}>
              {g.name}
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {g.endpoints.map((ep) => (
                <Card key={ep.method + ep.path} style={{ padding: '12px 18px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                    <Badge tone={methodTone[ep.method]}>{ep.method}</Badge>
                    <code style={{ fontSize: 14, color: 'var(--c-text)', fontFamily: 'ui-monospace, monospace' }}>{ep.path}</code>
                    <span style={{ fontSize: 13, color: 'var(--c-text-sec)', flex: 1 }}>{ep.desc}</span>
                    {ep.auth && <Badge tone="warning">需鉴权</Badge>}
                  </div>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>

      <Card style={{ marginTop: 24 }}>
        <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8 }}>鉴权说明</h3>
        <p style={{ fontSize: 13, color: 'var(--c-text-sec)', lineHeight: 1.6 }}>
          所有写接口（POST/PUT/DELETE）需登录管理员账号，由 <code style={{ color: 'var(--c-primary)' }}>middleware.ts</code> 自动校验 <code style={{ color: 'var(--c-primary)' }}>admin_token</code> Cookie。
          未授权请求会返回 <code style={{ color: '#ff6b6b' }}>401</code>。登录请访问 <code style={{ color: 'var(--c-primary)' }}>/admin/login</code>。
        </p>
      </Card>
    </div>
  );
}
