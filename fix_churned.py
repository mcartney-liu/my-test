import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix churned status display in detail view
old = "formData.status==='inactive'?'休眠':formData.status"
new = "formData.status==='inactive'?'休眠':formData.status==='churned'?'流失':formData.status"

if old in content:
    content = content.replace(old, new, 1)
    with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: Fixed churned status display')
else:
    print('Already fixed or not found')

# Also add churned badge styling check
if "badge-danger'" in content:
    pos = content.find("formData.status==='churned'?'badge")
    if pos < 0:
        # Add churned to card badge
        old_card_badge = "c.status==='inactive'?'badge-gray':'badge-danger'"
        new_card_badge = "c.status==='inactive'?'badge-gray':c.status==='churned'?'badge-danger':'badge-danger'"
        if old_card_badge in content:
            content = content.replace(old_card_badge, new_card_badge, 1)
            with open('C:/Users/haizhi/Projects/my-test/index.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('OK: Fixed churned badge in card')
        else:
            print('Card badge pattern not found')
