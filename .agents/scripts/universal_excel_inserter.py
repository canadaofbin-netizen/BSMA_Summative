import openpyxl
import os
import argparse
import json

def insert_data(excel_path, data_rows):
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # Check if the last row is completely empty to avoid adding multiple blank rows
    last_row_idx = ws.max_row
    last_row_empty = True
    for col in range(1, ws.max_column + 1):
        if ws.cell(row=last_row_idx, column=col).value is not None:
            last_row_empty = False
            break

    # If the last row is NOT empty, we insert an empty row for visual spacing
    if not last_row_empty and last_row_idx > 3:  # Row 3 is the header
        ws.append([None] * ws.max_column)

    # Append new data rows
    for row in data_rows:
        ws.append(row)

    wb.save(excel_path)
    print(f"Successfully injected {len(data_rows)} rows into {excel_path} with aesthetic spacing.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Excel Inserter for BSMA Meta-Analysis")
    parser.add_argument("--excel", type=str, required=True, help="Path to the master Excel file")
    parser.add_argument("--data", type=str, required=True, help="JSON string representing a list of rows to insert")
    
    args = parser.parse_args()
    
    try:
        data_rows = json.loads(args.data)
        insert_data(args.excel, data_rows)
    except Exception as e:
        print(f"Failed to parse JSON data or insert: {e}")
