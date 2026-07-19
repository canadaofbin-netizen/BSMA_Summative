import pdfplumber
import sys

file_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[475] Schwab et al. (1985) - Redefining the Boundary Spanning-Environment Relationship.pdf"
text = ""
with pdfplumber.open(file_path) as pdf:
    for p in pdf.pages:
        page_text = p.extract_text()
        if page_text:
            text += page_text + "\n"

print(len(text))
print(text[:1000])
