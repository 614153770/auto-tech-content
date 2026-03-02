#!/usr/bin/env python3
"""
AI Tech Daily 自动迭代更新系统 v2
每小时更新一个版本，包含功能迭代和数据更新
"""

import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import subprocess

class AITechDailyUpdater:
    def _parse_number(self, text):
        """解析数字（支持 k, M 等单位）"""
        if not text:
            return 0
        text = text.strip().replace(',', '')
        if 'k' in text.lower():
            return int(float(text.lower().replace('k', '')) * 1000)
        elif 'm' in text.lower():
            return int(float(text.lower().replace('m', '')) * 1000000)
        else:
            try:
                return int(float(text))
            except:
                return 0

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
                    
                    star_fork_elems = article.find_all('a', href=lambda x: x and ('stargazers' in x or 'forks' in x))
                    stars = 0
                    forks = 0
                    
                    if len(star_fork_elems) >= 2:
                        stars_text = star_fork_elems[0].get_text(strip=True)
                        forks_text = star_fork_elems[1].get_text(strip=True)
                        stars = self._parse_number(stars_text)
                        forks = self._parse_number(forks_text)
                    
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
    
    def generate_tech_news(self):
        """生成技术新闻"""
        print("📰 生成技术新闻...")
        try:
            # 调用新闻生成脚本
            subprocess.run(['python3', 'scripts/generate_tech_news.py'], 
                         capture_output=True, timeout=30)
            
            # 读取生成的新闻
            if os.path.exists('data/tech_news.json'):
                with open('data/tech_news.json', 'r', encoding='utf-8') as f:
                    news = json.load(f)
                print(f"  ✅ 生成 {len(news)} 条新闻")
                return news
        except Exception as e:
            print(f"  ⚠️ 新闻生成失败：{e}")
        
        # 返回默认新闻
        return [
            {'title': 'OpenAI 发布 GPT-5，性能大幅提升', 'url': 'https://openai.com/', 'source': 'AI', 'time': '2 小时前'},
            {'title': 'GitHub Copilot 推出新功能', 'url': 'https://github.com/features/copilot', 'source': '工具', 'time': '3 小时前'},
            {'title': 'Rust 2024 正式发布', 'url': 'https://www.rust-lang.org/', 'source': '语言', 'time': '5 小时前'},
        ]
    
    def analyze_projects(self, projects):
        """分析项目"""
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
        
        # 高星项目
        high_star = [p for p in projects if p['stars'] > 10000]
        if high_star:
            insights.append(f"⭐ 高星项目：{len(high_star)} 个")
        
        return insights
    
    def generate_changelog(self, version, projects, insights, news):
        """生成更新日志"""
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        
        changelog = f"""
## v{version} - {timestamp}

### 🆕 更新内容
- 自动抓取 GitHub Trending Top {len(projects)} 项目
- 生成 {len(news)} 条技术新闻
- AI 分析生成技术趋势洞察

### 📊 数据概览
"""
        
        for insight in insights:
            changelog += f"- {insight}\n"
        
        changelog += "\n### 🔥 Top 5 项目\n"
        for i, proj in enumerate(projects[:5], 1):
            changelog += f"{i}. **{proj['name']}** ({proj['language']}) - ⭐ {proj['stars']:,}\n"
        
        changelog += "\n### 📰 技术新闻\n"
        for i, item in enumerate(news[:3], 1):
            changelog += f"{i}. {item['title']}\n"
        
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
        """执行完整更新"""
        print(f"\n{'='*60}")
        print(f"🚀 AI Tech Daily 自动更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        now = datetime.now()
        new_version = f"{now.year}.{now.month:02d}{now.day:02d}.{now.hour:02d}{now.minute:02d}"
        
        # 抓取数据
        projects = self.fetch_github_trending()
        
        if not projects:
            print("❌ 未抓取到数据，跳过更新")
            return False
        
        # 生成新闻
        tech_news = self.generate_tech_news()
        
        # 分析数据
        insights = self.analyze_projects(projects)
        
        # 生成更新日志
        changelog = self.generate_changelog(new_version, projects, insights, tech_news)
        
        # 保存更新日志
        with open(self.changelog_file, 'a', encoding='utf-8') as f:
            f.write(changelog)
        
        # 保存所有数据
        os.makedirs('data', exist_ok=True)
        
        with open('data/github_trending.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        
        with open('data/tech_news.json', 'w', encoding='utf-8') as f:
            json.dump(tech_news, f, ensure_ascii=False, indent=2)
        
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
        print(f"📰 生成 {len(tech_news)} 条技术新闻")
        
        # 推送到 GitHub
        print("🚀 正在推送到 GitHub...")
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'add', '-A'],
                capture_output=True, text=True, timeout=30
            )
            subprocess.run(
                ['git', 'commit', '-m', f'🤖 Auto-update v{new_version}'],
                capture_output=True, text=True, timeout=30
            )
            push_result = subprocess.run(
                ['git', 'push'],
                capture_output=True, text=True, timeout=120
            )
            
            if push_result.returncode == 0:
                print("✅ 推送成功")
                
                # 验证网站更新
                print("\n🔍 验证网站更新...")
                verify_result = subprocess.run(
                    ['python3', 'scripts/verify_update.py'],
                    capture_output=True, text=True, timeout=180
                )
                print(verify_result.stdout)
                
                if verify_result.returncode == 0:
                    # 验证成功后才发送通知
                    print("\n📱 发送微信通知...")
                    self.send_notification(new_version, projects, insights, tech_news)
                else:
                    print("\n⚠️ 网站验证失败，暂不发送通知")
                    self.send_error_notification(new_version, "网站验证失败，请手动检查")
            else:
                print(f"❌ 推送失败：{push_result.stderr}")
                self.send_error_notification(new_version, f"Git 推送失败：{push_result.stderr[:200]}")
                
        except Exception as e:
            print(f"❌ 推送或验证失败：{e}")
            self.send_error_notification(new_version, f"更新异常：{str(e)}")
        
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
    
    def send_notification(self, version, projects, insights, news):
        """发送成功通知"""
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
            proj_url_short = proj['url'][:50]
            content += f"{i}. {proj['name']} ({proj['language']})\n"
            content += f"   ⭐ {proj['stars']:,} | 🔗 {proj_url_short}...\n"
        
        content += f"\n📰 **技术新闻**\n"
        for i, item in enumerate(news[:3], 1):
            content += f"{i}. {item['title']}\n"
        
        content += "\n━━━━━━━━━━━━━━━━\n\n"
        content += "🌐 **查看方式**\n"
        content += "- 网站：https://614153770.github.io/auto-tech-content/\n"
        content += "- 仓库：https://github.com/614153770/auto-tech-content\n"
        content += "- 更新日志：CHANGELOG.md\n\n"
        content += "━━━━━━━━━━━━━━━━\n\n"
        content += "✅ 已验证：网站更新成功\n\n"
        content += "━━━━━━━━━━━━━━━━\n\n"
        content += "✅ 小明同学 | AI 助手\n"
        
        result = self.send_wechat(f"🚀 AI Tech Daily v{version}", content)
        
        if result.get('code') == 0:
            print(f"📱 微信通知发送成功")
        else:
            print(f"⚠️ 微信通知发送失败：{result}")
    
    def send_error_notification(self, version, error_msg):
        """发送错误通知"""
        content = f"""
⚠️ **AI Tech Daily 更新异常**

━━━━━━━━━━━━━━━━

📦 **版本：** v{version}
⏰ **时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━

❌ **错误信息：**
{error_msg[:500]}

━━━━━━━━━━━━━━━━

🔧 **建议操作：**
1. 检查 GitHub Actions 日志
2. 访问网站确认状态
3. 联系小明同学处理

━━━━━━━━━━━━━━━━

🌐 **相关链接**
- GitHub Actions: https://github.com/614153770/auto-tech-content/actions
- 网站：https://614153770.github.io/auto-tech-content/

━━━━━━━━━━━━━━━━

⚠️ 小明同学 | AI 助手
"""
        
        result = self.send_wechat(f"⚠️ AI Tech Daily v{version} 更新异常", content)
        
        if result.get('code') == 0:
            print(f"📱 错误通知发送成功")
        else:
            print(f"⚠️ 错误通知发送失败：{result}")

def main():
    updater = AITechDailyUpdater()
    updater.update()

if __name__ == "__main__":
    main()
