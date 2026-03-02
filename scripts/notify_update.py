#!/usr/bin/env python3
"""
发送首次数据更新成功通知
"""

import requests
from datetime import datetime

SENDKEY = "SCT317686TjoxF0q9tBMkRPd6AvhWR5v1G"

def send_wechat(title, content):
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    params = {"title": title, "desp": content}
    try:
        response = requests.get(url, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"code": -1, "error": str(e)}

def main():
    content = f"""
🎉 **首次数据更新成功！**

━━━━━━━━━━━━━━━━

📊 **已抓取 10 个 GitHub Trending 热门项目**

**Top 5 项目：**

1️⃣ **moeru-ai/airi** (TypeScript)
   ⭐ 20,445 | AI 虚拟伴侣项目

2️⃣ **ruvnet/wifi-densepose** (Rust)
   ⭐ 18,182 | WiFi 信号人体姿态识别

3️⃣ **ruvnet/ruflo** (TypeScript)
   ⭐ 17,400 | Claude AI 智能体编排平台

4️⃣ **microsoft/markitdown** (Python)
   ⭐ 89,077 | 微软文档转 Markdown 工具

5️⃣ **bytedance/deer-flow** (Python)
   ⭐ 23,072 | 字节开源 SuperAgent 框架

━━━━━━━━━━━━━━━━

💡 **AI 技术趋势分析**

今日热门语言分布：
- 🐍 Python: 6 个项目
- 📘 TypeScript: 2 个项目
- 🦀 Rust: 1 个项目
- 🐚 Shell: 1 个项目

**AI 观察：**
- AI/ML 相关工具库持续火热
- 智能体 (Agent) 项目受到广泛关注
- 开发者工具和生产效率类项目表现突出

━━━━━━━━━━━━━━━━

🌐 **查看方式**

**周报（已生成）：**
https://614153770.github.io/auto-tech-content/weekly/2026-w10.html

**GitHub 仓库：**
https://github.com/614153770/auto-tech-content

**网站首页：**
https://614153770.github.io/auto-tech-content/
(可能需要刷新几次清除缓存)

━━━━━━━━━━━━━━━━

✅ **下次自动更新**
明天（3 月 3 日）早上 8:00
GitHub Actions 会自动执行更新

━━━━━━━━━━━━━━━━

✅ 小明同学 | AI 助手
"""
    
    result = send_wechat("🎉 首次数据更新成功！", content)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if result.get("code") == 0:
        print(f"[{timestamp}] 通知发送成功")
    else:
        print(f"[{timestamp}] 通知发送失败：{result}")

if __name__ == "__main__":
    main()
