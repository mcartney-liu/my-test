with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. AI区域：移除flex:1，改为固定高度紧凑布局
old_ai = '.dashboard-ai-section{'
if old_ai in content:
    idx = content.index(old_ai)
    # Find the end of this CSS block
    end_idx = content.index('}', idx)
    old_block = content[idx:end_idx+1]
    
    new_block = """.dashboard-ai-section{
  background:var(--glass-bg);
  border:1px solid var(--glass-border);
  border-radius:clamp(0.5rem, 0.8vw, 1rem);
  padding:clamp(10px, 1.2vw, 16px);
  flex:none;
  max-height:420px;
  overflow-y:auto;
}"""
    content = content.replace(old_block, new_block)
    changes += 1
    print('OK: AI区域CSS压缩')
else:
    print('MISS: AI区域CSS未找到')

# 2. AI区域HTML：移除flex:1和无效空间
old_ai_html = '<div class="dashboard-ai-section" v-if="dashboardCards.find(c=>c.id===\'ai\')?.visible" style="flex:1;display:flex;flex-direction:column;">'
new_ai_html = '<div class="dashboard-ai-section" v-if="dashboardCards.find(c=>c.id===\'ai\')?.visible" style="display:flex;flex-direction:column;">'
if old_ai_html in content:
    content = content.replace(old_ai_html, new_ai_html)
    changes += 1
    print('OK: AI区域HTML压缩')
else:
    # Try without flex:1
    alt = '<div class="dashboard-ai-section" v-if="dashboardCards.find(c=>c.id===\'ai\')?.visible" style="display:flex;flex-direction:column;">'
    if alt in content:
        print('OK: AI区域HTML(无flex:1)已正确')
    else:
        print('MISS: AI区域HTML未找到，搜索中...')
        pos = content.find('<div class="dashboard-ai-section"')
        print(f'  找到于位置: {pos}')

# 3. 各section margin-bottom从16px减少到10px
# 只针对仪表盘内的主要section
# Find the dashboard container and compress sections within it
dash_start = content.find('<div v-if="currentPage===\'dashboard\'">')
dash_end = content.find('<!-- Projects -->', dash_start)
dash_section = content[dash_start:dash_end]

# Compress margins
old_margins = [
    ('margin-bottom:16px', 'margin-bottom:10px'),
    ('margin-bottom:24px', 'margin-bottom:14px'),
    ('margin-bottom:20px', 'margin-bottom:12px'),
]
for old, new in old_margins:
    count = dash_section.count(old)
    if count > 0:
        dash_section = dash_section.replace(old, new)
        print(f'OK: 替换 {count} 个 "{old}" -> "{new}"')

content = content[:dash_start] + dash_section + content[dash_end:]

# 4. AI区域内部间距压缩
old_ai_h3 = '<h3 style="margin-bottom:16px;display:flex;align-items:center;gap:8px;">'
new_ai_h3 = '<h3 style="margin-bottom:10px;display:flex;align-items:center;gap:6px;">'
if old_ai_h3 in content:
    content = content.replace(old_ai_h3, new_ai_h3)
    changes += 1
    print('OK: AI区域标题间距压缩')

# 5. 输入记录按钮和输入框间距压缩
old_input_section = '<div style="margin-bottom:12px;">\n            <button @click="showInputHistory=!showInputHistory"'
if old_input_section in content:
    content = content.replace(old_input_section, '<div style="margin-bottom:8px;">\n            <button @click="showInputHistory=!showInputHistory"')
    changes += 1
    print('OK: 输入记录区间距压缩')

# 6. AI结果展示区间距压缩
old_result = '<div v-if="aiResult" style="margin-top:16px;padding:16px;background:'
new_result = '<div v-if="aiResult" style="margin-top:10px;padding:12px;background:'
if old_result in content:
    content = content.replace(old_result, new_result)
    changes += 1
    print('OK: AI结果区间距压缩')

# 7. 快捷入口区间距压缩
old_shortcuts = '<div v-if="dashboardCards.find(c=>c.id===\'shortcuts\')?.visible" class="shortcuts-grid" style="margin-bottom:16px;">'
new_shortcuts = '<div v-if="dashboardCards.find(c=>c.id===\'shortcuts\')?.visible" class="shortcuts-grid" style="margin-bottom:8px;">'
if old_shortcuts in content:
    content = content.replace(old_shortcuts, new_shortcuts)
    changes += 1
    print('OK: 快捷入口间距压缩')

# 8. 风险面板间距压缩
old_risk = '<div v-if="dashboardCards.find(c=>c.id===\'risk\')?.visible" class="risk-health-grid" style="margin-bottom:16px;" >'
new_risk = '<div v-if="dashboardCards.find(c=>c.id===\'risk\')?.visible" class="risk-health-grid" style="margin-bottom:8px;" >'
if old_risk in content:
    content = content.replace(old_risk, new_risk)
    changes += 1
    print('OK: 风险面板间距压缩')

# 9. 欢迎栏间距压缩
old_welcome = '<div class="dashboard-welcome dash-welcome">'
if old_welcome in content:
    content = content.replace(old_welcome, '<div class="dashboard-welcome dash-welcome" style="margin-bottom:10px;">')
    changes += 1
    print('OK: 欢迎栏间距设置')

# 10. 统计卡片区间距
old_stats = '<div class="stats-grid" v-if="dashboardCards.find(c=>c.id===\'stats\')?.visible" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0;">'
new_stats = '<div class="stats-grid" v-if="dashboardCards.find(c=>c.id===\'stats\')?.visible" style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px;">'
if old_stats in content:
    content = content.replace(old_stats, new_stats)
    changes += 1
    print('OK: 统计卡片区间距压缩')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n共完成 {changes}+ 项修改，文件长度: {len(content)} chars')
