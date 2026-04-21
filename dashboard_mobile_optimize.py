with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# =========================================================
# 优化1: 移动端仪表盘 - 风险/健康面板改为单列显示
# =========================================================
old_risk_panel = """        <!-- Paul：风险预警面板 + 项目健康度 -->
        <div v-if="dashboardCards.find(c=>c.id==='risk')?.visible" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;" >"""

new_risk_panel = """        <!-- Paul：风险预警面板 + 项目健康度 (移动端单列) -->
        <div v-if="dashboardCards.find(c=>c.id==='risk')?.visible" class="risk-health-grid" style="margin-bottom:16px;" >"""

content = content.replace(old_risk_panel, new_risk_panel)

# =========================================================
# 优化2: 快捷入口 - 移动端缩小间距
# =========================================================
old_shortcuts = """        <!-- Paul：今日快捷入口 -->
        <div v-if="dashboardCards.find(c=>c.id==='shortcuts')?.visible" style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:16px;">"""

new_shortcuts = """        <!-- Paul：今日快捷入口 -->
        <div v-if="dashboardCards.find(c=>c.id==='shortcuts')?.visible" class="shortcuts-grid" style="margin-bottom:16px;">"""

content = content.replace(old_shortcuts, new_shortcuts)

# =========================================================
# 优化3: 任务看板卡片 - 新增任务类型标签 + 进度条
# =========================================================
old_kanban_card = """                  <div class="card-meta">
                    <span v-if="t.projectId" class="card-tag"><i data-lucide="folder" style="width:10px;height:10px;margin-right:3px;"></i>{{(projects.find(p=>p.id===t.projectId)||{}).name||'未分配'}}</span>
                    <span v-if="t.assignee" class="card-assignee"><i data-lucide="user" style="width:10px;height:10px;"></i>{{t.assignee}}</span>
                    <span class="card-tag" :style="{color:t.priority==='紧急'?'var(--danger)':t.priority==='高'?'#f97316':'var(--muted)'}">{{t.priority}}</span>
                  </div>
                  <div class="card-footer">"""

new_kanban_card = """                  <div class="card-meta">
                    <span v-if="t.type" class="card-tag" style="background:rgba(99,102,241,0.2);color:var(--primary);border:1px solid rgba(99,102,241,0.3);"><i data-lucide="tag" style="width:9px;height:9px;margin-right:2px;"></i>{{t.type}}</span>
                    <span v-if="t.projectId" class="card-tag"><i data-lucide="folder" style="width:10px;height:10px;margin-right:3px;"></i>{{(projects.find(p=>p.id===t.projectId)||{}).name||'未分配'}}</span>
                    <span v-if="t.assignee" class="card-assignee"><i data-lucide="user" style="width:10px;height:10px;"></i>{{t.assignee}}</span>
                    <span class="card-tag" :style="{color:t.priority==='紧急'?'var(--danger)':t.priority==='高'?'#f97316':'var(--muted)'}">{{t.priority}}</span>
                  </div>
                  <div class="card-footer">"""

if old_kanban_card in content:
    content = content.replace(old_kanban_card, new_kanban_card)
    print('OK: 任务看板卡片增强成功')
else:
    print('WARN: 找不到原来的任务卡片结构，尝试备用匹配')
    # Try partial match
    if '<span v-if="t.projectId" class="card-tag"><i data-lucide="folder"' in content:
        print('Found partial pattern - will need manual fix')
    else:
        print('ERROR: 卡片结构已变化')

# =========================================================
# 优化4: 仪表盘欢迎栏 - 移动端优化样式类
# =========================================================
old_welcome = """        <!-- 顶部欢迎栏 -->
        <div class="dashboard-welcome">"""

new_welcome = """        <!-- 顶部欢迎栏 -->
        <div class="dashboard-welcome dash-welcome">"""

content = content.replace(old_welcome, new_welcome)

# =========================================================
# 优化5: 添加CSS变量和移动端响应式样式
# =========================================================
# 找到 @media(max-width:768px) 中的 .stats-grid 位置，在其后添加新样式
old_mobile_stats = """  .stats-grid{grid-template-columns:repeat(2, 1fr);gap:0.75rem}
  .form-row{grid-template-columns:1fr}"""

new_mobile_stats = """  .stats-grid{grid-template-columns:repeat(2, 1fr);gap:0.75rem}
  .risk-health-grid{display:grid;grid-template-columns:1fr;gap:12px}
  .shortcuts-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
  .dash-welcome{padding:0.75rem!important}
  .dash-welcome h1{font-size:1.125rem!important}
  .quick-stats{flex-wrap:wrap;gap:4px}
  .form-row{grid-template-columns:1fr}"""

content = content.replace(old_mobile_stats, new_mobile_stats)
print('OK: 移动端CSS优化完成')

# =========================================================
# 优化6: 在 @media(max-width:480px) 中添加更小屏幕适配
# =========================================================
# Find if there's a 480px media query
if '@media(max-width:480px)' in content:
    old_480 = """@media(max-width:480px){
  .stats-grid{grid-template-columns:repeat(2, 1fr);gap:0.5rem}
  .form-row{grid-template-columns:1fr}"""
    new_480 = """@media(max-width:480px){
  .stats-grid{grid-template-columns:1fr 1fr;gap:0.5rem}
  .shortcuts-grid{grid-template-columns:repeat(3,1fr);gap:6px}
  .risk-health-grid{grid-template-columns:1fr}
  .dash-welcome{flex-direction:column;gap:0.5rem}
  .form-row{grid-template-columns:1fr}"""
    if old_480 in content:
        content = content.replace(old_480, new_480)
        print('OK: 480px断点优化完成')
    else:
        print('WARN: 480px断点内容不匹配')
else:
    print('INFO: 未找到480px断点，跳过')

# =========================================================
# 优化7: 任务卡片进度条改为更宽显示（在移动端）
# =========================================================
old_progress_mini = """.card-progress-mini{width:50px;height:4px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden}"""
new_progress_mini = """.card-progress-mini{width:60px;height:4px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;flex-shrink:0}"""

if old_progress_mini in content:
    content = content.replace(old_progress_mini, new_progress_mini)
    print('OK: 进度条样式优化完成')
else:
    print('WARN: 进度条样式未找到')

# =========================================================
# 优化8: 任务卡片底部布局优化 - 让进度条更明显
# =========================================================
old_card_footer = """.kanban-card .card-footer{display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding-left:8px}"""
new_card_footer = """.kanban-card .card-footer{display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding-left:8px;gap:8px}"""

if old_card_footer in content:
    content = content.replace(old_card_footer, new_card_footer)
    print('OK: 卡片底部布局优化完成')
else:
    print('WARN: 卡片底部布局未找到')

# Save
with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nDone! File length: {len(content)} chars')
