import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 找客户表单弹窗
matches = [(m.start(), content[max(0,m.start()-50):m.start()+100]) for m in re.finditer(r"modalType\s*===\s*['\"]customer['\"]", content)]
print(f'Customer modal references: {len(matches)}')
for pos, ctx in matches:
    line_num = content[:pos].count('\n') + 1
    print(f'  L{line_num}: {ctx.replace(chr(10), " ")[:100]}')

# 找客户相关函数
funcs = [(m.start(), m.group(1)) for m in re.finditer(r'const\s+(openCustomer|customerList|getCustomer|customerValue|editCustomer|viewCustomer|deleteCustomer)\w*', content)]
print(f'\nCustomer functions: {len(funcs)}')
for pos, name in funcs:
    line_num = content[:pos].count('\n') + 1
    print(f'  L{line_num}: {name}')

# 找customers数据定义
cust_data = [(m.start(), content[max(0,m.start()-20):m.start()+60]) for m in re.finditer(r'customers\s*=\s*ref\s*\(\[|const\s+customers\s*=', content)]
print(f'\nCustomer data definitions: {len(cust_data)}')
for pos, ctx in cust_data:
    line_num = content[:pos].count('\n') + 1
    print(f'  L{line_num}: {ctx.replace(chr(10), " ")[:80]}')
