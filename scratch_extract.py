import fitz
import glob
files = glob.glob(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\*258*.pdf')
if files:
    doc=fitz.open(files[0])
    with open('scratch_extracted_258.txt', 'w', encoding='utf-8') as f:
        for i, page in enumerate(doc):
            text = page.get_text('blocks')
            f.write(f'--- PAGE {i} ---\n')
            for b in text:
                f.write(str(b[4]) + '\n')
