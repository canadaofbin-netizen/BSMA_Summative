import re
import sys

with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\BSMA0099.txt', encoding='utf-8') as f:
    text = f.read()

out_lines = []
matches = re.finditer(r'(?i)Independent Variable', text)
for m in matches:
    start = max(0, m.start() - 1000)
    end = min(len(text), m.start() + 2000)
    out_lines.append(f"MATCH AT {m.start()}")
    out_lines.append(text[start:end])
    out_lines.append("="*50)

with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\iv_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
