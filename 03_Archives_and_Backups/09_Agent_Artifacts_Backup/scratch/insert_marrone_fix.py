import re
import openpyxl

marrone_md = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\03_Shadow_Reports\Marrone_2007_Shadow_Report.md"
excel_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Actual Coding Sheet_v3.xlsx"

wb = openpyxl.load_workbook(excel_path)
ws = wb.active

def clean(val):
    val = val.strip()
    val = val.replace('**', '').replace('*', '')
    if val == '999': return 999
    if val == '1': return 1
    if val == '0': return 0
    try: return float(val)
    except: return val

# Insert Akaho
akaho_row = [None]*47
akaho_row[0] = "BSMA0004"
akaho_row[1] = "KY"
akaho_row[2] = "BSMA0004.1"
akaho_row[3] = "BSMA0004.1.1"
akaho_row[4] = 0
akaho_row[7] = "Yuma Akaho"
akaho_row[8] = 2024
akaho_row[11] = "4 = Non-primary study"
akaho_row[15] = "Excluded based on Shadow Report: Conceptual/theoretical paper."
ws.append(akaho_row)

# Parse Marrone
with open(marrone_md, 'r', encoding='utf-8') as f:
    text = f.read()

tables = re.findall(r'\| Effect Size ID.*?(?=\n\n|\Z)', text, re.DOTALL)
marrone_count = 1

for t in tables:
    lines = t.strip().split('\n')
    for line in lines:
        if line.startswith('| Effect Size ID') or line.startswith('|---') or line.startswith('| :---'):
            continue
        if line.startswith('|'):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) < 9: continue
            
            row = [None]*47
            row[0] = "BSMA0001"
            row[1] = "KY"
            row[2] = "BSMA0001.1"
            row[3] = f"BSMA0001.1.{marrone_count}"
            row[4] = 1
            row[7] = "Jennifer A. Marrone, Paul E. Tesluk, Jay B. Carson"
            row[8] = 2007
            row[11] = "1 = Journal article"
            row[20] = "1 = No"
            row[21] = 999
            row[23] = 999
            row[24] = 999
            row[25] = "MBA students in consulting"
            row[26] = "USA"
            row[27] = 1
            row[28] = 5
            row[29] = 3
            row[31] = "Boundary-spanning behavior. Closely following existing research..."
            
            row[35] = clean(cols[2])
            row[41] = clean(cols[8])
            row[43] = clean(cols[4])
            row[44] = clean(cols[3])
            
            ws.append(row)
            marrone_count += 1

wb.save(excel_path)
print(f"Appended Akaho and {marrone_count - 1} rows for Marrone to v3.xlsx")
