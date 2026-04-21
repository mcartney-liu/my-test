with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

changes = 0

# ============================================================
# 代码清理 - 有选择性地移除调试日志
# ============================================================

# 明确移除的调试日志（纯状态/调试用，生产不需要）
debug_patterns = [
    # 语音识别 - 纯状态日志
    (r"\n\s*console\.log\(['\"]语音输入页面诊断\.\.\.['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]✅ Vue加载正常['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]✅ 浏览器支持语音识别API['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]语音识别已启动['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]识别到语音:['\"].*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]语音识别结束['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]开始语音识别['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]语音识别未初始化，正在初始化\.\.\.['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]停止语音识别['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]✅ 语音识别初始化成功['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]⚠️ 语音识别初始化失败['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]开始初始化语音识别\.\.\.['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]语音识别初始化已启动['\"]\);?\n", '\n'),
    # AI分析调试日志
    (r"\n\s*console\.log\(['\"]AI分析结果:['\"].*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]找到客户实体:['\"].*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]selectedEntities:.*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]indicesToSave:.*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]aiResult:.*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]删除客户, 搜索:.*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]页面诊断结果:.*?\);?\n", '\n'),
    # AI配置调试
    (r"\n\s*console\.log\(['\"]AI配置状态:.*?\);?\n", '\n'),
    # SW注册
    (r"\n\s*console\.log\(['\"]Service Worker注册成功:.*?\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]Service Worker注册失败:.*?\);?\n", '\n'),
    # 系统初始化
    (r"\n\s*console\.log\(['\"]PM-OS 系统初始化完成['\"]\);?\n", '\n'),
    (r"\n\s*console\.log\(['\"]自动恢复登录状态，用户:.*?\);?\n", '\n'),
]

# 实际执行清理
removed_count = 0
for pattern, replacement in debug_patterns:
    new_content = re.sub(pattern, replacement, content)
    if new_content != content:
        diff = len(content) - len(new_content)
        content = new_content
        removed_count += 1
        print(f'Removed debug log pattern (saved {diff} chars)')

# 使用更通用的模式处理语音识别相关日志块
# 移除相邻的多行console.log（语音识别模块）
voice_block = re.findall(
    r"console\.log\(['\"](?:开始初始化|识别到语音|语音识别已启动|语音识别结束|开始语音识别|停止语音识别|✅|⚠️)[^'\"]*['\"]\)",
    content
)
print(f'\nRemaining voice-related console.log: {len(voice_block)}')

# 统计清理后剩余的console数量
remaining = len(re.findall(r'console\.(log|warn|error)\(', content))
print(f'Remaining console statements: {remaining}')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nCleaned {removed_count} patterns')
print(f'Final file size: {len(content)} chars')
