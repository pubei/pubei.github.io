// 数据模型类型定义

export interface NewsItem {
  id: string;
  date: string;
  category: string;
  title: string;
  image: string;
  image_fallback?: string;
  excerpt: string;
  content: string[];
  published: boolean;
  createdAt: number;
  updatedAt: number;
}

export interface ServiceItem {
  id: string;
  name: string;
  icon: string;
  image: string;
  description: string;
  features: string[];
  process: string[];
  order: number;
  createdAt: number;
  updatedAt: number;
}

export interface ProjectItem {
  id: string;
  name: string;
  style: string;
  layout: string;
  area: string;
  address: string;
  images: string[];
  cover: string;
  description: string;
  order: number;
  createdAt: number;
  updatedAt: number;
}

export interface ContactInfo {
  phone: string;
  email: string;
  address: string;
  wechat: string;
  hours: string;
  lat?: string;
  lng?: string;
}

export interface AboutInfo {
  intro: string;
  vision: string;
  stats: { label: string; value: string }[];
  commitments: string[];
  history: { year: string; event: string }[];
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  total?: number;
}

// ============== 新增多功能后端类型 ==============

// 客户咨询 / 预约线索
export type LeadStatus = 'new' | 'following' | 'won' | 'lost' | 'archived';
export interface Lead {
  id: string;
  name: string;
  phone: string;
  email?: string;
  service: string;       // 意向服务
  area?: string;          // 房屋面积
  budget?: string;        // 预算
  appointmentTime?: string; // 期望装修时间
  message?: string;       // 备注/需求
  source?: string;        // 来源（如：首页弹窗、contact 页、手动录入）
  status: LeadStatus;
  notes: { at: number; content: string }[]; // 跟进记录
  order: number;
  createdAt: number;
  updatedAt: number;
}

// 图库项（复用 /api/upload 已存的 image:gallery 数据）
export interface GalleryItem {
  id: string;
  type: string;
  size: number;
  name: string;
  url: string;
  tags?: string[];
  createdAt: number;
}

// 站点设置 / SEO
export interface SiteSettings {
  metaTitle: string;
  metaDescription: string;
  metaKeywords: string;
  ogImage: string;
  favicon: string;
  analyticsCode: string;   // 统计代码（如百度统计、Google Analytics）
  icp: string;             // 备案号
  social: { label: string; url: string; icon: string }[];
  announcement: string;    // 顶部公告条
  announcementEnabled: boolean;
  updatedAt: number;
}

// 首页 Banner
export interface Banner {
  id: string;
  title: string;
  subtitle: string;
  image: string;
  link: string;
  ctaText: string;         // 按钮文字
  order: number;
  enabled: boolean;
  createdAt: number;
  updatedAt: number;
}

// 客户评价
export interface Testimonial {
  id: string;
  customer: string;
  project: string;
  rating: number;          // 1-5
  content: string;
  avatar: string;
  order: number;
  enabled: boolean;
  createdAt: number;
  updatedAt: number;
}

// FAQ
export interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
  order: number;
  enabled: boolean;
  createdAt: number;
  updatedAt: number;
}

// 团队成员
export interface TeamMember {
  id: string;
  name: string;
  role: string;
  avatar: string;
  bio: string;
  skills: string[];
  order: number;
  enabled: boolean;
  createdAt: number;
  updatedAt: number;
}

// 活动日志
export interface AuditLog {
  id: string;
  action: string;          // create / update / delete / login / logout / export / import
  module: string;          // news / lead / settings ...
  target: string;          // 操作对象 id 或名称
  detail?: string;
  ip?: string;
  at: number;
}

// 数据备份结构
export interface BackupData {
  version: string;
  exportedAt: number;
  data: Record<string, any>;
}

