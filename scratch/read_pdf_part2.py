import PyPDF2

pdf_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[383] Lysonski (1985) - A Boundary Theory Investigation of the Product Manager's Role.pdf"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for i in range(12, len(reader.pages)):
        text += f"\n--- Page {i+1} ---\n"
        text += reader.pages[i].extract_text()
        
with open(r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\pdf_content_utf8_part2.txt", "w", encoding="utf-8") as out_file:
    out_file.write(text)
