import openpyxl
wb = openpyxl.load_workbook("G:\\My Drive\\UCL\\BSMA\\BSMA ANTIGRAVITY\\BSMA_Master_Coding_Sheet.xlsx")
ws = wb.active
for col in range(1, 18):
    print(f"Col {col}: {ws.cell(row=1, column=col).value}")
