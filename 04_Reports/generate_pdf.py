import os
import subprocess
import markdown
import sys

def convert_md_to_pdf(md_file, pdf_file):
    md_file = os.path.join(os.path.dirname(__file__), md_file)
    pdf_file = os.path.join(os.path.dirname(__file__), pdf_file)
    html_file = md_file.replace('.md', '.html')
    
    # 1. Read Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    # 2. Convert to HTML with tables extension
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # 3. Add beautiful GitHub-style CSS
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
            font-size: 12px;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        h1, h2, h3 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-top: 24px;
            margin-bottom: 16px;
        }}
        code {{
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
            padding: 0.2em 0.4em;
            font-family: SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;
        }}
    </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    # 4. Use Chrome Headless to print to PDF
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    abs_html = os.path.abspath(html_file)
    abs_pdf = os.path.abspath(pdf_file)
    
    print(f"Generating PDF for {md_file}...")
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html}"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Success: {pdf_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        
    # Cleanup HTML
    if os.path.exists(html_file):
        os.remove(html_file)

if __name__ == "__main__":
    convert_md_to_pdf('final_screening_report.md', 'final_screening_report.pdf')
    convert_md_to_pdf('Match_Rate_Report.md', 'Match_Rate_Report.pdf')
