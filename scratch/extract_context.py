import re

text = open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\BSMA0099.txt', encoding='utf-8').read()

def find_context(keywords, window=1000):
    for kw in keywords:
        matches = [m.start() for m in re.finditer(r'(?i)\b' + kw + r'\b', text)]
        for i, match in enumerate(matches[:3]):
            start = max(0, match - 200)
            end = min(len(text), match + window)
            print(f"--- Context for {kw} ({i+1}) ---")
            print(text[start:end])
            print("\n" + "="*50 + "\n")

find_context(['ABSTRACT', 'participants', 'sample', 'correlation'])
