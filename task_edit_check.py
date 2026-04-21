import re

with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check what we have
if '<!-- Task Edit Form -->' in content:
    print('OK: Task Edit Form marker found')
else:
    print('MISSING: Task Edit Form marker')
    
if "modalType==='task' && modalTitle==='编辑任务'" in content:
    print('OK: edit form condition found')
else:
    print('MISSING: edit form condition')
    
if "modalType==='task' && modalTitle==='新建任务'" in content:
    print('OK: add form condition found')
else:
    print('MISSING: add form condition')

if 'task-est-hours-edit' in content:
    print('OK: new estimated hours field found')
else:
    print('MISSING: new estimated hours field')

if 'v-if="formData.id"' in content:
    print('Found old v-if formData.id pattern')

# Find the exact start of task edit form
idx = content.find('<!-- Task Edit Form -->')
if idx >= 0:
    print(f'Task Edit Form starts at char {idx}')
    snippet = content[idx:idx+500]
    print(repr(snippet[:200]))
