with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# 代码清理 - Technical Debt Cleanup
# ============================================================

# ---- 1. 移除无用的内联注释 (Paul/Haizhi/调试标记) ----
# 移除类似 <!-- Paul: xxx --> 的注释
import re

# 移除调试 console.log 语句 (但保留关键的初始化日志)
debug_logs = re.findall(r"console\.(log|warn)\([^)]*\);", content)
print(f'Console statements found: {len(debug_logs)}')

# 移除内部的 /* Paul: xxx */ 格式调试注释
paul_comments = re.findall(r'\n\s*/\* *(Paul|Haizhi|Sam|调试|临时|TODO.*?:.*?)\s*\*/', content)
print(f'Internal dev comments: {len(paul_comments)}')

# 只移除明显的临时调试注释，保留功能性注释
patterns_to_remove = [
    # 临时调试行
    (r'\n\s*console\.log\([^)]*["\'](?:调试|临时|test|check)[\'"]?\);?\n', '\n'),
    (r'\n\s*console\.warn\([^)]*["\'](?:调试|临时|test|check)[\'"]?\);?\n', '\n'),
    # 临时代码块标记
    (r'\n\s*/\* ---- 临时注释[^-]*---- \*/\n', '\n'),
    # 过时的功能标记
    (r'\n\s*/\* === OLD VERSION[^-]*=== \*/\n', '\n'),
    (r'\n\s*/\* === UNUSED[^-]*=== \*/\n', '\n'),
]

for pattern, replacement in patterns_to_remove:
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        diff = len(content) - len(new_content)
        content = new_content
        changes += 1
        print(f'Cleaned pattern, removed {diff} chars')

# ---- 2. 合并重复的CSS规则 ----
# 检查是否有完全相同的CSS类定义（同一个class出现多次）
css_blocks = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*\}', content)
from collections import Counter
css_counts = Counter(css_blocks)
duplicates = {k: v for k, v in css_counts.items() if v > 1}
print(f'\nDuplicate CSS classes (defined {v} times): {list(duplicates.keys())[:5]}')

# ---- 3. 检查重复的函数定义 ----
# 提取所有 const/function 声明
func_decls = re.findall(r'(?:const|function)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*[\(=]', content)
func_counts = Counter(func_decls)
dup_funcs = {k: v for k, v in func_counts.items() if v > 1}
print(f'\nDuplicate JS declarations: {dup_funcs}')

# ---- 4. 移除空的样式块 ----
empty_css = re.findall(r'\.[a-zA-Z0-9_-]+\s*\{\s*\}', content)
print(f'\nEmpty CSS classes: {len(empty_css)}')
empty_clean = re.sub(r'\.[a-zA-Z0-9_-]+\s*\{\s*\}', '', content)
if empty_clean != content:
    content = empty_clean
    changes += 1
    print('Removed empty CSS classes')

# ---- 5. 清理末尾多余空白 ----
content = content.rstrip() + '\n'

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n=== 清理完成 ===')
print(f'总变更次数: {changes}')
print(f'最终文件大小: {len(content)} chars')
