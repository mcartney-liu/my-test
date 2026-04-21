import re

with open('C:/Users/haizhi/Projects/my-test/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check theme-related CSS
dark_css = re.findall(r'\[data-theme="dark"\][^{]*\{[^}]*\}', content)
auto_css = re.findall(r'\[data-theme="auto"\][^{]*\{[^}]*\}', content)
print(f'Dark CSS blocks: {len(dark_css)}')
print(f'Auto CSS blocks: {len(auto_css)}')

# Check what colors are used in dark mode
dark_sections = re.findall(r'(\[data-theme="dark"\][^@]*?\{[^}]*\})', content, re.DOTALL)
print(f'Dark mode color blocks: {len(dark_sections)}')

# Check for common dark mode variables
dark_vars = re.findall(r'--bg-dark|--text-dark|--card-dark|--surface-dark', content)
print(f'Dark-specific variables: {len(dark_vars)}')

# Check for var(--bg) usage vs hardcoded colors
# Count CSS variables vs hardcoded colors in dark mode sections
dark_content = '\n'.join(dark_sections[:3])
print(f'\nSample dark CSS (first block, 500 chars):\n{dark_content[:500]}')
