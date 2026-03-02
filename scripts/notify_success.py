#!/usr/bin/env python3
"""
发送网站上线通知
"""

import requests
from datetime import datetime

SENDKEY = "SCT317686TjoxF0q9tBMkRPd6AvhWR5v1G"

def send_wechat(title, content):
    """发送微信通知"""
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    params = {"title": title, "desp": content}
    try:
        response = requests.get(url, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"code": -1, "error": str(e)}

def main():
    content = f"""
🎉 **GitHub Pages 网站搭建成功！**

━━━━━━━━━━━━━━━━

🌐 **网站信息**

**网站地址：** https://614153770.github.io/auto-tech-content/

**GitHub 仓库：** https://github.com/614153770/auto-tech-content

**部署状态：** 正在部署中（通常 1-3 分钟）

━━━━━━━━━━━━━━━━

📋 **已配置功能**

✅ 网站前端页面（美观响应式设计）
✅ GitHub Trending 数据抓取脚本
✅ AI 内容自动生成脚本
✅ GitHub Actions 定时任务（每天 8:00 自动更新）
✅ 自动 commit 和推送

━━━━━━━━━━━━━━━━

⏰ **自动更新时间**

- **每日更新：** 北京时间 8:00
- **更新内容：** 
  - GitHub Trending 热门项目
  - AI 生成的技术趋势分析
  - 学习心得和周报

━━━━━━━━━━━━━━━━

🔧 **下一步**

1. **等待部署完成**（1-3 分钟后刷新网站）
2. **查看网站效果**
3. **如需调整，告诉我即可**

━━━━━━━━━━━━━━━━

💡 **说明**

- 首次内容将在首次自动更新后生成
- 当前显示的是占位内容
- 明天早上 8 点后会有完整的自动更新内容

━━━━━━━━━━━━━━━━

✅ 小明同学 | AI 助手
"""
    
    result = send_wechat("🎉 GitHub Pages 网站搭建成功！", content)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if result.get("code") == 0:
        print(f"[{timestamp}] 通知发送成功 - 微信")
    else:
        print(f"[{timestamp}] 通知发送失败：{result}")

if __name__ == "__main__":
    main()
