import fitz
import pytesseract
from PIL import Image
import io

doc = fitz.open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[483] Trent (1996) - Understanding and evaluating cross-functional sourcing team leadership.pdf')
text = ''
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes()))
    text += f'\n--- Page {i+1} ---\n' + pytesseract.image_to_string(img)
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0483_ocr.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('OCR complete.')
