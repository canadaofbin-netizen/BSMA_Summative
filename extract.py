import PyPDF2

file_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[330] Lazorchak and O'Neal (2001) - Department Store Apparel Buyers Relationships Among Environmental.pdf"
try:
    reader = PyPDF2.PdfReader(file_path)
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    with open('temp_paper.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extracted successfully, length:", len(text))
except Exception as e:
    print(f"Error: {e}")
