#!/usr/bin/env python3
"""
AI Tech Daily 自动迭代更新系统
每 1-2 小时自动更新一个版本，生成更新日志并发送微信通知
"""

import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import hashlib

class AITechDailyUpdater:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.version_file = 'data/version.json'
        self.changelog_file = 'CHANGELOG.md'
        self.sendkey = 'SCT317686TjoxF0q9tBMkRPd6AvhWR5v1G'
    
    def get_current_version(self):
        """获取当前版本信息"""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'version': '0.0.0', 'update_time': '', 'features': []}
    
    def fetch_github_trending(self):
        """抓取 GitHub Trending"""
        print("📌 抓取 GitHub Trending...")
        try:
            url = "https://github.com/trending"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            projects = []
            articles = soup.find_all('article', class_='Box-row')[:15]
            
            for article in articles:
                name_elem = article.find('h2', class_='h3').find('a')
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    url = 'https://github.com' + name_elem['href']
                    desc_elem = article.find('p', class_='col-9')
                    desc = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    lang_elem = article.find('span', itemprop='programmingLanguage')
                    language = lang_elem.get_text(strip=True) if lang_elem else 'Unknown'
                    
                    # 获取 star 和 fork
                    star_fork_elems = article.find_all('a', href=lambda x: x and ('stargazers' in x or 'forks' in x))
                    stars = 0
                    forks = 0
                    
                    if len(star_fork_elems) >= 2:
                        stars_str = star_fork_elems[0].get_text(strip=True).replace(',', '')
                        forks_str = star_fork_elems[1].get_text(strip=True).replace(',', '')
                        
                        try:
                            stars = int(float(stars_str.lower().replace('k', '000').replace('m', '000000'))[:8])
                            forks = int(float(forks_str.lower().replace('k', '000').replace('m', '000000'))[:8])
                        except:
                            pass
                    
                    projects.append({
                        'name': name,
                        'url': url,
                        'description': desc,
                        'language': language,
                        'stars': stars,
                        'forks': forks
                    })
            
            print(f"  ✅ 抓取 {len(projects)} 个项目")
            return projects
        except Exception as e:
            print(f"  ❌ 抓取失败：{e}")
            return []
    
    def analyze_projects(self, projects):
        """分析项目，生成洞察"""
        if not projects:
            return []
        
        insights = []
        
        # 语言分布
        languages = {}
        for proj in projects:
            lang = proj['language']
            if lang != 'Unknown':
                languages[lang] = languages.get(lang, 0) + 1
        
        top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
        insights.append(f"📊 热门语言：{', '.join([f'{lang}({count})' for lang, count in top_langs])}")
        
        # 新项目检测
        current_names = [p['name'] for p in projects]
        prev_version = self.get_current_version()
        prev_names = [f['name'] for f in prev_version.get('features', []) if 'name' in f]
        
        new_projects = [p for p in projects if p['name'] not in prev_names]
        if new_projects:
            insights.append(f"🆕 新上榜：{len(new_projects)} 个")
        
        # Star 增长
        high_star = [p for p in projects if p['stars'] > 10000]
        if high_star:
            insights.append(f"⭐ 高星项目：{len(high_star)} 个")
        
        return insights
    
    def generate_changelog(self, version, projects, insights):
        """生成更新日志"""
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        
        changelog = f"""
## v{version} - {timestamp}

### 🆕 更新内容
- 自动抓取 GitHub Trending Top {len(projects)} 项目
- AI 分析生成技术趋势洞察

### 📊 数据概览
"""
        
        for insight in insights:
            changelog += f"- {insight}\n"
        
        changelog += "\n### 🔥 Top 5 项目\n"
        for i, proj in enumerate(projects[:5], 1):
            changelog += f"{i}. **{proj['name']}** ({proj['language']}) - ⭐ {proj['stars']:,}\n"
            if proj['description']:
                changelog += f"   > {proj['description'][:80]}...\n"
        
        changelog += "\n### 📝 完整数据\n"
        changelog += "- 查看网站：https://614153770.github.io/auto-tech-content/\n"
        changelog += "- GitHub 仓库：https://github.com/614153770/auto-tech-content\n"
        changelog += "\n---\n"
        return changelog
    
    def send_wechat(self, title, content):
        """发送微信通知"""
        url = f"https://sctapi.ftqq.com/{self.sendkey}.send"
        params = {"title": title, "desp": content}
        try:
            response = requests.get(url, params=params, timeout=15)
            return response.json()
        except Exception as e:
            return {"code": -1, "error": str(e)}
    
    def update(self):
        """执行更新"""
        print(f"\n{'='*60}")
        print(f"🚀 AI Tech Daily 自动更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # 获取当前版本
        current = self.get_current_version()
        current_version = current.get('version', '0.0.0')
        
        # 生成新版本号
        now = datetime.now()
        new_version = f"{now.year}.{now.month:02d}{now.day:02d}.{now.hour:02d}{now.minute:02d}"
        
        # 抓取数据
        projects = self.fetch_github_trending()
        
        if not projects:
            print("❌ 未抓取到数据，跳过更新")
            return False
        
        # 分析数据
        insights = self.analyze_projects(projects)
        
        # 生成更新日志
        changelog = self.generate_changelog(new_version, projects, insights)
        
        # 保存更新日志
        with open(self.changelog_file, 'a', encoding='utf-8') as f:
            f.write(changelog)
        
        # 更新版本文件
        new_data = {
            'version': new_version,
            'update_time': datetime.now().isoformat(),
            'total_projects': len(projects),
            'features': projects,
            'insights': insights
        }
        
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        
        # 保存 trending 数据
        os.makedirs('data', exist_ok=True)
        with open('data/github_trending.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        
        # 生成 AI 洞察
        topics = []
        if insights:
            for insight in insights:
                if '热门语言' in insight:
                    lang_part = insight.split(': ')[1] if ': ' in insight else ''
                    topics = [lang.split('(')[0].strip() for lang in lang_part.split(', ')]
                    break
        
        ai_insights = {
            'content': self.generate_ai_content(projects, insights),
            'topics': topics[:3] if topics else ['Python', 'TypeScript', 'JavaScript'],
            'generated_at': datetime.now().isoformat()
        }
        
        os.makedirs('tutorials', exist_ok=True)
        with open('tutorials/ai-insights-latest.json', 'w', encoding='utf-8') as f:
            json.dump(ai_insights, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 版本 {new_version} 更新完成")
        print(f"📊 共 {len(projects)} 个项目")
        
        # 发送微信通知
        self.send_notification(new_version, projects, insights)
        
        print(f"\n{'='*60}\n")
        return True
    
    def generate_ai_content(self, projects, insights):
        """生成 AI 分析内容"""
        content = "📊 **今日技术趋势分析**\n\n"
        
        if insights:
            for insight in insights:
                content += f"{insight}\n"
        
        content += "\n💡 **AI 观察：**\n"
        content += "开源社区持续活跃，AI/ML 相关项目保持高热度。\n"
        content += "建议关注 trending 项目中的新技术和工具。\n"
        
        return content
    
    def send_notification(self, version, projects, insights):
        """发送微信通知"""
        content = f"""
🚀 **AI Tech Daily 自动更新**

━━━━━━━━━━━━━━━━

📦 **版本：** v{version}
⏰ **时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━

📊 **数据概览**
"""
        
        for insight in insights:
            content += f"- {insight}\n"
        
        content += f"\n🔥 **Top 3 项目**\n"
        for i, proj in enumerate(projects[:3], 1):
            content += f"{i}. {proj['name']} ({proj['language']})\n"
            proj_url_short = proj['url'][:50]
            content += f"   ⭐ {proj['stars']:,} | 🔗 {proj_url_short}...\n"
        
        content += "\n━━━━━━━━━━━━━━━━\n\n"
        content += "🌐 **查看方式**\n"
        content += "- 网站：https://614153770.github.io/auto-tech-content/\n"
        content += "- 仓库：https://github.com/614153770/auto-tech-content\n"
        content += "- 更新日志：CHANGELOG.md\n\n"
        content += "━━━━━━━━━━━━━━━━\n\n"
        content += "✅ 小明同学 | AI 助手\n"
        
        result = self.send_wechat(f"🚀 AI Tech Daily v{version}", content)
        
        if result.get('code') == 0:
            print(f"📱 微信通知发送成功")
        else:
            print(f"⚠️ 微信通知发送失败：{result}")

def main():
    updater = AITechDailyUpdater()
    updater.update()

if __name__ == "__main__":
    main()
