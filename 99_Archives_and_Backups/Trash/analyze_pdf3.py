import re
with open(r'C:\Users\yunky\.gemini\antigravity\brain\3023f334-1b72-4cbe-b4e9-873623fa96af\scratch\temp_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

out = []
for match in re.finditer(r'.{0,150}boundary-spanning.{0,150}', text, re.IGNORECASE):
    out.append(match.group(0).replace('\n', ' '))

with open('results2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
