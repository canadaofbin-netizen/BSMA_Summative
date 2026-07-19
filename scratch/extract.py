import PyPDF2

filename = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[677] Zhang and Li (2021) - Can employee's boundary-spanning behavior exactly promote innovation performance.pdf"
reader = PyPDF2.PdfReader(filename)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open(r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\BSMA0677.txt", "w", encoding="utf-8") as f:
    f.write(text)
