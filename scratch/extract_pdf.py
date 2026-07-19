import PyPDF2

pdf_path = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[473] Ramarajan et al. (2011) - From the outside in The negative spillover effects of boundary spanners' relations.pdf"
out_path = r"G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/BSMA0473_text.txt"

with open(pdf_path, 'rb') as f:
    pdf = PyPDF2.PdfReader(f)
    text = '\n'.join([page.extract_text() for page in pdf.pages])

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(text)
