import fitz, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
files = glob.glob(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\[[]5]*')
doc = fitz.open(files[0])
# Just first 2 pages
for i in range(2):
    print(f"\n--- PAGE {i+1} ---")
    print(doc[i].get_text())
