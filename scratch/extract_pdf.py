import PyPDF2
import sys
import re

pdf_path = "g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[622] Williams (2002) - The Competent Boundary Spanner.pdf"

try:
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- PAGE {i+1} ---\n"
            text += page.extract_text() + "\n"
        
    with open("g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/BSMA0622_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted text successfully.")
except Exception as e:
    print(f"PyPDF2 Error: {e}")
    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                text += f"--- PAGE {i+1} ---\n"
                text += page.extract_text() + "\n"
        with open("g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/BSMA0622_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted text successfully using pdfplumber.")
    except Exception as e2:
        print(f"pdfplumber Error: {e2}")
