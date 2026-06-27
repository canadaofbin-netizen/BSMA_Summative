import pdfplumber
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    print('Extracting LIU TABLE...')
    liu_pdf = glob.glob(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\*Liu Ting*.pdf')[0]
    with pdfplumber.open(liu_pdf) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for t in tables:
                if t and len(t) > 2 and 'Mean' in str(t):
                    print('--- LIU TABLE ---')
                    for row in t:
                        print(str(row))
except Exception as e:
    print('Error extracting LIU:', e)

try:
    print('\nExtracting MARRONE TABLE...')
    marrone_pdf = glob.glob(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers\*Marrone*.pdf')[0]
    with pdfplumber.open(marrone_pdf) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for t in tables:
                if t and len(t) > 2 and ('Mean' in str(t) or 's.d.' in str(t)):
                    print('--- MARRONE TABLE ---')
                    for row in t:
                        print(str(row))
except Exception as e:
    print('Error extracting MARRONE:', e)
