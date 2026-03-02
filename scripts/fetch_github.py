#!/usr/bin/env python3
"""
GitHub Trending 数据抓取脚本
自动获取 GitHub Trending 项目并保存为 JSON
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def fetch_github_trending():
    """抓取 GitHub Trending 页面"""
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        projects = []
        
        # 查找所有 trending 项目
        articles = soup.find_all('article', class_='Box-row')
        
        for article in articles[:10]:  # 取前 10 个
            try:
                # 项目名称
                name_elem = article.find('h2', class_='h3').find('a')
                name = name_elem.get_text(strip=True) if name_elem else 'Unknown'
                url = 'https://github.com' + name_elem['href'] if name_elem else ''
                
                # 描述
                desc_elem = article.find('p', class_='col-9')
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 语言
                lang_elem = article.find('span', itemprop='programmingLanguage')
                language = lang_elem.get_text(strip=True) if lang_elem else 'Unknown'
                
                # Star 数
                star_elem = article.find_all('a', href=lambda x: x and '/stargazers' in x)
                stars = 0
                if star_elem:
                    stars_str = star_elem[0].get_text(strip=True).replace(',', '')
                    try:
                        if 'k' in stars_str.lower():
                            stars = int(float(stars_str.lower().replace('k', '')) * 1000)
                        else:
                            stars = int(stars_str)
                    except:
                        stars = 0
                
                # Fork 数
                fork_elem = article.find_all('a', href=lambda x: x and '/forks' in x)
                forks = 0
                if fork_elem:
                    forks_str = fork_elem[0].get_text(strip=True).replace(',', '')
                    try:
                        if 'k' in forks_str.lower():
                            forks = int(float(forks_str.lower().replace('k', '')) * 1000)
                        else:
                            forks = int(forks_str)
                    except:
                        forks = 0
                
                projects.append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'language': language,
                    'stars': stars,
                    'forks': forks,
                    'fetched_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"解析项目失败：{e}")
                continue
        
        return projects
        
    except Exception as e:
        print(f"抓取失败：{e}")
        return []

def save_to_json(data, filepath):
    """保存数据到 JSON 文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {filepath}")

def main():
    print(f"[{datetime.now()}] 开始抓取 GitHub Trending...")
    
    projects = fetch_github_trending()
    
    if projects:
        print(f"成功抓取 {len(projects)} 个项目")
        
        # 保存数据
        save_to_json(projects, 'data/github_trending.json')
        
        # 生成简单报告
        report = {
            'update_time': datetime.now().isoformat(),
            'total_projects': len(projects),
            'top_project': projects[0] if projects else None,
            'languages': list(set([p['language'] for p in projects if p['language'] != 'Unknown']))
        }
        save_to_json(report, 'data/trending_report.json')
        
        print("✅ 抓取完成")
    else:
        print("❌ 抓取失败，使用缓存数据")

if __name__ == "__main__":
    main()
