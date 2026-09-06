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
