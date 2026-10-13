import os
import re
import sys
import argparse
import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding='utf-8')

def find_pdf_text(article_id, texts_dir="scratch/pdf_texts"):
    os.makedirs(texts_dir, exist_ok=True)
    target_txt = os.path.join(texts_dir, f"{article_id}.txt")
    
    # Extract number from Article ID (e.g., BSMA0005 -> 5)
    m = re.search(r'(\d+)', str(article_id))
    if not m:
        return target_txt
    art_no = int(m.group(1))
    
    # Look for the exact 1-to-1 PDF in 01_Academic_Papers
    papers_dir = os.path.join(os.getcwd(), "01_Academic_Papers")
    matched_pdf = None
    if os.path.exists(papers_dir):
        for f in os.listdir(papers_dir):
            if (f.startswith(f"[{art_no}]") or f.startswith(f"{art_no}_")) and f.lower().endswith(".pdf"):
                matched_pdf = os.path.join(papers_dir, f)
                break
    
    # If PDF found, extract clean text using fitz (PyMuPDF) and write to target_txt
    if matched_pdf and os.path.exists(matched_pdf):
        try:
            doc = fitz.open(matched_pdf)
            text_pages = []
            for page in doc:
                text_pages.append(page.get_text("text"))
            doc.close()
            full_text = "\n--- PAGE BREAK ---\n".join(text_pages)
            with open(target_txt, "w", encoding="utf-8", errors="ignore") as f:
                f.write(full_text)
            return target_txt
        except Exception as e:
            sys.stderr.write(f"Error extracting text from {matched_pdf}: {e}\n")
            
    # Fallback to old behavior if not found
    if os.path.exists(target_txt):
        return target_txt
    return target_txt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Locate PDF by Paper ID and extract text to scratch/pdf_texts/")
    parser.add_argument("--id", required=True, help="Paper ID (e.g., 53 or BSMA0053)")
    parser.add_argument("--dir", default="scratch/pdf_texts", help="Output directory for extracted text")
    args = parser.parse_args()
    
    result = find_pdf_text(args.id, args.dir)
    print(result)
