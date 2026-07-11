import re
with open(r'C:\Users\yunky\.gemini\antigravity\brain\3023f334-1b72-4cbe-b4e9-873623fa96af\scratch\temp_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

out = []
out.append("--- BOUNDARY SPANNING ---")
for match in re.finditer(r'.{0,100}boundary.{0,10}spanning.{0,100}', text, re.IGNORECASE):
    out.append(match.group(0).replace('\n', ' '))

out.append("\n--- MEANS, SD, CORRELATION ---")
for match in re.finditer(r'.{0,100}standard deviation.{0,100}', text, re.IGNORECASE):
    out.append(match.group(0).replace('\n', ' '))
for match in re.finditer(r'.{0,100}correlation.{0,100}', text, re.IGNORECASE):
    out.append(match.group(0).replace('\n', ' '))
for match in re.finditer(r'.{0,100}matrix.{0,100}', text, re.IGNORECASE):
    out.append(match.group(0).replace('\n', ' '))

with open('results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
