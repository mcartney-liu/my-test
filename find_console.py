with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 统计并列出所有console语句
console_stmts = [(m.start(), m.group()) for m in re.finditer(r'console\.(log|warn|error|info)\([^)]*\);?', content)]
print(f'Total console statements: {len(console_stmts)}')

# 按行分组
by_line = {}
for pos, stmt in console_stmts:
    line_num = content[:pos].count('\n') + 1
    by_line.setdefault(line_num, []).append(stmt)

# 显示前20个
print('\nConsole statements (first 20):')
for line_num in sorted(by_line.keys())[:20]:
    stmts = by_line[line_num]
    ctx_start = content.rfind('\n', 0, content.find('\n' * (line_num - 1) + content.split('\n')[line_num-1], 0) if line_num > 1 else 0)
    line_start = content.rfind('\n', 0, content.find('\n' * (line_num - 1)))
    line_end = content.find('\n', line_start if line_start >= 0 else 0)
    line_text = content[line_start if line_start >= 0 else 0:line_end].strip()[:100] if line_start >= 0 else ''
    print(f'  L{line_num}: {line_text}')

# 移除不必要的调试console语句（保留关键初始化日志）
removable = []
for pos, stmt in console_stmts:
    line_num = content[:pos].count('\n') + 1
    stmt_lower = stmt.lower()
    # 保留包含关键信息的日志（初始化、错误、警告）
    keep = any(kw in stmt_lower for kw in [
        'error', 'err', '初始化', '不支持', 'failed', 'invalid', '异常', 'warn',
        'start', 'begin', '启动', 'loaded'
    ])
    if not keep:
        removable.append((pos, stmt, line_num))

print(f'\nRemovable debug console statements: {len(removable)}')
print('Keeping critical logs: critical system messages')
