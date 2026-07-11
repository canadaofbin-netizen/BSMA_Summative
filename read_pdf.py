import fitz
import sys
import os

folder = r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers'
files = [f for f in os.listdir(folder) if '[257]' in f]
if not files:
    print("Not found")
    sys.exit(1)
pdf_path = os.path.join(folder, files[0])
print(f"Reading {pdf_path}")

try:
    doc = fitz.open(pdf_path)
    print("\n=== SEARCHING FOR CORRELATION TABLE / MEASURES ===")
    for i, page in enumerate(doc):
        p_text = page.get_text()
        # look for tables
        if "Table 1" in p_text or "Table 2" in p_text or "Descriptive" in p_text or "Correlation" in p_text:
            print(f"\n--- PAGE {i+1} TABLE CONTENT ---")
            print(p_text[:3000].encode('ascii', 'ignore').decode('ascii'))
except Exception as e:
    print(e)
