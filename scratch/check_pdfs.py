import fitz

files = [
    r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[335] Lee and Han (2019) - The effects of relationship bonds on bank employees’ psychological responses.pdf",
    r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[696] Zimmer and Henry (2017) - The role of social capital in selecting interpersonal information sources.pdf"
]

with open("scratch/pdf_texts.txt", "w", encoding="utf-8") as f:
    for file in files:
        f.write(f"\n\n================ {file} ================\n")
        doc = fitz.open(file)
        text = "".join([page.get_text() for page in doc])
        idx = text.lower().find("correlation")
        if idx != -1:
            f.write(text[max(0, idx-1000):idx+3000])
        else:
            f.write("No 'correlation' found.")
