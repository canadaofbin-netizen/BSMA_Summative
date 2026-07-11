import fitz, pytesseract, io
from PIL import Image

doc = fitz.open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[57] Biong and Selnes (1997) - The Strategic Role of the Salesperson in Established Buyer-Seller Relationships.pdf')
text=''
for i in range(21, 28):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    text += f'\n--- Page {i} ---\n' + pytesseract.image_to_string(img)

with open('scratch/outputs/BSMA0057_ocr_1.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')
