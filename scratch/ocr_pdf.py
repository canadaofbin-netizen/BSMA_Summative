import sys
from pdf2image import convert_from_path
import pytesseract

file_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[475] Schwab et al. (1985) - Redefining the Boundary Spanning-Environment Relationship.pdf"
pages = convert_from_path(file_path, dpi=300, first_page=1, last_page=3)

text = ""
for page in pages:
    text += pytesseract.image_to_string(page)

print(text[:2000])
