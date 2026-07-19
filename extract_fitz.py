import fitz

file_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[330] Lazorchak and O'Neal (2001) - Department Store Apparel Buyers Relationships Among Environmental.pdf"
try:
    doc = fitz.open(file_path)
    text = '\n'.join(page.get_text('text') for page in doc)
    with open('temp_paper_fitz.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extracted successfully, length:", len(text))
except Exception as e:
    print(f"Error: {e}")
