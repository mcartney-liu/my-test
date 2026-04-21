with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all </script> occurrences
matches = [(m.start(), content[max(0,m.start()-80):m.start()+20]) for m in re.finditer(r'</script>', content)]
print(f'Found {len(matches)} </script> tags:')
for pos, ctx in matches:
    line_num = content[:pos].count('\n') + 1
    print(f'  Line {line_num}: ...{ctx.replace(chr(10), " ")}...')

# Find document.write with </script> in string
doc_write = re.findall(r'.{0,100}document\.write[^;]*</scr[^>]*>[^;]*;.{0,50}', content)
print(f'\ndocument.write with </script>: {len(doc_write)}')
for dw in doc_write:
    line_num = content[:content.find(dw[:50])].count('\n') + 1
    print(f'  Line {line_num}: {dw[:100]}')
