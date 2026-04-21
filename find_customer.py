import re

with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到客户管理相关代码位置
lines = content.split('\n')

print(f'=== 客户管理关键词位置 ===')
for i, line in enumerate(lines):
    if any(kw in line for kw in ['客户', 'customer', 'Customer', 'customerList', 'customerModal']):
        print(f'L{i+1}: {line.strip()[:100]}')

print(f'\n=== 总行数: {len(lines)} ===')
