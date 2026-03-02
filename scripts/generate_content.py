#!/usr/bin/env python3
"""
内容生成脚本 - AI 自动生成技术文章和心得
"""

import json
import os
from datetime import datetime

def generate_ai_insights(trending_data):
    """根据 trending 数据生成 AI 学习心得"""
    
    if not trending_data or len(trending_data) == 0:
        return {
            'content': '暂无数据，请稍后再来。',
            'topics': [],
            'generated_at': datetime.now().isoformat()
        }
    
    # 分析趋势
    languages = {}
    for project in trending_data:
        lang = project.get('language', 'Unknown')
        if lang != 'Unknown':
            languages[lang] = languages.get(lang, 0) + 1
    
    # 找出最热门的语言
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 生成洞察内容
    insights = []
    insights.append("📊 **今日技术趋势分析**")
    insights.append("")
    
    if top_langs:
        lang_text = "、".join([f"{lang} ({count}个项目)" for lang, count in top_langs])
        insights.append(f"今日 GitHub Trending 中，{lang_text}表现最为活跃。")
        insights.append("")
    
    # 分析 top 项目
    if len(trending_data) >= 3:
        top_project = trending_data[0]
        insights.append(f"🔥 **热门项目：{top_project['name']}**")
        insights.append(f"Star 数：{top_project['stars']:,} | Fork 数：{top_project['forks']:,}")
        if top_project.get('description'):
            insights.append(f"简介：{top_project['description']}")
        insights.append("")
    
    insights.append("💡 **AI 观察：**")
    insights.append("技术迭代速度持续加快，开源社区活跃度保持高位。")
    insights.append("建议关注以下方向：")
    
    for lang, _ in top_langs:
        insights.append(f"- {lang} 生态及相关工具链")
    
    return {
        'content': '\n'.join(insights),
        'topics': [lang for lang, _ in top_langs],
        'generated_at': datetime.now().isoformat()
    }

def generate_weekly_report(weekly_trending):
    """生成周报内容"""
    
    if not weekly_trending:
        return "# 本周周报\n\n暂无数据\n"
    
    report = []
    report.append("# 📰 AI Tech Weekly")
    report.append(f"\n生成时间：{datetime.now().strftime('%Y年%m月%d日')}\n")
    report.append("---\n")
    
    report.append("## 🔥 本周热门项目 Top 5\n")
    
    for i, project in enumerate(weekly_trending[:5], 1):
        report.append(f"### {i}. {project.get('name', 'Unknown')}")
        report.append(f"- **链接：** [{project.get('url', '#')}]({project.get('url', '#')})")
        report.append(f"- **语言：** {project.get('language', 'Unknown')}")
        report.append(f"- **Stars：** {project.get('stars', 0):,}")
        if project.get('description'):
            report.append(f"- **简介：** {project['description']}")
        report.append("")
    
    report.append("## 💡 AI 本周洞察\n")
    report.append("通过分析本周 trending 项目，AI 发现以下趋势：\n")
    report.append("1. 开源项目持续活跃，开发者参与度保持高位")
    report.append("2. AI/ML 相关工具库受到广泛关注")
    report.append("3. 开发者工具和生产效率类项目表现突出\n")
    
    report.append("## 📈 技术栈分布\n")
    
    languages = {}
    for project in weekly_trending:
        lang = project.get('language', 'Unknown')
        if lang != 'Unknown':
            languages[lang] = languages.get(lang, 0) + 1
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        report.append(f"- {lang}: {count} 个项目")
    
    report.append("\n---\n")
    report.append("*本报告的由 AI 自动生成，数据来源于 GitHub Trending*")
    
    return '\n'.join(report)

def main():
    print(f"[{datetime.now()}] 开始生成内容...")
    
    # 读取 trending 数据
    trending_file = 'data/github_trending.json'
    if os.path.exists(trending_file):
        with open(trending_file, 'r', encoding='utf-8') as f:
            trending_data = json.load(f)
        
        # 生成 AI 心得
        insights = generate_ai_insights(trending_data)
        
        # 保存心得
        os.makedirs('tutorials', exist_ok=True)
        with open('tutorials/ai-insights-latest.json', 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        
        print("✅ AI 心得生成完成")
        
        # 生成周报（如果有历史数据）
        weekly_report = generate_weekly_report(trending_data)
        week_num = datetime.now().isocalendar()[1]
        year = datetime.now().year
        with open(f'weekly/{year}-w{week_num:02d}.md', 'w', encoding='utf-8') as f:
            f.write(weekly_report)
        
        print(f"✅ 周报生成完成：{year}-w{week_num:02d}.md")
    else:
        print("⚠️ 未找到 trending 数据，跳过内容生成")

if __name__ == "__main__":
    main()
