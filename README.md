# 浦北装修设计公司 - 玻璃风样例网站

说明
- 这是一个示例项目，展示玻璃风（Glassmorphism）公司官网页面与简单后端 API。
- 包含页面：index, about, services, projects, contact, admin。
- 后端：Node.js + Express，提供 /api/projects、/api/contact、/api/login、/api/messages 等接口。
- 数据持久化到 data.json（演示用途）。

运行
1. 安装依赖
   npm install

2. 启动服务
   npm start

3. 在浏览器打开
   http://localhost:3000

默认管理账号（测试用）
- 密码: admin123
- 登录后可以添加作品与查看留言（示例实现用静态 token；生产请用真实认证）。

拓展建议
- 使用数据库（Postgres/Mongo）替代 data.json。
- 加入真实认证（JWT + bcrypt）。
- 添加图片上传、CMS 管理页面、表单验证、SEO 优化。
