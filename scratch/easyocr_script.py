import pypdfium2 as pdfium
import easyocr
import numpy as np

pdf_path = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[334] Lee and Mathur (1997) - Formalization, Role Stress, Organizational Commitment, and Propensity-to-Leave.pdf'
pdf = pdfium.PdfDocument(pdf_path)
reader = easyocr.Reader(['en'])
full_text = []

for i in range(len(pdf)):
    page = pdf[i]
    bitmap = page.render(scale=2)
    pil_image = bitmap.to_pil()
    image_np = np.array(pil_image)
    
    results = reader.readtext(image_np, detail=0)
    text = "\n".join(results)
    full_text.append(f"--- PAGE {i+1} ---\n{text}")
    print(f"Page {i+1} extracted")

with open('BSMA0334_easyocr.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(full_text))

print("Done")
