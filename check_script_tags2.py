with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find ALL script tag occurrences with full context
for m in re.finditer(r'</?script[^>]*>', content):
    pos = m.start()
    line_num = content[:pos].count('\n') + 1
    ctx_before = content[max(0,pos-100):pos].replace('\n', ' ')
    ctx_after = content[pos:pos+50].replace('\n', ' ')
    print(f'Line {line_num}: [{m.group()}]')
    print(f'  Before: ...{ctx_before[-60:]}')
    print(f'  After:  {ctx_after[:80]}...')
    print()
