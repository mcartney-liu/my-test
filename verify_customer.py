import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 验证关键代码
checks = [
    'customerSearchKey',
    'customerFilterStatus',
    'filteredCustomers',
    'getCustomerProjects',
    'addCustomerActivity',
    'formData.status',
    'formData.level',
    'formData.email',
    'formData.address',
    'formData.notes',
    'getCustomerProjects=(customerId)',
    'addCustomerActivity=()',
]

print('=== 客户管理增强验证 ===')
for check in checks:
    if check in content:
        pos = content.find(check)
        line_num = content[:pos].count('\n') + 1
        print(f'  OK: {check} (L{line_num})')
    else:
        print(f'  MISSING: {check}')

# 验证状态映射
print('\n=== 状态显示映射 ===')
if "status==='active'?'活跃'" in content:
    print('  OK: active -> 活跃')
if "status==='prospect'?'潜在'" in content:
    print('  OK: prospect -> 潜在')
if "status==='inactive'?'休眠'" in content:
    print('  OK: inactive -> 休眠')
if "status==='churned'?'流失'" in content:
    print('  OK: churned -> 流失')

# 检查detail view是否包含关联项目
if 'getCustomerProjects' in content:
    pos = content.find('getCustomerProjects')
    ctx = content[pos:pos+200].replace('\n', ' ')
    print(f'\ngetCustomerProjects: {ctx[:100]}')
