import os
import re
import openpyxl

md_dir = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\03_Shadow_Reports"
excel_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Actual Coding Sheet_v2.xlsx"
out_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Actual Coding Sheet_v3.xlsx"

wb = openpyxl.load_workbook(excel_path)
ws = wb.active

# Find first empty row
start_row = 1
while ws.cell(row=start_row, column=1).value is not None:
    start_row += 1

def parse_md_table(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        in_table = False
        for line in lines:
            line = line.strip()
            if line.startswith("| Effect Size ID") or line.startswith("| **BSMA"):
                in_table = True
            if in_table and line.startswith("|") and not line.startswith("|---"):
                if "Effect Size ID" in line: continue
                # Parse markdown table row
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if cols:
                    rows.append(cols)
    return rows

print(f"Starting at row {start_row}")

# For Liu 2024
liu_rows = parse_md_table(os.path.join(md_dir, "Liu_2024_Shadow_Report.md"))
print(f"Found {len(liu_rows)} rows in Liu.")

# For Marrone 2007
marrone_rows = parse_md_table(os.path.join(md_dir, "Marrone_2007_Shadow_Report.md"))
print(f"Found {len(marrone_rows)} rows in Marrone.")

# This is a complex mapping, I will print the first row of Liu to see columns
if liu_rows:
    print("Liu columns:", len(liu_rows[0]))
    print("Liu row 0:", liu_rows[0])
