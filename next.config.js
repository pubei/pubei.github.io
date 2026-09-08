/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'trae-api-cn.mchost.guru' },
      { protocol: 'https', hostname: 'pboo.top' },
      { protocol: 'https', hostname: 'images.unsplash.com' },
    ],
  },
  async rewrites() {
    return [
      // 静态页面 clean URL 重写
      { source: '/', destination: '/index.html' },
      { source: '/about', destination: '/about.html' },
      { source: '/news', destination: '/news.html' },
      { source: '/news-detail', destination: '/news-detail.html' },
      { source: '/services', destination: '/services.html' },
      { source: '/projects', destination: '/projects.html' },
      { source: '/contact', destination: '/contact.html' },
      { source: '/faq', destination: '/faq.html' },
      { source: '/privacy', destination: '/privacy.html' },
      { source: '/terms', destination: '/terms.html' },
      { source: '/sitemap', destination: '/sitemap.html' },
      { source: '/project-detail-:id', destination: '/project-detail-:id.html' },
      { source: '/service-detail-:id', destination: '/service-detail-:id.html' },
    ];
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
