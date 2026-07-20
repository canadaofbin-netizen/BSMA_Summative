import openpyxl
import shutil

source = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx"
target = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_Validation3.xlsx"

# Copy the file first to preserve any special formatting, merged cells, etc (though openpyxl might drop some VBA/images, shutil.copy preserves it all)
# Wait, if I shutil.copy, then open it with openpyxl, it might be safer.
shutil.copy(source, target)

wb = openpyxl.load_workbook(target)
ws = wb.active

# Column P is the 16th column. Delete from 17 to the max column.
max_col = ws.max_column
if max_col > 16:
    ws.delete_cols(17, max_col - 16)

wb.save(target)
print("Successfully generated BSMA_AI_Run_Validation3.xlsx and stripped columns Q onwards.")
