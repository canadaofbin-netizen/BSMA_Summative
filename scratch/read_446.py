import fitz
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

filepath = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[446] Onishi (2016) - Measuring nurse managers' boundary spanning development and psychometric evaluation.pdf"
doc = fitz.open(filepath)
text = "\n".join([page.get_text() for page in doc])
print(f"Total length: {len(text)}")
print("\n--- TABLES/MATRICES ---")
for match in re.finditer(r'Table \d+.*?(?=(Table \d+|$))', text, re.DOTALL | re.IGNORECASE):
    print(match.group(0)[:1500])
    print("\n----------------\n")

print("\n--- CORRELATIONS ---")
for match in re.findall(r'.{0,100}correlat.{0,100}', text, re.IGNORECASE):
    print(match)
