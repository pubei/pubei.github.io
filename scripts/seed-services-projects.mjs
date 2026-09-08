// 导入初始服务和案例数据到 Vercel KV
import { kv } from '@vercel/kv';

const services = [
  {
    name: '全屋定制',
    icon: '🏠',
    image: '/images/service-custom.jpg',
    summary: '从设计到施工，一站式全屋定制服务，打造理想家居空间。',
    description: '浦北装修设计提供专业全屋定制服务，涵盖空间规划、设计方案、材料选购、施工落地全流程。我们的设计师一对一服务，根据您的生活习惯和审美需求，量身定制专属方案。',
    features: ['免费量房设计', 'E0级环保板材', '工厂直供价格', '5年质保服务'],
    process: ['上门量房', '方案设计', '报价确认', '生产施工', '验收交付'],
    price: '￥800/㎡起',
  },
  {
    name: '新房装修',
    icon: '✨',
    image: '/images/service-new.jpg',
    summary: '专业新房装修，从毛坯到精装，打造温馨舒适的新家。',
    description: '新房装修是人生大事，浦北装修设计拥有10年+经验，为您提供从毛坯房到精装入住的全套服务。透明报价，无隐形消费，让您安心入住。',
    features: ['资深设计师一对一', '全程施工监理', '环保材料保障', '售后终身维护'],
    process: ['需求沟通', '设计方案', '预算报价', '施工管理', '竣工验收'],
    price: '￥600/㎡起',
  },
  {
    name: '旧房翻新',
    icon: '🔄',
    image: '/images/service-renovation.jpg',
    summary: '旧房焕新颜，专业翻新改造，让老房子重获新生。',
    description: '专业旧房翻新服务，针对老房结构特点制定改造方案，解决漏水、电路老化、空间布局不合理等问题，让旧房焕发新活力。',
    features: ['结构安全评估', '水电全改保障', '局部翻新方案', '施工不扰民'],
    process: ['现场勘察', '问题诊断', '改造方案', '施工执行', '完工验收'],
    price: '￥500/㎡起',
  },
  {
    name: '局部改造',
    icon: '🔧',
    image: '/images/service-partial.jpg',
    summary: '厨房、卫生间、阳台等局部空间改造，小改动大提升。',
    description: '不需要全屋翻新？局部改造服务帮您解决单个空间的痛点。厨房翻新、卫生间改造、阳台封闭等，专业团队高效完成。',
    features: ['单空间定制', '快速施工', '不影响其他区域', '性价比高'],
    process: ['空间测量', '方案设计', '材料选定', '局部施工', '清洁交付'],
    price: '￥3000起',
  },
  {
    name: '软装配饰',
    icon: '🛋️',
    image: '/images/service-soft.jpg',
    summary: '专业软装搭配，家具、窗帘、灯饰、画品一站式配齐。',
    description: '软装是家居的灵魂。我们的软装设计师根据整体风格，为您搭配家具、窗帘、灯饰、装饰画等，让空间更有温度和品味。',
    features: ['风格统一搭配', '工厂直采价格', '免费摆场服务', '品质保障'],
    process: ['风格定位', '选配方案', '采购定制', '上门摆场', '效果调整'],
    price: '￥200/㎡起',
  },
  {
    name: '智能家居',
    icon: '📱',
    image: '/images/service-smart.jpg',
    summary: '智能灯光、安防、家电控制，打造科技感智慧家居。',
    description: '智能家居系统集成，包括智能照明、安防监控、家电联动、环境控制等，让您的家更智能、更便捷、更安全。',
    features: ['全屋智能方案', '品牌设备直供', '专业安装调试', '远程技术支持'],
    process: ['需求评估', '系统设计', '设备选型', '安装调试', '使用培训'],
    price: '￥10000起',
  },
  {
    name: '水电改造',
    icon: '⚡',
    image: '/images/service-electrical.jpg',
    summary: '专业水电改造，规范施工，安全可靠，经久耐用。',
    description: '水电是家装的隐蔽工程，质量至关重要。我们采用国标材料，规范施工工艺，走管横平竖直，强弱电分离，确保安全耐用。',
    features: ['国标电线水管', '规范施工工艺', '50年质保', '免费售后维修'],
    process: ['现场定位', '开槽布管', '穿线接管', '打压测试', '封槽保护'],
    price: '￥80/㎡起',
  },
  {
    name: '监理服务',
    icon: '👷',
    image: '/images/service-supervision.jpg',
    summary: '第三方装修监理，全程把控质量，为您的装修保驾护航。',
    description: '专业装修监理服务，独立第三方立场，对施工质量、材料、进度、造价进行全程监督，保障您的装修权益。',
    features: ['独立第三方', '关键节点验收', '质量问题追责', '造价审核'],
    process: ['合同审核', '材料验收', '节点检查', '竣工验收', '售后跟进'],
    price: '￥50/㎡起',
  },
];

