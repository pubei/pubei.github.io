// KV 存储层 - 使用 Vercel KV，无环境变量时回退到内存存储
import { kv } from '@vercel/kv';
import type {
  NewsItem, ServiceItem, ProjectItem, ContactInfo, AboutInfo,
  Lead, GalleryItem, SiteSettings, Banner, Testimonial, FAQItem, TeamMember, AuditLog, BackupData,
} from './types';

const hasKV = !!(process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN);

// 内存回退存储
const memoryStore: Record<string, any> = {};

async function kvGet<T>(key: string): Promise<T | null> {
  if (hasKV) {
    try {
      return await kv.get<T>(key);
    } catch {
      return null;
    }
  }
  return (memoryStore[key] as T) || null;
}

async function kvSet(key: string, value: any): Promise<void> {
  if (hasKV) {
    await kv.set(key, value);
    return;
  }
  memoryStore[key] = value;
}

async function kvDel(key: string): Promise<void> {
  if (hasKV) {
    await kv.del(key);
    return;
  }
  delete memoryStore[key];
}

// 新闻
export async function getAllNews(): Promise<NewsItem[]> {
  const news = await kvGet<NewsItem[]>('news:all');
  return news || [];
}

export async function getNewsList(page = 1, pageSize = 10, includeUnpublished = false) {
  const all = await getAllNews();
  let list = includeUnpublished ? all : all.filter((n) => n.published);
  list = list.sort((a, b) => b.createdAt - a.createdAt);
  const total = list.length;
  const start = (page - 1) * pageSize;
  const data = list.slice(start, start + pageSize);
  return { data, total, page, pageSize };
}

export async function getNewsById(id: string): Promise<NewsItem | null> {
  const all = await getAllNews();
  return all.find((n) => n.id === id) || null;
}

