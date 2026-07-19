import fitz
import os

pdf_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[336] Lee and Yoo (2023) - How do customer-related characteristics influence frontline bank employees' boundary.pdf"
out_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\BSMA0336.txt"

os.makedirs(os.path.dirname(out_path), exist_ok=True)
doc = fitz.open(pdf_path)
text = "\n".join(page.get_text() for page in doc)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)
