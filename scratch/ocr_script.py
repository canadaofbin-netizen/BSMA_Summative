import sys
from pdf2image import convert_from_path
import pytesseract
import re

pdf_path = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[334] Lee and Mathur (1997) - Formalization, Role Stress, Organizational Commitment, and Propensity-to-Leave.pdf'

print("Converting PDF to images...")
images = convert_from_path(pdf_path, dpi=200, poppler_path=r'C:\Program Files\poppler\Library\bin') # assuming poppler is in PATH or this path, wait, I can just rely on PATH first.
