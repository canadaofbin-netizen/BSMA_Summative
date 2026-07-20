import pandas as pd
import pandera as pa
import argparse
import sys
import os

def lint_data(excel_path: str):
    print(f"[*] Starting Data Lint (Pandera) on: {excel_path}")
    
    if not os.path.exists(excel_path):
        print(f"[ERROR] File not found: {excel_path}")
        sys.exit(1)
        
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"[ERROR] Failed to read Excel: {e}")
        sys.exit(1)
        
    is_validation = "Validation" in os.path.basename(excel_path)
    
    # Enforce Rule 19: Validation sheet should not exceed 16 columns (A-P)
    if is_validation and df.shape[1] > 16:
        print(f"[ERROR] Rule 19 Violation: Validation sheet has {df.shape[1]} columns. Expected <= 16 (A-P).")
        sys.exit(1)
        
    # Build a schema where every column must not have NaNs (Rule 1)
    columns_schema = {}
    for col in df.columns:
        columns_schema[col] = pa.Column(nullable=False)
        
    schema = pa.DataFrameSchema(
        columns=columns_schema,
        strict=False 
    )
    
    try:
        # lazy=True returns all errors at once
        schema.validate(df, lazy=True)
        print("[PASS] Data Integrity Confirmed. No Rule 1 (NaN) or Rule 19 violations.")
    except pa.errors.SchemaErrors as err:
        print(f"\n[CRITICAL] Data Integrity Violation (Rule 1):")
        print("The following cells contain blanks/NaNs. You MUST use 999 for numbers or 'Not Reported' for text.")
        print(err.failure_cases.to_string(index=False))
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pandera Data Linter for BSMA Excel sheets.")
    parser.add_argument("--excel", required=True, help="Path to the Excel file to lint.")
    args = parser.parse_args()
    
    lint_data(args.excel)
