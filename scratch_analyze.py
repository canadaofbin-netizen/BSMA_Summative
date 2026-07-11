import fitz
import re

pdf_path = r"g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/01_Academic_Papers/[668] Zhang et al. (2011) - The boundary spanning capabilities of purchasing agents in buyer–supplier trust.pdf"

doc = fitz.open(pdf_path)
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"

with open("scratch_analysis_output.txt", "w", encoding="utf-8") as f:
    # Search for correlation table keywords
    keywords = ["correlation", "latent", "discriminant validity", "average variance extracted", "AVE", "mean", "standard deviation"]
    for kw in keywords:
        f.write(f"Count of '{kw}': {full_text.lower().count(kw.lower())}\n")

    # Print context around "correlation" and "latent"
    matches = re.finditer(r'.{0,200}correlation.{0,200}', full_text, re.IGNORECASE | re.DOTALL)
    f.write("\n--- Context of 'correlation' ---\n")
    for i, match in enumerate(matches):
        if i > 5: break
        f.write(match.group(0).replace('\n', ' ') + "\n")

    matches2 = re.finditer(r'.{0,200}latent.{0,200}', full_text, re.IGNORECASE | re.DOTALL)
    f.write("\n--- Context of 'latent' ---\n")
    for i, match in enumerate(matches2):
        if i > 5: break
        f.write(match.group(0).replace('\n', ' ') + "\n")

    f.write("\n--- Context of 'validity' ---\n")
    matches3 = re.finditer(r'.{0,200}validity.{0,200}', full_text, re.IGNORECASE | re.DOTALL)
    for i, match in enumerate(matches3):
        if i > 5: break
        f.write(match.group(0).replace('\n', ' ') + "\n")

    f.write("\n--- Table content ---\n")
    table_matches = re.finditer(r'Table \d+.*?Mean', full_text, re.IGNORECASE | re.DOTALL)
    for i, match in enumerate(table_matches):
        if i > 2: break
        start = match.start()
        f.write(full_text[start:start+1000] + "\n")
        
    f.write("\n--- Methods/Sample ---\n")
    methods_start = full_text.find("Method")
    if methods_start == -1:
        methods_start = full_text.find("METHOD")
    if methods_start != -1:
        f.write(full_text[methods_start:methods_start+2000].replace('\n', ' ') + "\n")
