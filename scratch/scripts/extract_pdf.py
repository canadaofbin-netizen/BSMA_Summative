import sys
try:
    import fitz
except ImportError:
    print("fitz not found, trying PyPDF2")
    import PyPDF2
    
pdf_path = 'g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[424] Tushman (1977) - Special Boundary Roles in the Innovation Process.pdf'

try:
    if 'fitz' in sys.modules:
        doc = fitz.open(pdf_path)
        with open('scratch/outputs/pdf_content.txt', 'w', encoding='utf-8') as f:
            for page in doc:
                f.write(page.get_text())
        print("Success with PyMuPDF")
    else:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            with open('scratch/outputs/pdf_content.txt', 'w', encoding='utf-8') as f:
                for page in reader.pages:
                    f.write(page.extract_text())
        print("Success with PyPDF2")
except Exception as e:
    print(f"Error: {e}")
