import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 找关键函数签名
patterns = [
    'const saveCustomer=',
    'const viewCustomer=',
    'const editCustomer=',
    'saveTeamMembers,',
    'saveTeamMembers=',
]

for p in patterns:
    pos = content.find(p)
    if pos > 0:
        line_num = content[:pos].count('\n') + 1
        ctx = content[pos:pos+150].replace('\n', ' ')
        print(f'L{line_num}: {p}')
        print(f'  {ctx[:120]}')
        print()
    else:
        print(f'NOT FOUND: {p}')
        print()
