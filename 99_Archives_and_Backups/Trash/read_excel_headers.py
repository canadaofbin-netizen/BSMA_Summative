import openpyxl
wb = openpyxl.load_workbook(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx', data_only=True)
ws = wb.active
for row in range(1, 4):
    row_data = [str(ws.cell(row=row, column=col).value) for col in range(1, 10)]
    print(f"Row {row}: " + " | ".join(row_data))
