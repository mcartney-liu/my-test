with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有script标签位置
import re
starts = [(m.start(), 'script') for m in re.finditer(r'<script>', content)]
ends = [(m.start(), '/script') for m in re.finditer(r'</script>', content)]

all_tags = sorted(starts + ends)
print(f'Script tags found:')
for pos, tag in all_tags:
    line_num = content[:pos].count('\n') + 1
    # Show context
    ctx_start = max(0, pos-20)
    ctx = content[ctx_start:pos+30].replace('\n', ' ')
    print(f'  Line {line_num}: {tag} -- {ctx[:60]}')

print(f'\nTotal: {len(starts)} <script>, {len(ends)} </script>')
if len(ends) > len(starts):
    print(f'ERROR: {len(ends)-len(starts)} extra </script> tags!')
