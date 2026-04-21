with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到仪表盘section中的快捷入口和欢迎栏位置
dash_start = content.find('<div v-if="currentPage===\'dashboard\'">')
dash_end = content.find('<!-- Projects -->', dash_start)
dash_content = content[dash_start:dash_end]

# 找到快捷入口块的起止
shortcuts_start = dash_content.find('<!-- 快捷入口横排导航 -->')
shortcuts_end = dash_content.find('<!-- 底部 AI 数据识别区 -->', shortcuts_start)

# 找到欢迎栏的起止（在其前有个注释分隔）
welcome_start = dash_content.find('<!-- 顶部欢迎栏 -->')
# welcome区域从注释到统计卡片之前
stats_start = dash_content.find('<!-- 中间数据统计卡片区 -->')

if shortcuts_start > 0 and welcome_start > 0 and stats_start > 0:
    # 提取快捷入口块
    shortcuts_block = dash_content[shortcuts_start:shortcuts_end]
    # 提取欢迎栏+统计卡片之间的部分
    welcome_stats_block = dash_content[welcome_start:stats_start]
    
    # 从dash_content中删除快捷入口块
    dash_content_no_shortcuts = dash_content[:shortcuts_start] + dash_content[shortcuts_end:]
    
    # 找到欢迎栏在删除快捷入口后的新位置
    new_welcome_start = dash_content_no_shortcuts.find('<!-- 顶部欢迎栏 -->')
    new_stats_start = dash_content_no_shortcuts.find('<!-- 中间数据统计卡片区 -->', new_welcome_start)
    
    # 把快捷入口插入到欢迎栏前面
    new_dash = (dash_content_no_shortcuts[:new_welcome_start] 
                + shortcuts_block 
                + '\n        '  # 保持缩进
                + dash_content_no_shortcuts[new_welcome_start:])
    
    # 重新组装
    new_content = content[:dash_start] + new_dash + content[dash_end:]
    
    with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('OK: 快捷入口已移到欢迎栏上方')
    print(f'  快捷入口位置: 原来在统计卡片后 -> 现在在欢迎栏前')
    print(f'  文件长度: {len(new_content)} chars')
else:
    print('ERROR: 未能找到关键标记')
    print(f'  shortcuts_start={shortcuts_start}, welcome_start={welcome_start}, stats_start={stats_start}')