export async function createNews(data: Omit<NewsItem, 'createdAt' | 'updatedAt'> & { id?: string }): Promise<NewsItem> {
  const all = await getAllNews();
  const item: NewsItem = {
    ...data,
    id: data.id || `news_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.unshift(item);
  await kvSet('news:all', all);
  return item;
}

export async function updateNews(id: string, data: Partial<NewsItem>): Promise<NewsItem | null> {
  const all = await getAllNews();
  const idx = all.findIndex((n) => n.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('news:all', all);
  return all[idx];
}

export async function deleteNews(id: string): Promise<boolean> {
  const all = await getAllNews();
  const filtered = all.filter((n) => n.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('news:all', filtered);
  return true;
}

// 服务
export async function getAllServices(): Promise<ServiceItem[]> {
  const services = await kvGet<ServiceItem[]>('service:all');
  return services || [];
}

export async function getServiceById(id: string): Promise<ServiceItem | null> {
  const all = await getAllServices();
  return all.find((s) => s.id === id) || null;
}

export async function createService(data: Omit<ServiceItem, 'createdAt' | 'updatedAt'> & { id?: string }): Promise<ServiceItem> {
  const all = await getAllServices();
  const item: ServiceItem = {
    ...data,
    id: data.id || `svc_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.unshift(item);
  await kvSet('service:all', all);
  return item;
}

export async function updateService(id: string, data: Partial<ServiceItem>): Promise<ServiceItem | null> {
  const all = await getAllServices();
  const idx = all.findIndex((s) => s.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('service:all', all);
  return all[idx];
}

export async function deleteService(id: string): Promise<boolean> {
  const all = await getAllServices();
  const filtered = all.filter((s) => s.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('service:all', filtered);
  return true;
}

// 案例
export async function getAllProjects(): Promise<ProjectItem[]> {
  const projects = await kvGet<ProjectItem[]>('project:all');
  return projects || [];
}

export async function getProjectById(id: string): Promise<ProjectItem | null> {
  const all = await getAllProjects();
  return all.find((p) => p.id === id) || null;
}

export async function createProject(data: Omit<ProjectItem, 'createdAt' | 'updatedAt'> & { id?: string }): Promise<ProjectItem> {
  const all = await getAllProjects();
  const item: ProjectItem = {
    ...data,
    id: data.id || `proj_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.unshift(item);
  await kvSet('project:all', all);
  return item;
}

export async function updateProject(id: string, data: Partial<ProjectItem>): Promise<ProjectItem | null> {
  const all = await getAllProjects();
  const idx = all.findIndex((p) => p.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('project:all', all);
  return all[idx];
}

export async function deleteProject(id: string): Promise<boolean> {
  const all = await getAllProjects();
  const filtered = all.filter((p) => p.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('project:all', filtered);
  return true;
}

// 联系信息
const defaultContact: ContactInfo = {
  phone: '134-1227-7880',
  email: 'contact@pboo.top',
  address: '广西壮族自治区钦州市浦北县',
  wechat: 'pubei-design',
  hours: '周一至周日 8:00 - 20:00',
};

export async function getContactInfo(): Promise<ContactInfo> {
  const info = await kvGet<ContactInfo>('contact:info');
  return info || defaultContact;
}

export async function updateContactInfo(data: Partial<ContactInfo>): Promise<ContactInfo> {
  const current = await getContactInfo();
  const updated = { ...current, ...data };
  await kvSet('contact:info', updated);
  return updated;
}

// 关于信息
const defaultAbout: AboutInfo = {
  intro: '浦北装修设计，深耕本地装修行业多年，专注全屋定制、空间设计与施工落地。我们以匠心精神为每一位客户打造理想居所。',
  vision: '成为浦北地区最受信赖的装修设计品牌，让每一个家都成为艺术。',
  stats: [
    { label: '服务客户', value: '500+' },
    { label: '完成项目', value: '300+' },
    { label: '专业团队', value: '50+' },
    { label: '行业经验', value: '10年' },
  ],
  commitments: [
    '100% 透明报价，无隐形消费',
    '环保材料，健康居家',
    '专业设计师一对一服务',
    '售后保障，终身维护',
  ],
  history: [
    { year: '2014', event: '浦北装修设计工作室成立' },
    { year: '2017', event: '组建专业设计团队，服务客户突破100家' },
    { year: '2020', event: '引入全屋定制生产线，实现设计施工一体化' },
    { year: '2024', event: '累计服务500+家庭，成为本地知名装修品牌' },
  ],
};

export async function getAboutInfo(): Promise<AboutInfo> {
  const info = await kvGet<AboutInfo>('about:info');
  return info || defaultAbout;
}

export async function updateAboutInfo(data: Partial<AboutInfo>): Promise<AboutInfo> {
  const current = await getAboutInfo();
  const updated = { ...current, ...data };
  await kvSet('about:info', updated);
  return updated;
}

// 统计数据
export async function getStats() {
  const [news, services, projects, leads, gallery, testimonials, banners, faqs, team] = await Promise.all([
    getAllNews(),
    getAllServices(),
    getAllProjects(),
    getAllLeads(),
    getAllGallery(),
    getAllTestimonials(),
    getAllBanners(),
    getAllFAQs(),
    getAllTeam(),
  ]);
  return {
    totalNews: news.length,
    publishedNews: news.filter((n) => n.published).length,
    totalServices: services.length,
    totalProjects: projects.length,
    totalLeads: leads.length,
    newLeads: leads.filter((l) => l.status === 'new').length,
    totalGallery: gallery.length,
    totalTestimonials: testimonials.length,
    totalBanners: banners.length,
    totalFAQs: faqs.length,
    totalTeam: team.length,
  };
}

// KV 状态检测（用于健康检查）
export async function getKVStatus(): Promise<{ connected: boolean; mode: 'kv' | 'memory' }> {
  if (!hasKV) return { connected: true, mode: 'memory' };
  try {
    await kv.get('__health_check__');
    return { connected: true, mode: 'kv' };
  } catch {
    return { connected: false, mode: 'kv' };
  }
}

// 备份：导出所有数据
export async function exportAll(): Promise<BackupData> {
  const keys = [
    'news:all', 'service:all', 'project:all', 'contact:info', 'about:info',
    'lead:all', 'image:gallery', 'settings:site', 'banner:all',
    'testimonial:all', 'faq:all', 'team:all', 'audit:log',
  ];
  const data: Record<string, any> = {};
  for (const k of keys) {
    if (hasKV) {
      try { data[k] = await kv.get(k); } catch { /* skip */ }
    } else {
      data[k] = memoryStore[k] ?? null;
    }
  }
  return { version: '1.0', exportedAt: Date.now(), data };
}

// 备份：导入恢复
export async function importAll(backup: BackupData): Promise<void> {
  if (!backup || !backup.data) throw new Error('备份文件格式错误');
  for (const [k, v] of Object.entries(backup.data)) {
    if (v === null || v === undefined) continue;
    await kvSet(k, v);
  }
}

// 备份：清空所有数据（危险操作）
export async function resetAll(): Promise<void> {
  const keys = [
    'news:all', 'service:all', 'project:all', 'lead:all', 'image:gallery',
    'settings:site', 'banner:all', 'testimonial:all', 'faq:all', 'team:all', 'audit:log',
  ];
  for (const k of keys) await kvDel(k);
}

// ============== 客户咨询 (leads) ==============
export async function getAllLeads(): Promise<Lead[]> {
  return (await kvGet<Lead[]>('lead:all')) || [];
}
export async function getLeadById(id: string): Promise<Lead | null> {
  const all = await getAllLeads();
  return all.find((l) => l.id === id) || null;
}
export async function createLead(data: Omit<Lead, 'id' | 'createdAt' | 'updatedAt'> & { id?: string }): Promise<Lead> {
  const all = await getAllLeads();
  const item: Lead = {
    ...data,
    id: data.id || `lead_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.unshift(item);
  await kvSet('lead:all', all);
  return item;
}
export async function updateLead(id: string, data: Partial<Lead>): Promise<Lead | null> {
  const all = await getAllLeads();
  const idx = all.findIndex((l) => l.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('lead:all', all);
  return all[idx];
}
export async function deleteLead(id: string): Promise<boolean> {
  const all = await getAllLeads();
  const filtered = all.filter((l) => l.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('lead:all', filtered);
  return true;
}

// ============== 图库 (gallery) ==============
export async function getAllGallery(): Promise<GalleryItem[]> {
  return (await kvGet<GalleryItem[]>('image:gallery')) || [];
}
export async function addGalleryItem(item: GalleryItem): Promise<void> {
  const all = await getAllGallery();
  all.unshift(item);
  await kvSet('image:gallery', all.slice(0, 200));
}
export async function deleteGalleryItem(id: string): Promise<boolean> {
  const all = await getAllGallery();
  const filtered = all.filter((g) => g.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('image:gallery', filtered);
  return true;
}

// ============== 站点设置 (settings) ==============
const defaultSettings: SiteSettings = {
  metaTitle: '浦北装修设计 - 专业全屋定制 / 新房装修 / 旧房翻新',
  metaDescription: '浦北装修设计深耕本地装修行业多年，专注全屋定制、空间设计与施工落地。10年行业经验，500+服务家庭，环保材料，透明报价。',
  metaKeywords: '浦北装修,全屋定制,新房装修,旧房翻新,装修设计,软装配饰,智能家居',
  ogImage: '',
  favicon: '/favicon.ico',
  analyticsCode: '',
  icp: '',
  social: [
    { label: '微信公众号', url: '#', icon: 'wechat' },
    { label: '电话咨询', url: 'tel:134-1227-7880', icon: 'phone' },
  ],
  announcement: '🎉 浦北装修设计秋季优惠活动进行中，全屋定制 8 折起！',
  announcementEnabled: false,
  updatedAt: Date.now(),
};
export async function getSettings(): Promise<SiteSettings> {
  return (await kvGet<SiteSettings>('settings:site')) || defaultSettings;
}
export async function updateSettings(data: Partial<SiteSettings>): Promise<SiteSettings> {
  const current = await getSettings();
  const updated = { ...current, ...data, updatedAt: Date.now() };
  await kvSet('settings:site', updated);
  return updated;
}

// ============== Banner ==============
export async function getAllBanners(): Promise<Banner[]> {
  return (await kvGet<Banner[]>('banner:all')) || [];
}
export async function getBannerById(id: string): Promise<Banner | null> {
  const all = await getAllBanners();
  return all.find((b) => b.id === id) || null;
}
export async function createBanner(data: Omit<Banner, 'id' | 'createdAt' | 'updatedAt'> & { id?: string }): Promise<Banner> {
  const all = await getAllBanners();
  const item: Banner = {
    ...data,
    id: data.id || `banner_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.push(item);
  await kvSet('banner:all', all);
  return item;
}
export async function updateBanner(id: string, data: Partial<Banner>): Promise<Banner | null> {
  const all = await getAllBanners();
  const idx = all.findIndex((b) => b.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('banner:all', all);
  return all[idx];
}
export async function deleteBanner(id: string): Promise<boolean> {
  const all = await getAllBanners();
  const filtered = all.filter((b) => b.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('banner:all', filtered);
  return true;
}

// ============== 客户评价 (testimonials) ==============
export async function getAllTestimonials(): Promise<Testimonial[]> {
  return (await kvGet<Testimonial[]>('testimonial:all')) || [];
}
export async function getTestimonialById(id: string): Promise<Testimonial | null> {
  const all = await getAllTestimonials();
  return all.find((t) => t.id === id) || null;
}
export async function createTestimonial(data: Omit<Testimonial, 'id' | 'createdAt' | 'updatedAt'> & { id?: string }): Promise<Testimonial> {
  const all = await getAllTestimonials();
  const item: Testimonial = {
    ...data,
    id: data.id || `tst_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.push(item);
  await kvSet('testimonial:all', all);
  return item;
}
export async function updateTestimonial(id: string, data: Partial<Testimonial>): Promise<Testimonial | null> {
  const all = await getAllTestimonials();
  const idx = all.findIndex((t) => t.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('testimonial:all', all);
  return all[idx];
}
export async function deleteTestimonial(id: string): Promise<boolean> {
  const all = await getAllTestimonials();
  const filtered = all.filter((t) => t.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('testimonial:all', filtered);
  return true;
}

// ============== FAQ ==============
export async function getAllFAQs(): Promise<FAQItem[]> {
  return (await kvGet<FAQItem[]>('faq:all')) || [];
}
export async function getFAQById(id: string): Promise<FAQItem | null> {
  const all = await getAllFAQs();
  return all.find((f) => f.id === id) || null;
}
export async function createFAQ(data: Omit<FAQItem, 'id' | 'createdAt' | 'updatedAt'> & { id?: string }): Promise<FAQItem> {
  const all = await getAllFAQs();
  const item: FAQItem = {
    ...data,
    id: data.id || `faq_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.push(item);
  await kvSet('faq:all', all);
  return item;
}
export async function updateFAQ(id: string, data: Partial<FAQItem>): Promise<FAQItem | null> {
  const all = await getAllFAQs();
  const idx = all.findIndex((f) => f.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('faq:all', all);
  return all[idx];
}
export async function deleteFAQ(id: string): Promise<boolean> {
  const all = await getAllFAQs();
  const filtered = all.filter((f) => f.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('faq:all', filtered);
  return true;
}

// ============== 团队 (team) ==============
export async function getAllTeam(): Promise<TeamMember[]> {
  return (await kvGet<TeamMember[]>('team:all')) || [];
}
export async function getTeamMemberById(id: string): Promise<TeamMember | null> {
  const all = await getAllTeam();
  return all.find((m) => m.id === id) || null;
}
export async function createTeamMember(data: Omit<TeamMember, 'id' | 'createdAt' | 'updatedAt'> & { id?: string }): Promise<TeamMember> {
  const all = await getAllTeam();
  const item: TeamMember = {
    ...data,
    id: data.id || `tm_${Date.now()}`,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  all.push(item);
  await kvSet('team:all', all);
  return item;
}
export async function updateTeamMember(id: string, data: Partial<TeamMember>): Promise<TeamMember | null> {
  const all = await getAllTeam();
  const idx = all.findIndex((m) => m.id === id);
  if (idx === -1) return null;
  all[idx] = { ...all[idx], ...data, updatedAt: Date.now() };
  await kvSet('team:all', all);
  return all[idx];
}
export async function deleteTeamMember(id: string): Promise<boolean> {
  const all = await getAllTeam();
  const filtered = all.filter((m) => m.id !== id);
  if (filtered.length === all.length) return false;
  await kvSet('team:all', filtered);
  return true;
}

// ============== 活动日志 (audit) ==============
export async function getAuditLogs(limit = 100): Promise<AuditLog[]> {
  const all = (await kvGet<AuditLog[]>('audit:log')) || [];
  return all.slice(0, limit);
}
export async function appendAuditLog(log: AuditLog): Promise<void> {
  const all = (await kvGet<AuditLog[]>('audit:log')) || [];
  all.unshift(log);
  // 仅保留最近 500 条
  await kvSet('audit:log', all.slice(0, 500));
}
export async function clearAuditLogs(): Promise<void> {
  await kvSet('audit:log', []);
}

