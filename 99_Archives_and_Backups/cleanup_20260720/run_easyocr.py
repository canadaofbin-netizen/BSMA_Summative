import fitz
import easyocr
import numpy as np

doc = fitz.open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[276] Liebeskind et al. (1996) - Social Networks, Learning and Flexibility.pdf')
reader = easyocr.Reader(['en'], gpu=False)

text = ""
for i in range(13): # OCR first 13 pages
    if i >= len(doc): break
    print(f"Processing page {i}...")
    pix = doc[i].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    # easyocr expects BGR or RGB numpy array
    results = reader.readtext(img, detail=0)
    text += f"--- PAGE {i} ---\n"
    text += " ".join(results) + "\n\n"

with open('scratch/outputs/BSMA0276_easyocr.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done!")
