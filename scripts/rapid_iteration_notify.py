#!/usr/bin/env python3
"""
快速迭代通知
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

def send_iteration_notification(version, feature, status="success"):
    """发送迭代通知"""
    if status == "success":
        content = f"""
🚀 **AI Tech Daily 快速迭代**

━━━━━━━━━━━━━━━━

📦 **版本：** v{version}
⏰ **时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ **状态：** 验证成功

━━━━━━━━━━━━━━━━

✨ **新功能：** {feature}

━━━━━━━━━━━━━━━━

🔄 **迭代计划：**
- 周期：每 10 分钟一个版本
- 持续时间：2 小时（15:00-17:00）
- 目标：12 个新功能

━━━━━━━━━━━━━━━━

🌐 **立即体验：**
https://614153770.github.io/auto-tech-content/

━━━━━━━━━━━━━━━━

📋 **已完成版本：**
1. ✅ v2026.0302.1500 - 项目搜索功能
2. ✅ v{version} - {feature}

━━━━━━━━━━━━━━━━

🎯 ** upcoming：**
- v2026.0302.1520 - 收藏/点赞功能
- v2026.0302.1530 - 优化 AI 评价算法
- v2026.0302.1540 - 项目详情弹窗

━━━━━━━━━━━━━━━━

✅ 小明同学 | AI 助手
"""
    else:
        content = f"""
⚠️ **AI Tech Daily 迭代异常**

━━━━━━━━━━━━━━━━

📦 **版本：** v{version}
⏰ **时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
❌ **状态：** 验证失败

━━━━━━━━━━━━━━━━

🔧 **问题：** {feature}

━━━━━━━━━━━━━━━━

建议检查 GitHub Actions 日志。

━━━━━━━━━━━━━━━━

⚠️ 小明同学 | AI 助手
"""
    
    result = send_wechat(f"🚀 AI Tech Daily v{version}", content)
    
    if result.get('code') == 0:
        print(f"📱 通知发送成功")
        return True
    else:
        print(f"⚠️ 通知发送失败：{result}")
        return False

if __name__ == "__main__":
    import sys
    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    feature = sys.argv[2] if len(sys.argv) > 2 else "未知功能"
    status = sys.argv[3] if len(sys.argv) > 3 else "success"
    send_iteration_notification(version, feature, status)
