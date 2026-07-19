import PyPDF2
import re
reader = PyPDF2.PdfReader(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[399] Marrone et al. (2007) - A Multilevel Investigation of Antecedents and Consequences of Team Member BSB.pdf')
text = '\n'.join(page.extract_text() for page in reader.pages)

print("=== METHOD SECTION ===")
method_match = re.search(r'METHOD\s*\n(.*?)(?:RESULTS|DISCUSSION)', text, re.IGNORECASE | re.DOTALL)
if method_match:
    print(method_match.group(1)[:4000])
else:
    print("METHOD NOT FOUND")

print("\n=== SAMPLE INFO ===")
matches = re.findall(r'.{0,150}(?:sample|participants|response rate|teams|level of analysis).{0,150}', text, re.IGNORECASE)
for m in set(matches[:15]):
    print(m.strip().replace('\n', ' '))

print("\n=== MEASURES INFO ===")
measures_match = re.search(r'Measures(.*?)(?:RESULTS|Analytical Strategy)', text, re.IGNORECASE | re.DOTALL)
if measures_match:
    print(measures_match.group(1)[:2000])

print("\n=== TABLES ===")
tables = re.findall(r'TABLE\s+\d+[\s\S]{1,100}?(?:Mean|SD|Correlation)[\s\S]{1,1500}?(?:TABLE|FIGURE|\n\n\n)', text, re.IGNORECASE)
for i, t in enumerate(tables):
    print(f"--- Table {i+1} ---")
    print(t[:1000])
