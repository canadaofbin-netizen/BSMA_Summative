import PyPDF2
import os
import glob

# find the file
files = glob.glob(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\*119*.pdf')
if files:
    pdf_path = files[0]
    print(f"Reading {pdf_path}")
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for i, p in enumerate(reader.pages):
        text += p.extract_text()
    
    with open(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs\BSMA0119_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
else:
    print("File not found.")
