# Pulbei Glass Site - Pull Request

这是将 feature/glass-site 分支上的完整项目（包含前端与后端示例）合并到仓库默认分支的 Pull Request。

说明：
- 包含文件：README.md, package.json, data.json, server.js, public/ 下的静态前端文件等。
- 注意点：
  - 因为项目包含 Node.js 后端（server.js），如果你打算在 GitHub Pages 上托管，请仅合并 public/ 内容或设置相应的部署流程。
  - data.json 中包含演示数据；上线前请移除敏感信息并将 data.json 加入 .gitignore，或改用数据库。
  - 请在合并前确认仓库默认分支（main/master）以及是否需要我把 data.json 从合并中排除。

操作建议：
- 如果你确定要合并到默认分支，我将创建 PR，标题为："Merge feature/glass-site: add glassmorphism site"，并提供简短说明。
- 或者，我可以先创建一个草稿 PR 供你审阅，再由你决定何时合并。
