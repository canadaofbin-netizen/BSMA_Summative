import os
import argparse
import glob
import openpyxl

def find_pdf_text(article_id, excel_path, texts_dir):
    # Try to find the exact BSMA000X match first (if renamed)
    exact_match = os.path.join(texts_dir, f"{article_id}.txt")
    if os.path.exists(exact_match):
        return exact_match

    # If not renamed, lookup Author/Year in Excel to fuzzy match the filename
    try:
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        ws = wb.active
        
        author = None
        year = None
        for row in ws.iter_rows(min_row=4, max_col=10, values_only=True):
            if row[1] == article_id: # Col 2 is Article ID
                author = str(row[7]).split(',')[0].strip() if row[7] else "" # First author
                year = str(row[8]).strip() if row[8] else ""
                break
        
        if author and year:
            # Look for a file containing the author and year recursively
            all_files = glob.glob(os.path.join("03_Archives_and_Backups", "**", "*.txt"), recursive=True)
            for f in all_files:
                fname = os.path.basename(f).lower()
                if author.lower() in fname and year in fname:
                    return f
            # If year is missing but author matches
            for f in all_files:
                fname = os.path.basename(f).lower()
                if author.lower() in fname:
                    return f

    except Exception as e:
        print(f"Error reading Excel for mapping: {e}")

    # Fallback: Just return a structured path even if it fails, let the caller handle it
    return exact_match

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--excel", default="BSMA_Master_Coding_Sheet.xlsx")
    parser.add_argument("--dir", default="03_Archives_and_Backups/pdf_texts")
    args = parser.parse_args()
    
    result = find_pdf_text(args.id, args.excel, args.dir)
    print(result) # Print the resolved file path to stdout
