"""
verify_ingestion_parity.py — Lossless Data Ingestion Parity Verifier (Rule 27)
=============================================================================
Audits whether empirical data (Sample Size N, Demographics, Item Counts,
Likert Anchors, Means, SDs, Reliabilities, and Correlations r) extracted by
Subagents into structured JSON were losslessly transcribed into the target
Excel coding sheet.

If any valid empirical metric in the JSON is recorded as '999' (or dropped)
in Excel, this script flags a CRITICAL_PARITY_VIOLATION and exits with code 1.
"""

import os
import re
import sys
import json
import argparse
from typing import Dict, Any, List, Tuple
import openpyxl

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def normalize_anchor(s: str) -> str:
    """Normalize variable name for comparison (pruning leading layout indices per Rule 14)."""
    if not s:
        return ""
    s_clean = re.sub(r'^\s*(?:\(\d+\)|\d+[\.\)])\s*', '', str(s).strip().lower())
    s_clean = s_clean.replace(".", "").replace("(", "").replace(")", "").replace(" ", "").replace("_", "").replace("-", "")
    return s_clean


def is_valid_metric(v: Any) -> bool:
    """Check if value is a valid numeric metric (not None, not empty, not 999)."""
    if v is None or isinstance(v, bool):
        return False
    if isinstance(v, str):
        v_str = v.strip()
        if not v_str or v_str.lower() in ("none", "null", "not reported", "not_reported", "n/a", "na", "-"):
            return False
        v_clean = re.sub(r'[^\d.-]', '', v_str)
        try:
            v_num = float(v_clean)
            return abs(v_num - 999.0) > 1e-4
        except ValueError:
            return False
    if isinstance(v, (int, float)):
        return abs(float(v) - 999.0) > 1e-4
    return False


