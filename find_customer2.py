import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 找客户管理主页面区域
matches = [(m.start(), content[max(0,m.start()-100):m.start()+80]) for m in re.finditer(r'currentPage\s*===\s*[\'"]customer|客户管理|openCustomerModal|customerModal', content)]
print(f'Found {len(matches)} customer page references:')
for pos, ctx in matches[:20]:
    line_num = content[:pos].count('\n') + 1
    print(f'  L{line_num}: ...{ctx.replace(chr(10), " ")[:80]}')
