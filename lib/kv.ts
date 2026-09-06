// KV 存储层 - 使用 Vercel KV，无环境变量时回退到内存存储
import { kv } from '@vercel/kv';
import type { NewsItem, ServiceItem, ProjectItem, ContactInfo, AboutInfo } from './types';

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
  const [news, services, projects] = await Promise.all([
    getAllNews(),
    getAllServices(),
    getAllProjects(),
  ]);
  return {
    totalNews: news.length,
    publishedNews: news.filter((n) => n.published).length,
    totalServices: services.length,
    totalProjects: projects.length,
  };
}
