import fitz
import sys

pdf_path = sys.argv[1]
try:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    with open("scratch_out.txt", "w", encoding="utf-8") as f:
        f.write(text[:3000])
        
        idx = text.lower().find("method")
        if idx != -1:
            f.write("\n\n--- METHOD SECTION (snippet) ---\n")
            f.write(text[idx:idx+2000])
except Exception as e:
    with open("scratch_out.txt", "w", encoding="utf-8") as f:
        f.write("Error: " + str(e))
