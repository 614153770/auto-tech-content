# 🤖 AI Tech Daily - 自动化技术内容站

> 由 AI 自动抓取、分析并生成技术内容的实验项目

## 📌 项目简介

这是一个全自动化的技术内容网站，每天自动：

- 🔥 抓取 GitHub Trending 热门项目
- 📰 收集技术新闻
- 💡 AI 分析生成学习心得
- 📊 生成周报和技术趋势分析

**网站地址：** https://614153770.github.io/auto-tech-content/

## ✨ 特色功能

- **全自动更新** - 每天北京时间 8:00 自动更新内容
- **AI 驱动** - 内容由 AI 分析生成，持续学习进化
- **开源透明** - 所有代码开源，欢迎 Fork 和改进
- **免费托管** - 使用 GitHub Pages 免费托管

## 🏗️ 项目结构

```
auto-tech-content/
├── index.html              # 网站首页
├── weekly/                 # 周报目录
├── projects/               # 项目推荐
├── tutorials/              # AI 生成教程
├── data/                   # 数据缓存
│   ├── github_trending.json
│   └── news_cache.json
├── scripts/                # 自动化脚本
│   ├── fetch_github.py     # 抓取 GitHub 数据
│   └── generate_content.py # 生成内容
└── .github/workflows/      # GitHub Actions
    └── auto-update.yml     # 定时更新任务
```

## 🚀 如何使用

### 查看网站

直接访问：https://614153770.github.io/auto-tech-content/

### 手动触发更新

1. 进入 Actions 页面
2. 选择 "Auto Update Content"
3. 点击 "Run workflow"

### 本地运行

```bash
# 安装依赖
pip install requests beautifulsoup4

# 抓取数据
cd scripts
python fetch_github.py

# 生成内容
python generate_content.py

# 本地预览（需要 Python 3）
cd ..
python -m http.server 8000
# 访问 http://localhost:8000
```

## 📅 更新计划

- [x] GitHub Trending 抓取
- [x] AI 内容生成
- [x] 定时自动更新
- [ ] 技术新闻抓取
- [ ] 邮件订阅功能
- [ ] 更多数据源接入

## 🎯 实验目标

1. 测试 AI 能否独立运营一个内容网站
2. 探索自动化内容生产的可行性
3. 积累流量后尝试变现（广告/订阅/赞助）

## 📝 注意事项

- 所有内容均由 AI 自动生成，仅供参考学习
- 数据来源于公开 API，遵守各平台使用条款
- 欢迎提出改进建议或贡献代码

## 📧 联系方式

- GitHub: https://github.com/614153770
- 问题反馈：请在 Issues 中提出

## 📄 License

MIT License

---

*本项目是一个实验性项目，旨在探索 AI 自动化内容生产的可能性*
