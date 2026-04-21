import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找return块
return_pos = content.rfind('return {', 0, content.find('app.mount'))
if return_pos < 0:
    return_pos = content.rfind('return {', 0, len(content)-1000)
    
if return_pos >= 0:
    depth = 1
    j = content.find('{', return_pos) + 1
    while depth > 0 and j < len(content):
        if content[j] == '{': depth += 1
        elif content[j] == '}': depth -= 1
        j += 1
    
    block = content[return_pos:j]
    lines = block.split('\n')
    print(f'Return block: {len(block)} chars, {len(lines)} lines')
    print('\nLast 30 lines:')
    for i, line in enumerate(lines[-30:]):
        actual_line = len(lines) - 30 + i + 1
        print(f'L{actual_line}: {line.strip()[:100]}')
    
    # 检查是否有 customerSearchKey
    if 'customerSearchKey' in block:
        print('\ncustomerSearchKey: ALREADY IN RETURN')
    else:
        print('\ncustomerSearchKey: NOT IN RETURN - need to add')
        # 找最后导出的函数位置
        for i in range(len(lines)-1, -1, -1):
            line = lines[i].strip()
            if line and not line.startswith('//'):
                print(f'Last export line {i}: {line[:80]}')
                break
