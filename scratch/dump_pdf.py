import sys
import PyPDF2

try:
    with open(r'scratch\336.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            print(f"--- PAGE {i} ---")
            print(page.extract_text()[:2000]) # first 2000 chars of each page
except Exception as e:
    print("ERROR:", e)
