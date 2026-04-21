with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. 找重复的函数声明
lines = content.split('\n')
func_positions = {}
for i, line in enumerate(lines):
    m = re.match(r'\s*(?:const|let|var|function)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*[\(=]', line)
    if m:
        name = m.group(1)
        if name not in func_positions:
            func_positions[name] = []
        func_positions[name].append(i+1)

dup_funcs = {k: v for k, v in func_positions.items() if len(v) > 1}
print(f'=== 重复函数声明 ({len(dup_funcs)}个) ===')
for name, positions in sorted(dup_funcs.items(), key=lambda x: x[1][0]):
    print(f'  {name}: 行 {positions}')

# 2. 找重复的变量声明
var_positions = {}
for i, line in enumerate(lines):
    m = re.match(r'\s*(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=', line)
    if m:
        name = m.group(1)
        if name not in var_positions:
            var_positions[name] = []
        var_positions[name].append(i+1)

dup_vars = {k: v for k, v in var_positions.items() if len(v) > 1}
print(f'\n=== 重复变量声明 ({len(dup_vars)}个) ===')
for name, positions in sorted(dup_vars.items(), key=lambda x: x[1][0])[:10]:
    print(f'  {name}: 行 {positions}')

# 3. 检查未闭合的大括号（setup函数）
setup_start = None
setup_end = None
brace_count = 0
in_setup = False
for i, line in enumerate(lines):
    if 'const setup=()=>{' in line or 'setup=()=>{' in line:
        setup_start = i+1
        in_setup = True
        brace_count = 1
        continue
    if in_setup:
        brace_count += line.count('{') - line.count('}')
        if brace_count == 0:
            setup_end = i+1
            break

print(f'\n=== setup函数 ===')
if setup_start:
    print(f'  开始: 行 {setup_start}')
    if setup_end:
        print(f'  结束: 行 {setup_end}')
        print(f'  总行数: {setup_end - setup_start}')
    else:
        print(f'  警告: 未找到结束！剩余大括号: {brace_count}')
else:
    print('  未找到')

# 4. 检查文件结构完整性
print(f'\n=== 文件结构 ===')
print(f'  总行数: {len(lines)}')
print(f'  <script>标签: {content.count("<script>")}')
print(f'  </script>标签: {content.count("</script>")}')
print(f'  <style>标签: {content.count("<style>")}')
print(f'  </style>标签: {content.count("</style>")}')
