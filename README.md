# PM OS - 项目管理操作系统

一个完整的项目管理系统，包含任务管理、团队协作、AI智能推荐、风险预警、资源分配优化等功能。

## 🚀 快速部署

### 方式一：Vercel（推荐）
1. 访问 [https://vercel.com](https://vercel.com)
2. 导入此项目仓库
3. 自动部署，无需配置

### 方式二：Netlify
1. 访问 [https://netlify.com](https://netlify.com)
2. 拖拽此文件夹到页面
3. 自动部署

### 方式三：GitHub Pages
1. 设置仓库为 GitHub Pages
2. 选择 `/ (root)` 作为源目录
3. 访问 `https://你的用户名.github.io/仓库名`

## 🔧 本地运行

```bash
# 使用Python
python -m http.server 8000

# 使用Node.js serve
npx serve .

# 或直接双击 index.html 文件
```

## 📁 项目结构

```
web/
├── index.html          # 主应用文件
├── lucide.min.js       # 图标库（本地化）
├── vercel.json         # Vercel部署配置
├── netlify.toml        # Netlify部署配置
└── README.md           # 说明文档
```

## ⚡ 功能特性

- ✅ 任务管理与跟踪
- ✅ 团队协作与沟通
- ✅ AI智能推荐系统
- ✅ 风险预警与监控
- ✅ 语音输入与AI对话
- ✅ 响应式设计（支持移动端）
- ✅ 深色/浅色主题切换
- ✅ 数据持久化（本地存储）

## 🔒 安全性说明

- 所有敏感数据存储在浏览器本地
- 无后端服务器，无数据库连接
- AI功能需要用户自行配置API密钥
- 支持离线使用基础功能

## 📞 技术支持

如遇问题，请检查：
1. 浏览器控制台是否有错误
2. 网络连接是否正常
3. API密钥配置是否正确

## 📄 许可证

MIT License - 详见项目根目录 LICENSE 文件