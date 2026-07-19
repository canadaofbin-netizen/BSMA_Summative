import sys
import pypdfium2 as pdfium
import pytesseract
import re
from PIL import Image

pdf_path = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[334] Lee and Mathur (1997) - Formalization, Role Stress, Organizational Commitment, and Propensity-to-Leave.pdf'

print("Extracting images using pypdfium2...")
pdf = pdfium.PdfDocument(pdf_path)
full_text = []

for i in range(len(pdf)):
    page = pdf[i]
    bitmap = page.render(scale=3) # 3x scale ~216 dpi
    pil_image = bitmap.to_pil()
    text = pytesseract.image_to_string(pil_image)
    full_text.append(f"--- PAGE {i+1} ---\n{text}")
    print(f"OCR Page {i+1} done.")

text_output = "\n".join(full_text)

with open('BSMA0334_ocr.txt', 'w', encoding='utf-8') as f:
    f.write(text_output)

print("Saved to BSMA0334_ocr.txt")
