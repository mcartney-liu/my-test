with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

edit_form = '<!-- Task Edit Form -->'
add_form = '<!-- Task Add Form -->'

edit_pos = content.find(edit_form)
add_pos = content.find(add_form)

print(f'Task Edit Form at: {edit_pos}')
print(f'Task Add Form at: {add_pos}')
print(f'edit_pos < add_pos: {edit_pos < add_pos}')

# Get snippet around edit form
if edit_pos >= 0:
    print(f'\nSnippet around Task Edit Form:')
    print(repr(content[edit_pos-50:edit_pos+200]))

# Find where Task Add Form ENDS
add_end = content.find('</form>', add_pos)
print(f'\nTask Add Form ends at: {add_end}')
print(f'After Task Add Form: {repr(content[add_end:add_end+200])}')

# The next marker after Task Add Form
for marker in ['<!-- 模板面板', '<!-- Task Add Form -->', '<!-- 批量操作']:
    pos = content.find(marker, add_end)
    if pos >= 0:
        print(f'\nNext marker after add form: {marker!r} at {pos}')