const projects = [
  {
    name: '现代简约三居室',
    category: '全屋定制',
    image: '/images/news-bg-1.svg',
    gallery: ['/images/news-bg-1.svg', '/images/news-bg-2.svg', '/images/news-bg-3.svg'],
    location: '浦北县·金浦新区',
    area: '120㎡',
    duration: '90天',
    description: '为年轻夫妻打造的现代简约风格三居室，以黑白灰为主色调，搭配原木色家具，营造简洁温馨的居住氛围。开放式厨房与客厅相连，空间通透大气。',
  },
  {
    name: '新中式四居室',
    category: '全屋定制',
    image: '/images/news-bg-2.svg',
    gallery: ['/images/news-bg-2.svg', '/images/news-bg-3.svg', '/images/news-bg-4.svg'],
    location: '浦北县·越秀大道',
    area: '160㎡',
    duration: '120天',
    description: '传承东方美学的新中式风格，将传统元素与现代设计完美融合。实木家具搭配水墨画装饰，营造典雅内敛的东方韵味。',
  },
  {
    name: '北欧风两居室',
    category: '新房装修',
    image: '/images/news-bg-3.svg',
    gallery: ['images/news-bg-3.svg', '/images/news-bg-4.svg', '/images/news-bg-1.svg'],
    location: '浦北县·商业街',
    area: '89㎡',
    duration: '75天',
    description: '清新自然的北欧风格，大量使用白色和原木色，搭配绿植和布艺软装，打造明亮通透、温馨舒适的小家。',
  },
  {
    name: '轻奢大平层',
    category: '全屋定制',
    image: '/images/news-bg-4.svg',
    gallery: ['/images/news-bg-4.svg', '/images/news-bg-1.svg', '/images/news-bg-2.svg'],
    location: '浦北县·江滨东路',
    area: '180㎡',
    duration: '150天',
    description: '现代轻奢风格大平层，金属线条与大理石材质的碰撞，营造低调奢华的品质生活。',
  },
  {
    name: '老旧小区翻新',
    category: '旧房翻新',
    image: '/images/news-bg-1.svg',
    gallery: ['/images/news-bg-1.svg', '/images/news-bg-3.svg', '/images/news-bg-4.svg'],
    location: '浦北县·解放路',
    area: '95㎡',
    duration: '60天',
    description: '20年老旧小区翻新，全面更换水电管线，重新规划空间布局，让老房子焕发新生。',
  },
  {
    name: '小户型智慧家',
    category: '智能家居',
    image: '/images/news-bg-2.svg',
    gallery: ['/images/news-bg-2.svg', '/images/news-bg-4.svg', '/images/news-bg-1.svg'],
    location: '浦北县·城南区',
    area: '65㎡',
    duration: '45天',
    description: '小户型全屋智能改造，智能照明、安防、家电一体化控制，让小空间也有大智慧。',
  },
];

const now = Date.now();

const serviceItems = services.map((s, i) => ({
  id: `svc_seed_${i}`,
  ...s,
  createdAt: now - i * 1000,
  updatedAt: now,
}));

const projectItems = projects.map((p, i) => ({
  id: `proj_seed_${i}`,
  ...p,
  createdAt: now - i * 1000,
  updatedAt: now,
}));

console.log(`准备导入 ${serviceItems.length} 个服务和 ${projectItems.length} 个案例...`);

await kv.set('service:all', serviceItems);
await kv.set('project:all', projectItems);

console.log(`✓ 成功导入 ${serviceItems.length} 个服务`);
console.log(`✓ 成功导入 ${projectItems.length} 个案例`);

// 验证
const svcCount = (await kv.get('service:all')).length;
const projCount = (await kv.get('project:all')).length;
console.log(`✓ 验证: 服务 ${svcCount} 个，案例 ${projCount} 个`);
