with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
m = re.findall(r'\[data-theme="[^"]+"\]', content)
print('Theme selectors found:')
for item in m[:10]:
    print(' ', item)

# Check if dark theme block exists
if '[data-theme="dark"]' in content:
    print('\nOK: [data-theme="dark"] block exists')
    # Find its position
    pos = content.find('[data-theme="dark"]')
    print(f'   Position: {pos}')
    # Show first few lines
    block = content[pos:pos+200]
    print('   Content preview:', block[:100])
else:
    print('\nERROR: [data-theme="dark"] block NOT found')

if 'initTheme' in content:
    print('\nOK: initTheme function exists')
