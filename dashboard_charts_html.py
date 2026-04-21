with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 仪表盘图表数据 + HTML 插入
# ============================================================

# ---- Step 1: 添加图表数据computed ----
chart_data = '''
    // 【Dashboard】图表数据
    const dashTaskStatusPie=computed(()=>{
      const statuses=['pending','in-progress','review','done','blocked'];
      const names=['待处理','进行中','审核中','已完成','已阻塞'];
      return statuses.map((s,i)=>({
        label:names[i],
        value:tasks.value.filter(t=>t.status===s).length
      })).filter(d=>d.value>0);
    });
    const dashProjectProgressBar=computed(()=>{
      return projects.value.slice(0,6).map(p=>{
        const detail=getProjectDetail(p.id);
        const total=detail?detail.stats.totalTasks:0;
        const done=detail?detail.stats.completedTasks:0;
        return{label:p.name.slice(0,6),value:total,done};
      });
    });
    const dashWeeklyTrendLine=computed(()=>{
      const days=7;
      const now=new Date();
      const result=[];
      for(let i=days-1;i>=0;i--){
        const d=new Date(now);d.setDate(d.getDate()-i);
        const dateStr=`${d.getMonth()+1}/${d.getDate()}`;
        const dayTasks=tasks.value.filter(t=>{
          const cd=new Date(t.createdAt||Date.now());
          return cd.toDateString()===d.toDateString();
        });
        const dayDone=tasks.value.filter(t=>{
          if(!t.completedAt)return false;
          const cd=new Date(t.completedAt);
          return cd.toDateString()===d.toDateString();
        });
        result.push({date:dateStr,v1:dayTasks.length,v2:dayDone.length});
      }
      return result;
    });
    const dashTeamWorkloadBar=computed(()=>{
      return members.value.slice(0,8).map(m=>{
        const memberTasks=tasks.value.filter(t=>t.assignee===m.name);
        return{label:m.name,vlaue:memberTasks.length};
      }).filter(d=>d.vlaue>0);
    });

'''

# 在 projectHealthList 定义后添加
health_end = content.find('    // AI Configuration')
if health_end > 0:
    content = content[:health_end] + chart_data + content[health_end:]
    print('OK: 添加图表数据computed')
else:
    print('ERROR: 未找到插入位置')

# ---- Step 2: 添加仪表盘图表HTML ----
# 在 stats-grid 统计卡片后，风险面板前插入
chart_html = '''
        <!-- 仪表盘可视化图表区 -->
        <div v-if="dashboardCards.find(c=>c.id==='charts')?.visible" class="dash-charts-grid">
          <!-- 任务状态饼图 -->
          <div class="dash-chart-card">
            <h4><i data-lucide="pie-chart" style="color:var(--primary);"></i>任务状态分布</h4>
            <div class="dash-chart-svg">
              <svg width="160" height="160" viewBox="0 0 160 160" v-html="miniPieSvg(dashTaskStatusPie)"></svg>
            </div>
          </div>
          <!-- 项目进度条形图 -->
          <div class="dash-chart-card">
            <h4><i data-lucide="bar-chart-2" style="color:var(--info);"></i>项目进度</h4>
            <div class="dash-chart-svg" v-html="dashProjectProgressBar.length?miniBarSvg(dashProjectProgressBar.map(d=>({label:d.label,value:d.value}))):'<div style=color:var(--muted);font-size:12px;text-align:center;padding:40px 0>暂无项目数据</div>'"></div>
          </div>
          <!-- 本周趋势折线图 -->
          <div class="dash-chart-card">
            <h4><i data-lucide="trending-up" style="color:var(--success);"></i>本周趋势</h4>
            <div class="dash-chart-svg" v-html="miniLineSvg(dashWeeklyTrendLine)"></div>
          </div>
          <!-- 团队工作量分布 -->
          <div class="dash-chart-card">
            <h4><i data-lucide="users" style="color:var(--warning);"></i>团队工作量</h4>
            <div class="dash-chart-svg" v-html="dashTeamWorkloadBar.length?miniTeamSvg(dashTeamWorkloadBar.map(d=>({label:d.label,vlaue:d.vlaue}))):'<div style=color:var(--muted);font-size:12px;text-align:center;padding:40px 0>暂无成员数据</div>'"></div>
          </div>
        </div>

'''

# 在 stats-grid 结束后的风险面板前插入
# 找到统计卡片结束 + 风险面板开始之间的位置
stats_end_marker = '<!-- Paul：风险预警面板 + 项目健康度 (移动端单列) -->'
pos = content.find(stats_end_marker)
if pos > 0:
    # 找到统计卡片区域的结束（</div> 关闭 stats-grid）
    grid_close = content.rfind('</div>', 0, pos)
    if grid_close > 0:
        content = content[:grid_close] + '\n' + chart_html + content[grid_close:]
        print(f'OK: 添加图表HTML (位置 {grid_close})')
    else:
        print('WARN: 未找到stats-grid结束标签')
else:
    print('ERROR: 未找到风险面板标记')

# ---- Step 3: 修复 dashTeamWorkloadBar 的变量名拼写错误 ----
# 原始代码中 vlaue 是错误的，应该是 value
content = content.replace("vlaue:memberTasks.length", "value:memberTasks.length")
content = content.replace("d.vlaue>0", "d.value>0")
content = content.replace("dashTeamWorkloadBar.map(d=>({label:d.label,vlaue:d.vlaue}))", "dashTeamWorkloadBar.map(d=>({label:d.label,value:d.value}))")
print('OK: 修复变量名拼写')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'完成，文件长度: {len(content)} chars')
