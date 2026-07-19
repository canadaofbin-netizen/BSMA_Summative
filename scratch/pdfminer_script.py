from pdfminer.high_level import extract_text
text = extract_text('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[85] Castellani et al. (2022) - Knowledge integration in multinational enterprises.pdf')
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/pdfminer_out.txt', 'w', encoding='utf-8') as f:
    f.write(text)
