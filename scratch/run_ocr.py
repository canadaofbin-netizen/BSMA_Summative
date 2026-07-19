import fitz
import pytesseract
from PIL import Image
import io

doc = fitz.open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[276] Liebeskind et al. (1996) - Social Networks, Learning and Flexibility.pdf')
with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2\BSMA0276_ocr.txt', 'w', encoding='utf-8') as f:
    for i in range(min(doc.page_count, 15)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes()))
        text = pytesseract.image_to_string(img)
        f.write(f"\n--- Page {i + 1} ---\n")
        f.write(text)
