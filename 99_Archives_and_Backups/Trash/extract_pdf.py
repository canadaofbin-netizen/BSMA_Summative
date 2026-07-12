import sys
import PyPDF2

def extract_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        import traceback
        return str(e) + "\n" + traceback.format_exc()

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    text = extract_text(pdf_path)
    with open("pdf_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Done")
