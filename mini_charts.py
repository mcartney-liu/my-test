with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 仪表盘可视化增强
# 1. 添加mini图表CSS
# 2. 添加mini图表生成函数（miniPieSvg, miniBarSvg, miniLineSvg）
# 3. 添加dashboard卡片HTML（4个可视化卡片）
# ============================================================

# ---- 1. 添加mini图表CSS ----
mini_css = '''
/* 仪表盘迷你图表 */
.dash-charts-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px;}
.dash-chart-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px;transition:all .2s;}
.dash-chart-card:hover{box-shadow:0 4px 12px rgba(0,0,0,0.15);transform:translateY(-1px);}
.dash-chart-card h4{font-size:12px;font-weight:600;color:var(--text-muted);margin:0 0 8px;display:flex;align-items:center;gap:6px;}
.dash-chart-card h4 i{width:14px;height:14px;}
.dash-chart-svg{display:flex;justify-content:center;align-items:center;}

@media(max-width:1200px){
  .dash-charts-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:768px){
  .dash-charts-grid{grid-template-columns:repeat(2,1fr);gap:6px}
}
@media(max-width:480px){
  .dash-charts-grid{grid-template-columns:1fr}
}
'''

# 找到报表中心样式结束位置，在那之前插入
insert_pos = content.find('/* ===== 报表中心样式 ===== */')
if insert_pos > 0:
    # 找到这个区块开始
    prev_pos = content.rfind('\n/* =====', 0, insert_pos)
    content = content[:prev_pos] + mini_css + '\n\n' + content[prev_pos:]
    print(f'OK: 添加mini图表CSS，位置 {prev_pos}')
else:
    # 备用位置：统计卡片CSS附近
    pos = content.find('.stats-grid{')
    if pos > 0:
        content = content[:pos] + mini_css + '\n' + content[pos:]
        print(f'OK: 添加mini图表CSS（备用位置）')
    else:
        print('ERROR: 未找到插入位置')

