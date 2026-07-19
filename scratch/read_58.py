import PyPDF2
file_path = "G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[58] Biong and Ulvnes (2011) - If the Supplier's Human Capital Walks Away, Where Would the Customer Go.pdf"
with open(file_path, 'rb') as f:
    pdf = PyPDF2.PdfReader(f)
    text = ''
    for i, page in enumerate(pdf.pages):
        text += f'\n\n--- PAGE {i} ---\n'
        text += page.extract_text() or ''
        
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/bsma0058_text.txt', 'w', encoding='utf-8') as out:
    out.write(text)
print('Success')
