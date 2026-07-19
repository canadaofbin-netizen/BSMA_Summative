import PyPDF2

pdf_path = r'G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[663] Zahoor et al. (2025) - Green strategic intent, artificial intelligence capability and behavioral.pdf'
reader = PyPDF2.PdfReader(pdf_path)
text = ''.join(page.extract_text() for page in reader.pages)

with open('temp_663.txt', 'w', encoding='utf-8') as f:
    f.write(text)
