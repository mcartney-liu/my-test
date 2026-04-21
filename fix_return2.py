import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找 return { 块
return_pos = content.rfind('return {', 0, content.find('app.mount'))

# 找 { return } 块
depth = 1
j = content.find('{', return_pos) + 1
while depth > 0 and j < len(content):
    if content[j] == '{': depth += 1
    elif content[j] == '}': depth -= 1
    j += 1

block = content[return_pos:j]
lines = block.split('\n')

# 找倒数第2行(空行 L91)的位置
# 在 empty line before } 插入
insert_after = None
for i in range(len(lines)-2, -1, -1):
    if lines[i].strip():
        insert_after = i
        break

if insert_after is not None:
    # 在该行后插入
    insert_line = len('\n'.join(lines[:insert_after+1]))
    insert_point = return_pos + insert_line
    insert_text = '\n      customerSearchKey,customerFilterStatus,customerFilterLevel,filteredCustomers,\n      getCustomerProjects,addCustomerActivity,'
    
    content = content[:insert_point] + insert_text + content[insert_point:]
    with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: Added customer exports to return statement')
    print(f'Inserted at line {content[:insert_point].count(chr(10))+1}')
else:
    print('ERROR: Could not find insertion point')