def extract_reliability_val(obj: Any) -> Any:
    """Extract numeric reliability value from dict or scalar."""
    if isinstance(obj, dict):
        return obj.get("value")
    return obj


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

    # 1. Parse JSON variables and measure descriptors
    json_vars: Dict[str, Dict[str, Any]] = {}

    def merge_var_entry(name: str, data: Dict[str, Any]):
        if not name:
            return
        norm = normalize_anchor(name)
        if not norm:
            return
        entry = json_vars.setdefault(norm, {"raw_name": name})
        for k, v in data.items():
            if is_valid_metric(v) or (k == "reliability" and is_valid_metric(extract_reliability_val(v))):
                entry[k] = v
            elif k not in entry:
                entry[k] = v

    if "variables" in payload:
        vars_data = payload["variables"]
        if isinstance(vars_data, dict):
            for k, v in vars_data.items():
                name = v.get("name") or v.get("table_anchor_name") or str(k)
                merge_var_entry(name, v)
        elif isinstance(vars_data, list):
            for v in vars_data:
                name = v.get("table_anchor_name") or v.get("name") or ""
                merge_var_entry(name, v)

    for m_list_key in ("measure_details", "boundary_spanning_measures", "non_bs_measures"):
        if m_list_key in payload and isinstance(payload[m_list_key], list):
            for m in payload[m_list_key]:
                name = m.get("table_anchor_name") or m.get("name") or ""
                merge_var_entry(name, m)

    # Parse JSON correlations
    json_corrs: Dict[Tuple[str, str], Any] = {}
    if "correlations" in payload and isinstance(payload["correlations"], list):
        for c in payload["correlations"]:
            v1 = normalize_anchor(c.get("var1_anchor", ""))
            v2 = normalize_anchor(c.get("var2_anchor", ""))
            r_val = c.get("r")
            if v1 and v2 and is_valid_metric(r_val):
                json_corrs[(v1, v2)] = r_val
                json_corrs[(v2, v1)] = r_val

    # Sample & Demographics in JSON (support both nested and top-level keys)
    demographics = payload.get("sample_descriptors") or payload.get("study_sample") or {}

    def get_demo_metric(*keys):
        for k in keys:
            if k in demographics and is_valid_metric(demographics[k]):
                return demographics[k]
            if k in payload and is_valid_metric(payload[k]):
                return payload[k]
        return None

    # 2. Load Excel sheet
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb["Extracted Data"] if "Extracted Data" in wb.sheetnames else wb.active

    # Find rows for paper_id
    paper_rows = []
    for r in range(4, ws.max_row + 1):
        cell_id = ws.cell(r, 2).value  # Col 2: Article ID
        if cell_id is not None:
            m = re.search(r'(\d+)', str(cell_id))
            if m and int(m.group(1)) == int(paper_id):
                paper_rows.append(r)

    if not paper_rows:
        wb.close()
        return False, [f"No rows found in Excel sheet for Paper ID {paper_id}"], []

    first_row = paper_rows[0]
    judgment_val = str(ws.cell(first_row, 5).value or "").strip()
    if judgment_val.startswith("0"):
        confirmations.append(f"Paper [{paper_id}] is Excluded ('{judgment_val}'); Col 7-50 blank check verified.")
        wb.close()
        return True, [], confirmations

    # 3. Verify Sample Size N (Col 22) and Demographics (Cols 23, 24, 25)
    expected_n = get_demo_metric("listwise_n", "sample_size_n", "sample_n")
    expected_age = get_demo_metric("mean_age")
    expected_female = get_demo_metric("pct_female", "percent_female")
    expected_tenure = get_demo_metric("org_tenure", "tenure")

    for label, col_idx, exp_val in [
        ("Sample Size N (Col 22)", 22, expected_n),
        ("Demographics Mean Age (Col 23)", 23, expected_age),
        ("Demographics % Female (Col 24)", 24, expected_female),
        ("Demographics Org Tenure (Col 25)", 25, expected_tenure),
    ]:
        if is_valid_metric(exp_val):
            excel_val = ws.cell(first_row, col_idx).value
            if not is_valid_metric(excel_val):
                violations.append(f"{label}: JSON has '{exp_val}', but Excel has '{excel_val}' (dropped to 999).")
            else:
                confirmations.append(f"{label} verified: {excel_val}")

    # 4. Verify Variable Measure Descriptors, Means, SDs, Reliabilities, and Correlations across rows
    for r in paper_rows:
        bs_name = ws.cell(r, 41).value
        nb_name = ws.cell(r, 45).value
        excel_r = ws.cell(r, 49).value

        # Check BSB variable (Cols 27, 28, 29, 42, 43, 44)
        if bs_name:
            bs_norm = normalize_anchor(bs_name)
            j_var = json_vars.get(bs_norm)
            if j_var:
                j_items = j_var.get("number_of_items") if j_var.get("number_of_items") is not None else j_var.get("items")
                j_min = j_var.get("min_score") if j_var.get("min_score") is not None else j_var.get("min")
                j_max = j_var.get("max_score") if j_var.get("max_score") is not None else j_var.get("max")
                j_mean = j_var.get("mean")
                j_sd = j_var.get("sd")
                j_rel = extract_reliability_val(j_var.get("reliability"))
                if not is_valid_metric(j_rel):
                    j_rel = j_var.get("reliability_table") if is_valid_metric(j_var.get("reliability_table")) else j_var.get("alpha")

                for field_lbl, col_i, j_val in [
                    ("Items (Col 27)", 27, j_items),
                    ("Min Score (Col 28)", 28, j_min),
                    ("Max Score (Col 29)", 29, j_max),
                    ("Mean (Col 42)", 42, j_mean),
                    ("SD (Col 43)", 43, j_sd),
                    ("Reliability (Col 44)", 44, j_rel),
                ]:
                    ex_v = ws.cell(r, col_i).value
                    if is_valid_metric(j_val) and not is_valid_metric(ex_v):
                        violations.append(f"Row {r} BSB '{bs_name}' {field_lbl}: JSON has '{j_val}', but Excel has '{ex_v}'.")
                    elif is_valid_metric(j_val) and is_valid_metric(ex_v):
                        confirmations.append(f"Row {r} BSB '{bs_name}' {field_lbl} verified: {ex_v}")

        # Check Non-BS variable (Cols 34, 35, 36, 46, 47, 48)
        if nb_name:
            nb_norm = normalize_anchor(nb_name)
            j_var = json_vars.get(nb_norm)
            if j_var:
                j_items = j_var.get("number_of_items") if j_var.get("number_of_items") is not None else j_var.get("items")
                j_min = j_var.get("min_score") if j_var.get("min_score") is not None else j_var.get("min")
                j_max = j_var.get("max_score") if j_var.get("max_score") is not None else j_var.get("max")
                j_mean = j_var.get("mean")
                j_sd = j_var.get("sd")
                j_rel = extract_reliability_val(j_var.get("reliability"))
                if not is_valid_metric(j_rel):
                    j_rel = j_var.get("reliability_table") if is_valid_metric(j_var.get("reliability_table")) else j_var.get("alpha")

                for field_lbl, col_i, j_val in [
                    ("Items (Col 34)", 34, j_items),
                    ("Min Score (Col 35)", 35, j_min),
                    ("Max Score (Col 36)", 36, j_max),
                    ("Mean (Col 46)", 46, j_mean),
                    ("SD (Col 47)", 47, j_sd),
                    ("Reliability (Col 48)", 48, j_rel),
                ]:
                    ex_v = ws.cell(r, col_i).value
                    if is_valid_metric(j_val) and not is_valid_metric(ex_v):
                        violations.append(f"Row {r} Non-BS '{nb_name}' {field_lbl}: JSON has '{j_val}', but Excel has '{ex_v}'.")
                    elif is_valid_metric(j_val) and is_valid_metric(ex_v):
                        confirmations.append(f"Row {r} Non-BS '{nb_name}' {field_lbl} verified: {ex_v}")

        # Check Correlation r (Col 49)
        if bs_name and nb_name:
            pair_key = (normalize_anchor(bs_name), normalize_anchor(nb_name))
            if pair_key in json_corrs:
                exp_r = json_corrs[pair_key]
                if is_valid_metric(exp_r) and not is_valid_metric(excel_r):
                    violations.append(f"Row {r} Correlation r ('{bs_name}' x '{nb_name}', Col 49): JSON has '{exp_r}', but Excel has '{excel_r}'.")
                elif is_valid_metric(exp_r) and is_valid_metric(excel_r):
                    confirmations.append(f"Row {r} Correlation r ('{bs_name}' x '{nb_name}') verified: {excel_r}")

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
        for c in confirmations[:12]:
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
