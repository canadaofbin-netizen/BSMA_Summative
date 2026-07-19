import fitz
import glob

# Find the file
files = glob.glob('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/*683*.pdf')
if files:
    filename = files[0]
    doc = fitz.open(filename)
    text = '\n'.join([page.get_text() for page in doc])
    with open('scratch_BSMA0683.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extracted", filename)
else:
    print("File not found.")
