#!/usr/bin/env python3
"""
网站更新验证脚本
推送后自动检查网站是否正常更新
"""

import requests
import time
from datetime import datetime

def verify_website_update():
    """验证网站更新"""
    print(f"\n{'='*60}")
    print(f"🔍 开始验证网站更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    url = "https://614153770.github.io/auto-tech-content/"
    max_retries = 6
    retry_interval = 10  # 秒
    
    for i in range(max_retries):
        try:
            print(f"📡 第 {i+1} 次尝试访问网站...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查关键元素
                checks = {
                    '新布局': 'content-grid' in content,
                    '中文说明': '🎯 中文说明' in content,
                    'AI 评价': '🤖 AI 评价' in content,
                    '技术新闻': '📰 技术新闻' in content,
                    'AI 心得': '💡 AI 学习心得' in content,
                }
                
                print(f"\n✅ 网站访问成功！")
                print(f"\n📊 功能验证结果：")
                
                all_passed = True
                for feature, passed in checks.items():
                    status = "✅" if passed else "❌"
                    print(f"  {status} {feature}")
                    if not passed:
                        all_passed = False
                
                if all_passed:
                    print(f"\n{'='*60}")
                    print(f"🎉 所有功能验证通过！更新成功！")
                    print(f"{'='*60}\n")
                    return True
                else:
                    print(f"\n⚠️ 部分功能未生效，可能需要等待 CDN 刷新")
                    if i < max_retries - 1:
                        print(f"⏳ {retry_interval}秒后重试...\n")
                        time.sleep(retry_interval)
                    else:
                        print(f"\n{'='*60}")
                        print(f"❌ 验证失败，请手动检查网站")
                        print(f"{'='*60}\n")
                        return False
            else:
                print(f"⚠️ 返回状态码：{response.status_code}")
                if i < max_retries - 1:
                    print(f"⏳ {retry_interval}秒后重试...\n")
                    time.sleep(retry_interval)
                    
        except Exception as e:
            print(f"❌ 访问失败：{e}")
            if i < max_retries - 1:
                print(f"⏳ {retry_interval}秒后重试...\n")
                time.sleep(retry_interval)
    
    return False

if __name__ == "__main__":
    success = verify_website_update()
    exit(0 if success else 1)
