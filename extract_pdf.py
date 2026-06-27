import PyPDF2
import sys
import os

pdf_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[1] Perreault Mildred et al. (2023) Everything else is public relations - how rural journalists draw the boundary between journalism and public relations in rural communities.pdf"
txt_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\03_Archives_and_Backups\pdf_texts\BSMA0001.txt"

with open(pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
        
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(text))
    
print("Done")
