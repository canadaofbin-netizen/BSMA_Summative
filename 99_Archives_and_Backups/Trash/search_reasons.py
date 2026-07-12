import json
import re
from pathlib import Path

for md in Path(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\03_Coding_Rulebook').glob('*.md'):
    text = md.read_text(encoding='utf-8')
    if 'Exclude' in text or 'exclusion' in text.lower():
        print(f"--- {md.name} ---")
        lines = text.split('\n')
        for line in lines:
            if 'exclude' in line.lower() or 'exclusion' in line.lower() or 'reason' in line.lower():
                print(line)
