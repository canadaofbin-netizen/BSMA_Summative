import fitz
import pytesseract
from PIL import Image
import io

pdf_path = 'G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[85] Castellani et al. (2022) - Knowledge integration in multinational enterprises.pdf'
doc = fitz.open(pdf_path)

out = []
for i in range(min(6, len(doc))):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img)
    out.append(f"--- PAGE {i+1} ---\n" + text)

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/ocr_out2.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
