import fitz
import pytesseract
import glob
from PIL import Image
import io

files = glob.glob(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\*258*.pdf')
if files:
    doc = fitz.open(files[0])
    with open('scratch_ocr_258.txt', 'w', encoding='utf-8') as f:
        for page_index in range(len(doc)):
            page = doc[page_index]
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            text = pytesseract.image_to_string(img)
            f.write(f'--- PAGE {page_index+1} ---\n' + text + '\n')
