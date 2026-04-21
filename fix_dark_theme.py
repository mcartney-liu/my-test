with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. 添加 [data-theme="dark"] CSS 变量块
# 2. 完善 initTheme 的 auto 模式
# ============================================================

# ---- 1. 深色主题CSS块 ----
# 在 [data-theme="light"] 块后面添加 [data-theme="dark"]
dark_theme_css = '''
/* ============================================
   1.2 深色主题 - Dark Theme
   ============================================ */
[data-theme="dark"] {
  --bg: #0f172a;
  --bg-soft: #1e293b;
  --bg-card: #1e293b;
  --bg-hover: rgba(255, 255, 255, 0.05);
  --bg-active: rgba(255, 255, 255, 0.08);
  --card: #1e293b;

  --text-primary: #f1f5f9;
  --text-secondary: #e2e8f0;
  --text-muted: #94a3b8;
  --text-hint: #64748b;

  --border: #334155;
  --border-light: #475569;

  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.6);

  --glass-bg: rgba(30, 41, 59, 0.85);
  --glass-border: rgba(255, 255, 255, 0.08);
  --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
}

/* ============================================
   1.3 自动跟随系统主题 - Auto Theme
   ============================================ */
'''

# 在 [data-theme="light"] 块结束后插入
light_end = content.find('[data-theme="light"] {')
if light_end > 0:
    # 找到 [data-theme="light"] 块的结束（下一个 /* 或 @ 或 </style>）
    block_end = content.find('/* ============================================\n   2.', light_end)
    if block_end > 0:
        content = content[:block_end] + dark_theme_css + content[block_end:]
        print(f'OK: 添加深色主题CSS块 (位置 {block_end})')
    else:
        print('ERROR: 未找到[light]块结束位置')
else:
    print('ERROR: 未找到[light]块')

# ---- 2. 修复 initTheme - 确保auto模式正确处理 ----
old_init_theme = '''const initTheme=()=>{
      const savedTheme=localStorage.getItem('pm-os-theme');
      if(savedTheme==='auto'||!savedTheme){
        // 跟随系统主题
        const prefersDark=window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark?'dark':'light');
        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',e=>{
          if(localStorage.getItem('pm-os-theme')==='auto'){
            setTheme(e.matches?'dark':'light');
          }
        });
      }else{
        setTheme(savedTheme);
      }
    };'''

new_init_theme = '''const initTheme=()=>{
      const savedTheme=localStorage.getItem('pm-os-theme');
      // auto或未设置时：跟随系统主题
      if(savedTheme==='auto'||!savedTheme){
        const prefersDark=window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme',prefersDark?'dark':'light');
        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',e=>{
          const cur=localStorage.getItem('pm-os-theme');
          if(cur==='auto'||!cur){
            document.documentElement.setAttribute('data-theme',e.matches?'dark':'light');
          }
        });
      }else{
        // 手动选择的主题直接应用属性
        document.documentElement.setAttribute('data-theme',savedTheme);
      }
    };'''

if old_init_theme in content:
    content = content.replace(old_init_theme, new_init_theme)
    print('OK: 修复 initTheme')
else:
    # 尝试模糊匹配
    if 'const initTheme=()=>{' in content:
        print('WARN: initTheme内容不完全匹配，可能已被修改')

# ---- 3. 添加auto主题选项的CSS（跟随系统时显示当前系统对应主题）----
# setTheme函数已正确设置data-theme，auto模式由initTheme处理
# 但需要在设置页面显示auto为active状态
# 找到setTheme函数，在其中添加auto处理
old_set_theme = '''    const setTheme=(theme)=>{
      document.documentElement.setAttribute('data-theme',theme);
      localStorage.setItem('pm-os-theme',theme);
      currentTheme.value=theme;
      // 更新胶囊按钮状态
      document.querySelectorAll('.segment-item[data-theme]').forEach(item=>{
        item.classList.toggle('active',item.getAttribute('data-theme')===theme);
      });
      nextTick(()=>{if(window.lucide)lucide.createIcons()});
    };'''

new_set_theme = '''    const setTheme=(theme)=>{
      document.documentElement.setAttribute('data-theme',theme);
      localStorage.setItem('pm-os-theme',theme);
      currentTheme.value=theme;
      // 更新胶囊按钮状态（包括auto按钮）
      document.querySelectorAll('.segment-item').forEach(item=>{
        const t=item.getAttribute('data-theme');
        if(t==='auto'){
          item.classList.toggle('active',localStorage.getItem('pm-os-theme')==='auto');
        }else{
          item.classList.toggle('active',t===theme);
        }
      });
      nextTick(()=>{if(window.lucide)lucide.createIcons()});
    };'''

if old_set_theme in content:
    content = content.replace(old_set_theme, new_set_theme)
    print('OK: 修复 setTheme auto处理')
else:
    print('WARN: setTheme内容不完全匹配')

with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'完成，文件长度: {len(content)} chars')
