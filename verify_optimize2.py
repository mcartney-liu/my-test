with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('risk-health-grid CSS', 'risk-health-grid{display:grid;grid-template-columns:1fr'),
    ('risk-health-grid HTML', 'class="risk-health-grid" style'),
    ('shortcuts-grid CSS', 'shortcuts-grid{display:grid;grid-template-columns:repeat(3,1fr)'),
    ('shortcuts-grid HTML', 'class="shortcuts-grid"'),
    ('任务类型标签', 't.type'),
    ('卡片进度条宽度', '.card-progress-mini{width:60px'),
    ('卡片底部间距(gap)', 'gap:8px'),
]

for name, pattern in checks:
    if pattern in content:
        print(f'OK  {name}')
    else:
        print(f'MISS {name}')
