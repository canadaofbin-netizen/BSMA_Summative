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
        last_row_idx += 1

    # Text mapping dictionaries
    include_exclude_map = {0: "0 = Exclude", 1: "1 = Include"}
    pub_type_map = {1: "1 = Journal article", 2: "2 = Dissertation/thesis", 3: "3 = Conference paper", 4: "4 = Working paper/unpublished", 5: "5 = Book/book chapter"}
    study_design_map = {1: "1 = Cross-sectional", 2: "2 = Longitudinal/time-lagged", 3: "3 = Experimental", 4: "4 = Qualitative"}
    intl_context_map = {1: "1 = No (domestic only)", 2: "2 = Yes (expatriate, multinational, etc.)"}
    report_type_map = {1: "1 = Self", 2: "2 = Supervisor", 3: "3 = Others", 4: "4 = Objective"}

    # Process each row
    for index, row in enumerate(data_rows):
        # Auto-generate IDs
        article_id = row[1] if row[1] else "BSMA9999"
        sample_id = f"{article_id}.1"
        effect_size_id = f"{sample_id}.{index + 1}"
        
        # Hardcode Coder Initials and Auto-IDs
        row[0] = "KY"
        row[2] = sample_id
        row[3] = effect_size_id
        
        # Apply Text Mappings (safely handling cases where the AI might have already provided text)
        if len(row) > 4 and row[4] in include_exclude_map:
            row[4] = include_exclude_map[row[4]]
            
        if len(row) > 11 and row[11] in pub_type_map:
            row[11] = pub_type_map[row[11]]
            
        if len(row) > 16 and row[16] in study_design_map:
            row[16] = study_design_map[row[16]]
            
        if len(row) > 20 and row[20] in intl_context_map:
            row[20] = intl_context_map[row[20]]
            
        # Report Type mappings for specific variables (Columns 33 for BS Report Type, and 39 for Non-BS Report Type)
        # Note: Actual column indices are 0-indexed in python list.
        # BS Report Type is Col 34 (Index 33)
        if len(row) > 33 and row[33] in report_type_map:
            row[33] = report_type_map[row[33]]
            
        # Non-BS Report Type is Col 40 (Index 39)
        if len(row) > 39 and row[39] in report_type_map:
            row[39] = report_type_map[row[39]]

        ws.append(row)

    wb.save(excel_path)
    print(f"Successfully injected {len(data_rows)} rows into {excel_path} with auto-IDs and text mapping.")

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
