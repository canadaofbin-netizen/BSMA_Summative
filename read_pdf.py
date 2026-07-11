import PyPDF2

reader = PyPDF2.PdfReader(r'g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[518] Scholz et al. (2008) - Do Networks Solve Collective Action Problems Credibility, Search, and Collaboration.pdf')
text = '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
with open(r'C:\Users\yunky\.gemini\antigravity\brain\3023f334-1b72-4cbe-b4e9-873623fa96af\scratch\temp_pdf_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
