import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找 return 块中包含 saveTeamMembers 的区域
pos = content.find('saveTeamMembers')
if pos >= 0:
    line_num = content[:pos].count('\n') + 1
    ctx = content[max(0,pos-100):pos+200].replace('\n', ' ')
    print(f'Found at L{line_num}: {ctx}')
else:
    print('saveTeamMembers not found')

# 也找 saveTeamMembers= 在return之前的
pos2 = content.find('saveTeamMembers=')
if pos2 >= 0:
    line_num = content[:pos2].count('\n') + 1
    ctx = content[max(0,pos2-50):pos2+100].replace('\n', ' ')
    print(f'\nsaveTeamMembers= at L{line_num}: {ctx}')

# 找return块中最后几个导出
return_pos = content.rfind('return {', 0, content.find('saveTeamMembers'))
if return_pos >= 0:
    # 往后找 } 
    depth = 1
    j = content.find('{', return_pos) + 1
    while depth > 0 and j < len(content):
        if content[j] == '{': depth += 1
        elif content[j] == '}': depth -= 1
        j += 1
    block = content[return_pos:j]
    # 找最后20行
    lines = block.split('\n')
    print(f'\nLast 25 lines of return block:')
    for line in lines[-25:]:
        if line.strip():
            print(f'  {line.strip()[:100]}')
