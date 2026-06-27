import PyPDF2
import os

pdf_paths = [
    r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[75] Yuma Akaho (2024) Conceptualizing the adventure tourist as a cross-boundary learner.pdf',
    r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[256] Liu Ting et al. (2024) Expatriates'' boundary-spanning double-edged effects in multinational enterprises.pdf',
    r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[18] Marrone Jennifer A., Tesluk Paul E., Carson Jay B. (2007) A Multilevel Investigation of Antecedents and Consequences of Team Member Boundary-Spanning Behavior.pdf'
]

out_dir = r'C:\Users\yunky\.gemini\antigravity\brain\24b0e3bc-d58a-4110-960c-eef25f2d0ce8\scratch\pdf_texts'
os.makedirs(out_dir, exist_ok=True)

for path in pdf_paths:
    if not os.path.exists(path):
        # Fallback for Akaho path from the search result
        if "Akaho" in path:
            path = r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[166] Akaho Yuma (2024) Conceptualizing the adventure tourist as a cross-boundary learner.pdf'
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue
        else:
            print(f"File not found: {path}")
            continue

    fname = os.path.basename(path).replace('.pdf', '.txt')
    out_path = os.path.join(out_dir, fname)
    
    text = ""
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted: {fname}")
    except Exception as e:
        print(f"Error extracting {path}: {e}")
