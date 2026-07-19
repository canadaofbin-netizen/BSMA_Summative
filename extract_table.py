import re
with open('temp_663.txt', 'r', encoding='utf-8') as f:
    text = f.read()

out = []
match = re.search(r'(?is)(Table 1.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n)', text)
if match:
    out.append(match.group(0))
else:
    idx = text.find('Table 1')
    out.append(text[idx:idx+2500])

with open('table1.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
