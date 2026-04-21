import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 找 return { 块
# 找包含 saveTeamMembers 的 return 块
pos = content.find('saveTeamMembers,')
if pos > 0:
    # 往前找 return {
    search_start = max(0, pos - 500)
    return_start = content.rfind('return {', search_start, pos)
    if return_start >= 0:
        # 往后找到匹配的 }
        depth = 0
        i = return_start + 7  # skip 'return {'
        line_start = content.rfind('\n', max(0, return_start - 100))
        
        # 找 return 块结束
        brace_start = content.find('{', return_start)
        depth = 1
        j = brace_start + 1
        while depth > 0 and j < len(content):
            if content[j] == '{':
                depth += 1
            elif content[j] == '}':
                depth -= 1
            j += 1
        
        return_block = content[return_start:j]
        print(f'Found return block, {len(return_block)} chars, {return_block.count(chr(10))} lines')
        
        # 检查是否已有 customerSearchKey
        if 'customerSearchKey' in return_block:
            print('customerSearchKey already in return block')
        else:
            # 在 saveTeamMembers, 后插入
            new_block = return_block.replace('saveTeamMembers,', 'saveTeamMembers,\n      customerSearchKey,customerFilterStatus,customerFilterLevel,filteredCustomers,\n      getCustomerProjects,addCustomerActivity,')
            content = content[:return_start] + new_block + content[j:]
            with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('OK: Updated return statement')
    else:
        print('WARN: return { not found before saveTeamMembers')
else:
    print('WARN: saveTeamMembers, not found in file')
