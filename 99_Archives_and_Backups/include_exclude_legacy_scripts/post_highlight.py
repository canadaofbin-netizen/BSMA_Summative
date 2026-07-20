import win32com.client
import re
import subprocess

excel_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_Validation2.xlsx"
keywords = ["team", "firm", "students", "alliance"]

print("==================================================")
print("Starting Post-Highlighting & Backup Process")
print("==================================================")

try:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    wb_com = excel.Workbooks.Open(excel_path)
    ws_com = wb_com.Sheets(1)
    
    # Scan from row 4 to the last populated row in Column 16 (P)
    last_row = ws_com.Cells(ws_com.Rows.Count, "P").End(-4162).Row # -4162 is xlUp
    
    print(f"  -> Scanning {max(0, last_row - 3)} rows for keywords...")
    
    for row in range(4, last_row + 1):
        cell = ws_com.Cells(row, 16) # Column 16 is 'Notes'
        note_str = cell.Value
        if note_str:
            verb_idx = note_str.find('Verbatim Evidence:')
            if verb_idx != -1:
                verbatim_part = note_str[verb_idx:]
                for kw in keywords:
                    for match in re.finditer(rf"\b{re.escape(kw)}\b", verbatim_part, flags=re.IGNORECASE):
                        start_char = verb_idx + match.start() + 1
                        length = match.end() - match.start()
                        chars = cell.GetCharacters(start_char, length)
                        chars.Font.Color = 255 # Red
                        chars.Font.Bold = True
                        
    wb_com.Save()
    wb_com.Close()
    print("  -> Highlighting complete!")
finally:
    if 'excel' in locals():
        excel.Quit()

# GitHub Auto Backup
print("\n  -> Starting GitHub Auto-backup...")
try:
    cwd_path = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY"
    subprocess.run(["git", "add", "BSMA_AI_Run_Validation2.xlsx"], check=True, cwd=cwd_path)
    subprocess.run(["git", "commit", "-m", "Auto-backup: Post-highlighting batch completed"], check=True, cwd=cwd_path)
    subprocess.run(["git", "push"], check=True, cwd=cwd_path)
    print("  -> GitHub Auto-backup successful!")
except subprocess.CalledProcessError as e:
    print(f"  -> GitHub Auto-backup: Working tree clean or nothing to commit. ({e})")
except Exception as e:
    print(f"  -> GitHub Auto-backup failed: {e}")

print("==================================================")
print("Post-Processing Finished!")
print("==================================================")
