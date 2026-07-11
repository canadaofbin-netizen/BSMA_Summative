import PyPDF2
path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[331] Leuthesser (1991) - Boundary behavior and sellers' performance in business relationships.pdf"
reader = PyPDF2.PdfReader(path)
text = ""
for i, page in enumerate(reader.pages):
    text += f"\n--- PAGE {i+1} ---\n"
    text += page.extract_text()
with open("scratch/bsma0331_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Saved to scratch/bsma0331_text.txt")
