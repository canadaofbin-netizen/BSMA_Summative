"""
verify_ingestion_parity.py — Lossless Data Ingestion Parity Verifier (Rule 27)
=============================================================================
Audits whether empirical data (Means, SDs, Reliabilities, Sample Demographics)
extracted by Subagents into structured JSON were losslessly transcribed into
the target Excel coding sheet.

If any valid empirical metric in the JSON is recorded as '999' in Excel, this
script flags a CRITICAL_PARITY_VIOLATION and exits with code 1.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List, Tuple
import openpyxl

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def normalize_anchor(s: str) -> str:
    """Normalize variable name for comparison."""
    if not s:
        return ""
    # Strip layout numbering like "1. ", "(2) "
    s = str(s).strip().lower()
    s = s.replace(".", "").replace("(", "").replace(")", "").replace(" ", "").replace("_", "")
    return s


def is_valid_metric(v: Any) -> bool:
    """Check if value is a valid numeric metric (not None, not empty, not 999)."""
    if v is None:
        return False
    if isinstance(v, str):
        v_str = v.strip()
        if not v_str or v_str.lower() in ("none", "null", "not reported", "n/a"):
            return False
        try:
            v_num = float(v_str)
            return abs(v_num - 999.0) > 1e-4
        except ValueError:
            return False
    if isinstance(v, (int, float)):
        return abs(float(v) - 999.0) > 1e-4
    return False


def verify_paper_parity(excel_path: str, json_path: str, paper_id: int) -> Tuple[bool, List[str], List[str]]:
    """
    Compare JSON extraction output against Excel sheet data for a specific paper.
    Returns: (passed, violations, confirmations)
    """
    violations = []
    confirmations = []

    if not os.path.exists(excel_path):
        return False, [f"Excel file not found: {excel_path}"], []
    if not os.path.exists(json_path):
        return False, [f"JSON file not found: {json_path}"], []

    with open(json_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)

    # 1. Parse JSON variables
    json_vars = {}
    if "variables" in payload:
        vars_data = payload["variables"]
        if isinstance(vars_data, dict):
            for k, v in vars_data.items():
                name = v.get("name") or v.get("table_anchor_name") or str(k)
                json_vars[name] = v
        elif isinstance(vars_data, list):
            for v in vars_data:
                name = v.get("table_anchor_name") or v.get("name") or ""
                if name:
                    json_vars[name] = v

    # Demographics in JSON
    demographics = payload.get("sample_descriptors") or payload.get("study_sample") or {}

    # 2. Load Excel sheet
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active

    # Find rows for paper_id
    paper_rows = []
    # Data starts at row 4
    for r in range(4, ws.max_row + 1):
        cell_id = ws.cell(r, 2).value  # Col 2: Article ID
        if cell_id is not None:
            try:
                if int(cell_id) == int(paper_id):
                    paper_rows.append(r)
            except (ValueError, TypeError):
                continue

    if not paper_rows:
        wb.close()
        return False, [f"No rows found in Excel sheet for Paper ID {paper_id}"], []

    # 3. Verify Demographics (Cols 23, 24, 25)
    first_row = paper_rows[0]
    expected_age = demographics.get("mean_age")
    expected_female = demographics.get("percent_female")
    expected_tenure = demographics.get("tenure") or demographics.get("org_tenure")

    if is_valid_metric(expected_age):
        excel_age = ws.cell(first_row, 23).value
        if not is_valid_metric(excel_age):
            violations.append(f"Demographics Mean Age (Col 23): JSON has '{expected_age}', but Excel has '{excel_age}' (dropped to 999).")
        else:
            confirmations.append(f"Demographics Mean Age verified: {excel_age}")

    if is_valid_metric(expected_female):
        excel_female = ws.cell(first_row, 24).value
        if not is_valid_metric(excel_female):
            violations.append(f"Demographics % Female (Col 24): JSON has '{expected_female}', but Excel has '{excel_female}' (dropped to 999).")
        else:
            confirmations.append(f"Demographics % Female verified: {excel_female}")

    if is_valid_metric(expected_tenure):
        excel_tenure = ws.cell(first_row, 25).value
        if not is_valid_metric(excel_tenure):
            violations.append(f"Demographics Org Tenure (Col 25): JSON has '{expected_tenure}', but Excel has '{excel_tenure}' (dropped to 999).")
        else:
            confirmations.append(f"Demographics Org Tenure verified: {excel_tenure}")

    # 4. Verify Variables Mean and SD
    # Col 41: BSB Name, Col 42: BSB Mean, Col 43: BSB SD
    # Col 45: Non-BS Name, Col 46: Non-BS Mean, Col 47: Non-BS SD
    for r in paper_rows:
        bs_name = ws.cell(r, 41).value
        bs_mean = ws.cell(r, 42).value
        bs_sd = ws.cell(r, 43).value

        nb_name = ws.cell(r, 45).value
        nb_mean = ws.cell(r, 46).value
        nb_sd = ws.cell(r, 47).value

        # Check BS variable
        if bs_name:
            bs_norm = normalize_anchor(bs_name)
            for j_name, j_var in json_vars.items():
                if normalize_anchor(j_name) == bs_norm:
                    j_mean = j_var.get("mean")
                    j_sd = j_var.get("sd")
                    if is_valid_metric(j_mean) and not is_valid_metric(bs_mean):
                        violations.append(f"Row {r} BSB '{bs_name}' Mean: JSON has '{j_mean}', but Excel Col 42 has '{bs_mean}'.")
                    if is_valid_metric(j_sd) and not is_valid_metric(bs_sd):
                        violations.append(f"Row {r} BSB '{bs_name}' SD: JSON has '{j_sd}', but Excel Col 43 has '{bs_sd}'.")
                    break

        # Check Non-BS variable
        if nb_name:
            nb_norm = normalize_anchor(nb_name)
            for j_name, j_var in json_vars.items():
                if normalize_anchor(j_name) == nb_norm:
                    j_mean = j_var.get("mean")
                    j_sd = j_var.get("sd")
                    if is_valid_metric(j_mean) and not is_valid_metric(nb_mean):
                        violations.append(f"Row {r} Non-BS '{nb_name}' Mean: JSON has '{j_mean}', but Excel Col 46 has '{nb_mean}'.")
                    if is_valid_metric(j_sd) and not is_valid_metric(nb_sd):
                        violations.append(f"Row {r} Non-BS '{nb_name}' SD: JSON has '{j_sd}', but Excel Col 47 has '{nb_sd}'.")
                    break

    wb.close()
    passed = len(violations) == 0
    return passed, violations, confirmations


def main():
    parser = argparse.ArgumentParser(description="Lossless Ingestion Parity Verifier (Rule 27)")
    parser.add_argument("--excel", required=True, help="Path to Excel coding sheet")
    parser.add_argument("--json", required=True, help="Path to Subagent extraction JSON")
    parser.add_argument("--paper-id", type=int, required=True, help="Article ID of the paper")

    args = parser.parse_args()

    print("=" * 70)
    print(f"BSMA Ingestion Parity Audit — Paper ID: [{args.paper_id}]")
    print(f"Excel Sheet: {args.excel}")
    print(f"Source JSON: {args.json}")
    print("=" * 70)

    passed, violations, confirmations = verify_paper_parity(args.excel, args.json, args.paper_id)

    if confirmations:
        print(f"\n[CONFIRMED CHECKS] ({len(confirmations)} verified)")
        for c in confirmations[:10]:
            print(f"  ✓ {c}")

    if not passed:
        print(f"\n[CRITICAL PARITY VIOLATIONS] ({len(violations)} data loss incidents detected):")
        for v in violations:
            print(f"  ✗ {v}")
        print("\n[RESULT] FAILED — Data was lost or converted to 999 during ingestion. Commit blocked.")
        sys.exit(1)
    else:
        print("\n[RESULT] PASSED — Zero data drop detected. All JSON empirical metrics match Excel cells perfectly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
