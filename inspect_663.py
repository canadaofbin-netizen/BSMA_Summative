import re
with open('temp_663.txt', 'r', encoding='utf-8') as f:
    text = f.read()

out = []
out.append("--- ABSTRACT ---")
out.append(text[:2500])

out.append("\n\n--- METHODOLOGY ---")
match = re.search(r'(?i)(Methodology|Methods?|Sample|Data collection|Participants?)', text[2500:])
if match:
    start = match.start() + 2500
    out.append(text[start:start+4000])
    
    out.append("\n\n--- MEASURES ---")
    match2 = re.search(r'(?i)(Measures|Measurement)', text[start:])
    if match2:
        start2 = match2.start() + start
        out.append(text[start2:start2+4000])

with open('inspect_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
