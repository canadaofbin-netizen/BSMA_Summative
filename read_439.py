import os, fitz
f=[x for x in os.listdir('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers') if '439' in x][0]
path = os.path.join('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers', f)
doc = fitz.open(path)
with open('439_text.txt', 'w', encoding='utf-8') as out:
    for p in doc:
        out.write(p.get_text())