# ---- 2. 添加mini图表生成函数 ----
# 在 pieSvgPaths 函数后面添加
pie_func_pos = content.find('    const pieSvgPaths=(data,size=200)=>{')
if pie_func_pos > 0:
    # 找到这个函数的结束位置
    end_pos = content.find('\n    // --- 趋势', pie_func_pos)
    if end_pos < 0:
        end_pos = content.find('\n    const pieSvgPaths', pie_func_pos + 100)
    
    mini_funcs = '''
    // --- 仪表盘迷你饼图SVG ---
    const miniPieSvg=(data,size=160)=>{
      if(!data||!data.length)return'<text x="50%" y="50%" text-anchor="middle" fill="var(--muted)" font-size="11">暂无数据</text>';
      const total=data.reduce((s,d)=>s+d.value,0);
      if(total===0)return'<text x="50%" y="50%" text-anchor="middle" fill="var(--muted)" font-size="11">暂无数据</text>';
      const cx=size/2,cy=size/2,r=size/2-8;
      let paths='',cur=0;
      const colors=['#6366f1','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#f97316'];
      data.forEach((d,i)=>{
        const start=cur/total*2*Math.PI-Math.PI/2;
        const end=(cur+d.value)/total*2*Math.PI-Math.PI/2;
        const x1=cx+r*Math.cos(start),y1=cy+r*Math.sin(start);
        const x2=cx+r*Math.cos(end),y2=cy+r*Math.sin(end);
        const large=(d.value/total>0.5)?1:0;
        paths+=`<path d="M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${large},1 ${x2},${y2} Z" fill="${colors[i%colors.length]}" opacity="0.85"/>`;
        cur+=d.value;
      });
      // 中心白圆
      paths+=`<circle cx="${cx}" cy="${cy}" r="${r*0.5}" fill="var(--card)"/>`;
      // 中心文字
      paths+=`<text x="${cx}" y="${cy-4}" text-anchor="middle" font-size="12" font-weight="700" fill="var(--text)">${total}</text>`;
      paths+=`<text x="${cx}" y="${cy+12}" text-anchor="middle" font-size="8" fill="var(--muted)">总计</text>`;
      return paths;
    };
    
    // --- 仪表盘迷你水平条形图SVG ---
    const miniBarSvg=(data,width=280,height=140)=>{
      if(!data||!data.length)return'<text x="50%" y="50%" text-anchor="middle" fill="var(--muted)" font-size="11">暂无数据</text>';
      const colors=['#6366f1','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4'];
      const pad={t:5,r:10,b:25,l:5};
      const cw=width-pad.l-pad.r,ch=height-pad.t-pad.b;
      const barH=Math.min(14,Math.floor(ch/data.length)-4);
      const gap=Math.floor((ch-barH*data.length)/data.length);
      let svg=`<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`;
      data.slice(0,6).forEach((d,i)=>{
        const bw=(d.value/Math.max(...data.map(x=>x.value),1))*cw;
        const y=pad.t+i*(barH+gap);
        svg+=`<rect x="${pad.l}" y="${y}" width="${bw}" height="${barH}" rx="3" fill="${colors[i%colors.length]}" opacity="0.8"/>`;
        svg+=`<text x="${pad.l+bw+4}" y="${y+barH/2+4}" font-size="9" fill="var(--muted)">${d.label}</text>`;
        svg+=`<text x="${bw}" y="${y+barH/2+4}" text-anchor="end" font-size="9" font-weight="600" fill="var(--text)">${d.value}</text>`;
      });
      svg+='</svg>';
      return svg;
    };
    
    // --- 仪表盘迷你趋势折线图SVG ---
    const miniLineSvg=(data,width=280,height=100)=>{
      if(!data||data.length<2)return'<text x="50%" y="50%" text-anchor="middle" fill="var(--muted)" font-size="11">数据不足</text>';
      const pad={t:8,r:8,b:20,l:8};
      const cw=width-pad.l-pad.r,ch=height-pad.t-pad.b;
      const maxV=Math.max(...data.map(d=>Math.max(d.v1,d.v2)),1);
      const step=cw/(data.length-1);
      const pts1=data.map((d,i)=>`${pad.l+i*step},${pad.t+ch-d.v1/maxV*ch}`).join(' ');
      const pts2=data.map((d,i)=>`${pad.l+i*step},${pad.t+ch-d.v2/maxV*ch}`).join(' ');
      let svg=`<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`;
      // 网格
      for(let i=0;i<=3;i++){
        const y=pad.t+ch-ch*i/3;
        svg+=`<line x1="${pad.l}" y1="${y}" x2="${width-pad.r}" y2="${y}" stroke="var(--border)" stroke-width="0.5" stroke-dasharray="2,2"/>`;
        svg+=`<text x="${pad.l-2}" y="${y+3}" text-anchor="end" font-size="8" fill="var(--muted)">${Math.round(maxV*i/3)}</text>`;
      }
      // 线
      svg+=`<polyline points="${pts1}" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round"/>`;
      svg+=`<polyline points="${pts2}" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>`;
      // 点
      data.forEach((d,i)=>{
        svg+=`<circle cx="${pad.l+i*step}" cy="${pad.t+ch-d.v1/maxV*ch}" r="2.5" fill="#6366f1"/>`;
        svg+=`<circle cx="${pad.l+i*step}" cy="${pad.t+ch-d.v2/maxV*ch}" r="2.5" fill="#10b981"/>`;
      });
      // 图例
      svg+=`<circle cx="${width-pad.r-50}" cy="${pad.t+10}" r="3" fill="#6366f1"/><text x="${width-pad.r-44}" y="${pad.t+13}" font-size="8" fill="var(--muted)">新建</text>`;
      svg+=`<circle cx="${width-pad.r-10}" cy="${pad.t+10}" r="3" fill="#10b981"/><text x="${width-pad.r-4}" y="${pad.t+13}" font-size="8" fill="var(--muted)">完成</text>`;
      svg+='</svg>';
      return svg;
    };
    
    // --- 仪表盘团队任务分布图 ---
    const miniTeamSvg=(data,width=280,height=100)=>{
      if(!data||!data.length)return'<text x="50%" y="50%" text-anchor="middle" fill="var(--muted)" font-size="11">暂无数据</text>';
      const colors=['#6366f1','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#f97316','#84cc16'];
      const maxV=Math.max(...data.map(d=>d.value),1);
      let svg=`<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`;
      const barH=8,gap=6;
      const totalH=Math.min(data.length,8)*(barH+gap)+8;
      const startY=(height-totalH)/2;
      data.slice(0,8).forEach((d,i)=>{
        const bw=(d.value/maxV)*(width-80);
        const y=startY+i*(barH+gap);
        svg+=`<rect x="60" y="${y}" width="${bw}" height="${barH}" rx="4" fill="${colors[i%colors.length]}" opacity="0.75"/>`;
        svg+=`<text x="58" y="${y+barH/2+3}" text-anchor="end" font-size="8" fill="var(--muted)">${d.label.slice(0,4)}</text>`;
        svg+=`<text x="${60+bw+4}" y="${y+barH/2+3}" font-size="8" font-weight="600" fill="var(--text)">${d.value}</text>`;
      });
      svg+='</svg>';
      return svg;
    };
    
'''
    # 在 pieSvgPaths 函数结束处插入
    # 找到 pieSvgPaths 函数结束
    func_end = content.find('return svg;', pie_func_pos)
    func_end = content.find('\n    // ---', func_end)
    if func_end > 0:
        content = content[:func_end] + mini_funcs + content[func_end:]
        print(f'OK: 添加mini图表函数')
    else:
        print(f'WARN: 未找到插入位置，pieSvgPaths位置={pie_func_pos}')
        # 尝试备用位置
        func_end = content.find('\n    const pieSvgPaths', pie_func_pos+10)
        if func_end > 0:
            content = content[:func_end] + mini_funcs + content[func_end:]
            print(f'OK: 添加mini图表函数（备用）')

# ---- 3. 注册mini图表函数到return ----
return_pos = content.rfind('return {')
if return_pos > 0:
    # 在 return { 中添加新函数
    new_exports = '''    miniPieSvg,miniBarSvg,miniLineSvg,miniTeamSvg,
    '''
    # 找到第一个导出属性
    first_prop = content.find('\n    }', return_pos)
    if first_prop > 0:
        content = content[:first_prop] + '\n    ' + new_exports + content[first_prop:]
        print('OK: 注册mini图表函数')
    else:
        print('WARN: 未找到return块')

# ---- 4. 添加dashboardCards的id定义 ----
# 在 dashboardCards 定义中添加 id='charts'
cards_def = "      {id:'ai',label:'AI数据识别',visible:true}"
if "id:'charts'" not in content:
    # 在 ai 卡片前添加 charts 卡片
    pos = content.find(cards_def)
    if pos > 0:
        charts_def = "      {id:'charts',label:'可视化图表',visible:true},\n"
        content = content[:pos] + charts_def + content[pos:]
        print('OK: 添加dashboardCards的charts定义')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'完成，文件长度: {len(content)} chars')
