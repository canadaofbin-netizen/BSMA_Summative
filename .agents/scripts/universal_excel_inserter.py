import openpyxl
import os
import argparse
import json
import re

def insert_data(excel_path, data):
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # Determine last row for spacing
    last_row_idx = ws.max_row
    last_row_empty = True
    for col in range(1, ws.max_column + 1):
        if ws.cell(row=last_row_idx, column=col).value is not None:
            last_row_empty = False
            break

    if not last_row_empty and last_row_idx > 3:
        ws.append([None] * ws.max_column)
        last_row_idx += 1

    # Text mapping dictionaries
    pub_type_map = {1: "1 = Journal article", 2: "2 = Dissertation/thesis", 3: "3 = Conference paper", 4: "4 = Working paper/unpublished", 5: "5 = Book/book chapter"}
    study_design_map = {1: "1 = Cross-sectional", 2: "2 = Longitudinal/time-lagged", 3: "3 = Experimental", 4: "4 = Qualitative"}
    intl_context_map = {1: "1 = No (domestic only)", 2: "2 = Yes (expatriate, multinational, etc.)"}
    report_type_map = {1: "1 = Self", 2: "2 = Supervisor", 3: "3 = Others", 4: "4 = Objective"}

    article_id = data.get("article_id", "BSMA9999")
    sample_size = data.get("sample_size", None)
    pub_type = pub_type_map.get(data.get("publication_type"), data.get("publication_type"))
    study_design = study_design_map.get(data.get("study_design"), data.get("study_design"))
    intl_context = intl_context_map.get(data.get("international_context"), data.get("international_context"))
    occ_type = data.get("occupation_type", None)

    bs_measure = data.get("bs_measure", {})
    correlations = data.get("correlations", [])

    for index, corr in enumerate(correlations):
        row = [None] * 50 # 50 columns
        
        # Col 0-4: Identifiers
        row[0] = "KY"
        row[1] = article_id
        row[2] = f"{article_id}.1" # Sample ID
        row[3] = f"{row[2]}.{index + 1}" # Effect Size ID
        row[4] = "1 = Include"
        
        # Categoricals
        row[11] = pub_type # Publication Type
        row[16] = study_design # Study Design
        row[20] = intl_context # International Context
        row[21] = sample_size # N
        row[25] = occ_type # Occupation Type

        # Measure Descriptors: Boundary Spanning (Cols 26-31)
        row[26] = bs_measure.get("items")
        row[27] = bs_measure.get("min")
        row[28] = bs_measure.get("max")
        row[29] = report_type_map.get(bs_measure.get("report_type"), bs_measure.get("report_type"))
        row[31] = bs_measure.get("specific_measure")

        # Measure Descriptors: Non-BS (Cols 33-38)
        row[33] = corr.get("items")
        row[34] = corr.get("min")
        row[35] = corr.get("max")
        row[36] = report_type_map.get(corr.get("report_type"), corr.get("report_type"))
        row[38] = corr.get("specific_measure")

        # Effect Sizes: BS (Cols 40-43)
        row[40] = bs_measure.get("name")
        row[41] = bs_measure.get("mean")
        row[42] = bs_measure.get("sd")
        row[43] = bs_measure.get("alpha")

        # Effect Sizes: Non-BS (Cols 44-47)
        row[44] = corr.get("non_bs_name")
        row[45] = corr.get("mean")
        row[46] = corr.get("sd")
        row[47] = corr.get("alpha")

        # Effect Sizes: Correlation (Col 48)
        row[48] = corr.get("r")

        ws.append(row)

    wb.save(excel_path)
    print(f"Successfully injected {len(correlations)} rows into {excel_path} using rigid JSON schema.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Excel Inserter for BSMA Meta-Analysis")
    parser.add_argument("--excel", type=str, required=True, help="Path to the master Excel file")
    parser.add_argument("--data", type=str, required=True, help="JSON string matching the structured schema")
    
    args = parser.parse_args()
    
    try:
        payload = json.loads(args.data)
        insert_data(args.excel, payload)
    except Exception as e:
        print(f"Failed to parse JSON schema or insert data: {e}")
