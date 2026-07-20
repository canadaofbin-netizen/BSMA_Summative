import fitz
import pytesseract
from PIL import Image

doc = fitz.open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[276] Liebeskind et al. (1996) - Social Networks, Learning and Flexibility.pdf')
text = ""
for i in range(len(doc)):
    pix = doc[i].get_pixmap(dpi=150)
    img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    text += pytesseract.image_to_string(img) + "\n"

with open('scratch/outputs/BSMA0276_ocr.txt', 'w', encoding='utf-8') as f:
    f.write(text)
