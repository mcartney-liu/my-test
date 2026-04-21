with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 目标：把快捷入口移到刷新栏下方，横排显示
# 新布局顺序：
# 1. 刷新栏
# 2. 快捷入口横排（项目/任务/客户/问题/会议/AI助手）
# 3. 欢迎栏
# 4. 统计卡片
# 5. 风险/健康面板
# 6. AI数据识别区
# ============================================================

# Step 1: 修改 shortcuts-grid CSS 为横排单行
old_shortcuts_css = '.shortcuts-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}'
new_shortcuts_css = '.shortcuts-grid{display:flex;gap:6px;flex-wrap:wrap;align-items:center}'
if old_shortcuts_css in content:
    content = content.replace(old_shortcuts_css, new_shortcuts_css)
    print('OK: shortcuts CSS改为横排flex')
else:
    print('WARN: shortcuts CSS未匹配，搜索中...')
    pos = content.find('.shortcuts-grid{')
    if pos >= 0:
        end = content.index('}', pos)
        block = content[pos:end+1]
        print(f'  现有: {block[:100]}')
    else:
        print('  未找到shortcuts-grid CSS')

# Step 2: 修改快捷入口HTML，改为横排样式
# 原来的快捷入口每个item是grid cell，需要改为flex item
old_shortcuts_html = '''        <!-- Paul：今日快捷入口 -->
        <div v-if="dashboardCards.find(c=>c.id===\'shortcuts\')?.visible" class="shortcuts-grid" style="margin-bottom:8px;">
          <div v-for="item in [{page:\'projects\',icon:\'folder-open\',label:\'项目\',color:\'var(--info)\'},{page:\'tasks\',icon:\'check-square\',label:\'任务\',color:\'var(--success)\'},{page:\'customers\',icon:\'users\',label:\'客户\',color:\'var(--primary)\'},{page:\'issues\',icon:\'alert-triangle\',label:\'问题\',color:\'var(--warning)\'},{page:\'meetings\',icon:\'calendar\',label:\'会议\',color:\'var(--danger)\'},{page:\'ai\',icon:\'bot\',label:\'AI助手\',color:\'var(--primary-light)\'}]" :key="item.page"
            @click="currentPage=item.page"
            style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 8px;background:var(--card);border-radius:12px;cursor:pointer;border:1px solid var(--border);transition:all .2s;"
            @mouseover="$event.currentTarget.style.background=\'var(--bg-hover)\';$event.currentTarget.style.borderColor=item.color"
            @mouseout="$event.currentTarget.style.background=\'var(--card)\';$event.currentTarget.style.borderColor=\'var(--border)\'">
            <i :data-lucide="item.icon" style="width:20px;height:20px;" :style="{color:item.color}"></i>
            <span style="font-size:12px;color:var(--text);">{{item.label}}</span>
          </div>
        </div>'''

new_shortcuts_html = '''        <!-- 快捷入口横排导航 -->
        <div v-if="dashboardCards.find(c=>c.id===\'shortcuts\')?.visible" class="shortcuts-grid" style="margin-bottom:8px;">
          <div v-for="item in [{page:\'projects\',icon:\'folder-open\',label:\'项目\',color:\'var(--info)\'},{page:\'tasks\',icon:\'check-square\',label:\'任务\',color:\'var(--success)\'},{page:\'customers\',icon:\'users\',label:\'客户\',color:\'var(--primary)\'},{page:\'issues\',icon:\'alert-triangle\',label:\'问题\',color:\'var(--warning)\'},{page:\'meetings\',icon:\'calendar\',label:\'会议\',color:\'var(--danger)\'},{page:\'ai\',icon:\'bot\',label:\'AI助手\',color:\'var(--primary-light)\'}]" :key="item.page"
            @click="currentPage=item.page"
            :class="{active:currentPage===item.page}"
            :style="{\'border-bottom\':currentPage===item.page?\'2px solid \'+item.color:\'2px solid transparent\',\'background\':currentPage===item.page?\'rgba(99,102,241,0.08)\':\'transparent\'}"
            style="display:flex;align-items:center;gap:6px;padding:8px 14px;background:var(--card);border-radius:8px;cursor:pointer;border:1px solid var(--border);transition:all .2s;flex-shrink:0;">
            <i :data-lucide="item.icon" style="width:16px;height:16px;" :style="{color:item.color}"></i>
            <span style="font-size:13px;color:var(--text);font-weight:500;">{{item.label}}</span>
          </div>
        </div>'''

if old_shortcuts_html in content:
    content = content.replace(old_shortcuts_html, new_shortcuts_html)
    print('OK: 快捷入口HTML改为横排导航')
else:
    print('WARN: 快捷入口HTML未完全匹配，尝试部分匹配...')
    # Try to find the start of the shortcuts section
    start_marker = '<!-- Paul：今日快捷入口 -->'
    if start_marker in content:
        pos = content.find(start_marker)
        end_marker = '<!-- 底部 AI 数据识别区 -->'
        end_pos = content.find(end_marker, pos)
        print(f'  找到快捷入口块：位置 {pos} - {end_pos}')
        print(f'  内容片段：{content[pos:pos+200]}')
    else:
        print('  完全找不到快捷入口')

# Step 3: 添加快捷入口的active样式
active_css = """
/* 快捷入口导航active状态 */
.shortcuts-grid .active{
  background:rgba(99,102,241,0.08)!important;
  border-color:var(--primary)!important;
}"""

if '.shortcuts-grid .active' not in content:
    # Insert before .dashboard-ai-section comment
    insert_pos = content.find('/* ============================================\n   7.6 仪表盘AI区域')
    if insert_pos > 0:
        content = content[:insert_pos] + active_css + '\n' + content[insert_pos:]
        print('OK: 添加快捷入口active样式')
    else:
        print('WARN: 未找到插入位置')
else:
    print('OK: active样式已存在')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'完成，文件长度: {len(content)} chars')
