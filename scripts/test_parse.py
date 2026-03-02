#!/usr/bin/env python3
"""
快速 Bug 修复：Star/Fork 数量解析
"""

import re

def parse_number(text):
    """正确解析数字（支持 k, M 等单位）"""
    if not text:
        return 0
    
    text = text.strip().replace(',', '')
    
    # 处理 k (千) 和 M (百万)
    if 'k' in text.lower():
        num = float(text.lower().replace('k', ''))
        return int(num * 1000)
    elif 'm' in text.lower():
        num = float(text.lower().replace('m', ''))
        return int(num * 1000000)
    else:
        try:
            return int(float(text))
        except:
            return 0

# 测试
test_cases = [
    ("1.2k", 1200),
    ("5k", 5000),
    ("1.5M", 1500000),
    ("20,000", 20000),
    ("123", 123),
    ("", 0),
]

print("测试数字解析：")
for text, expected in test_cases:
    result = parse_number(text)
    status = "✅" if result == expected else "❌"
    print(f"  {status} '{text}' -> {result} (期望：{expected})")
