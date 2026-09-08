"""
universal_excel_inserter.py — Defense-in-Depth Data Inserter
============================================================
Layer 1: Contamination Detection
Layer 2: Truncation Detection & JSON Auto-Repair
Layer 3: Quarantine Containment
Layer 4: Zero Guesswork Coercion (Type-Safe Sanitizer)
Layer 5: Token-Aware Anchor Reconciliation & Cartesian Routing
"""

import argparse
import json
import os
import re
import sys
import csv
import shutil
from datetime import datetime
from difflib import SequenceMatcher

# Import automated backup script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backup_manager import backup_databases

CWD = os.getcwd()
QUARANTINE_DIR = os.path.join(CWD, "scratch", "quarantine")

# ============================================================
# Layer 1: Contamination Detection
# ============================================================
CONTAMINATION_PATTERNS = [
    r'</SYSTEM_MESSAGE>',
    r'<SYSTEM_MESSAGE>',
    r'</PLANNER_RESPONSE>',
    r'<PLANNER_RESPONSE>',
    r'<truncated \d+ bytes>',
    r'"step_index"',
    r'"tool_calls"',
    r'"source":\s*"MODEL"',
]

def check_contamination(raw_text, payload_id="PAYLOAD"):
    """Pre-injection contamination scan. Returns list of detected patterns."""
    found = []
    for pattern in CONTAMINATION_PATTERNS:
        if re.search(pattern, raw_text):
            found.append(pattern)
    if found:
        print(f"  [CONTAMINATION] {payload_id}: Detected {len(found)} pattern(s): {found}")
    return found

# ============================================================
# Layer 2: Truncation Detection & JSON Auto-Repair
# ============================================================
def detect_truncation(raw_text, payload_id="PAYLOAD"):
    """Detect if JSON output was truncated by token limits."""
    issues = []
    open_braces = raw_text.count('{') - raw_text.count('}')
    open_brackets = raw_text.count('[') - raw_text.count(']')
    if open_braces != 0:
        issues.append(f"unbalanced_braces({open_braces:+d})")
    if open_brackets != 0:
        issues.append(f"unbalanced_brackets({open_brackets:+d})")

    unescaped_quotes = len(re.findall(r'(?<!\\)"', raw_text))
    if unescaped_quotes % 2 != 0:
        issues.append("odd_unescaped_quotes")

    if issues:
        print(f"  [TRUNCATION] {payload_id}: Detected issues: {issues}")
    return issues

def attempt_json_repair(raw_text, payload_id="PAYLOAD"):
    """Attempt to repair truncated JSON using LIFO delimiter stack and syntax fixing."""
    repaired = raw_text.rstrip()

    # Step 1: Detect if cut off inside a string
    in_string = False
    escape = False
    stack = []

    for char in repaired:
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if not in_string:
            if char == '{':
                stack.append('}')
            elif char == '[':
                stack.append(']')
            elif char in ['}', ']']:
                if stack and stack[-1] == char:
                    stack.pop()

    # If string is unclosed, close it
    if in_string:
        repaired += '"'

    # Step 2: Fix trailing comma or trailing colon
    trimmed = repaired.rstrip()
    if trimmed.endswith(':'):
        repaired += ' null'
    elif trimmed.endswith(','):
        repaired = trimmed[:-1]

    # Step 3: Close delimiters in LIFO order
    while stack:
        repaired += stack.pop()

    try:
        data = json.loads(repaired)
        print(f"  [REPAIR SUCCESS] {payload_id}: JSON repaired successfully.")
        return data
    except json.JSONDecodeError as e:
        print(f"  [REPAIR FAILED] {payload_id}: JSONDecodeError after repair attempt: {e}")
        return None

# ============================================================
# Layer 3: Quarantine Containment
# ============================================================
def move_to_quarantine(file_path, reason, payload_id="PAYLOAD"):
    """Move corrupted/contaminated payload to quarantine directory and log reason."""
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    dest = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    shutil.copy(file_path, dest)

    log_path = os.path.join(QUARANTINE_DIR, "quarantine_log.csv")
    file_exists = os.path.exists(log_path)
    with open(log_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Payload_ID", "Reason", "File"])
        writer.writerow([datetime.now().isoformat(), payload_id, reason, os.path.basename(file_path)])

    print(f"  [QUARANTINE] {payload_id}: Moved to quarantine ({dest}). Reason: {reason}")

# ============================================================
# Layer 4: Zero Guesswork Coercion (Type-Safe Sanitizer)
# ============================================================
def sanitize_numeric(val, default=999):
    """Strictly coerce missing, null, or corrupted numbers to type-safe 999."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return default if val == 999 else val
    val_str = str(val).strip().lower()
    if val_str in ["", "-", "n/a", "na", "null", "none", "not reported", "not_reported", "999"]:
        return default
    # Strip asterisks or extraneous non-numeric characters
    cleaned = re.sub(r'[^\d.-]', '', val_str)
    try:
        f_val = float(cleaned)
        return int(f_val) if f_val.is_integer() else f_val
    except (ValueError, TypeError):
        return default

def sanitize_text(val, default="Not Reported"):
    """Strictly coerce missing or placeholder strings to 'Not Reported'."""
    if val is None:
        return default
    val_str = str(val).strip()
    if val_str.lower() in ["", "-", "n/a", "na", "null", "none", "999", "not reported", "not_reported"]:
        return default
    return val_str

def sanitize_reliability(rel_dict):
    """Normalize polymorphic reliability object: {'type': ..., 'value': ...}."""
    if isinstance(rel_dict, dict):
        rel_type = sanitize_text(rel_dict.get("type"), default="Not_Reported")
        rel_val = sanitize_numeric(rel_dict.get("value"), default=999)
        return {"type": rel_type, "value": rel_val}
    elif isinstance(rel_dict, (int, float)):
        return {"type": "Alpha", "value": sanitize_numeric(rel_dict, default=999)}
    else:
        return {"type": "Not_Reported", "value": 999}

# ============================================================
# Layer 5: Token-Aware Anchor Reconciliation & Safe Matching
# ============================================================
DEMOGRAPHIC_KEYWORDS = ["age", "gender", "tenure", "education", "experience", "sex", "marital"]

def is_demographic_anchor(anchor_name):
    """Check if variable is a demographic control variable."""
    if not anchor_name:
        return False
    lower = anchor_name.lower().strip()
    for kw in DEMOGRAPHIC_KEYWORDS:
        if kw == lower or re.search(rf'\b{kw}\b', lower):
            return True
    return False

def is_internal_anchor(text):
    tokens = re.findall(r'\w+', text.lower())
    return any(t in ['internal', 'intra', 'inside', 'int'] for t in tokens)

def is_external_anchor(text):
    tokens = re.findall(r'\w+', text.lower())
    return any(t in ['external', 'extra', 'outside', 'inter', 'ext'] for t in tokens)

def smart_anchor_match(anchor1, anchor2, threshold=0.70):
    """Token-aware safe fuzzy match with abbreviation prefix support and directional protection."""
    if not anchor1 or not anchor2:
        return False
    a1 = anchor1.lower().strip()
    a2 = anchor2.lower().strip()

    if a1 == a2:
        return True

    # Directional Guardrail: NEVER match 'internal' with 'external'
    if is_internal_anchor(a1) and is_external_anchor(a2):
        return False
    if is_external_anchor(a1) and is_internal_anchor(a2):
        return False

    # Standard SequenceMatcher
    ratio = SequenceMatcher(None, a1, a2).ratio()
    if ratio >= threshold:
        return True

    # Token-level abbreviation matching
    tokens1 = re.findall(r'\w+', a1)
    tokens2 = re.findall(r'\w+', a2)
    if not tokens1 or not tokens2:
        return False

    shorter, longer = (tokens1, tokens2) if len(tokens1) <= len(tokens2) else (tokens2, tokens1)
    all_matched = True
    for s_tok in shorter:
        if len(s_tok) < 3:
            if s_tok not in longer:
                all_matched = False
                break
        else:
            if not any(l_tok.startswith(s_tok) or s_tok.startswith(l_tok) for l_tok in longer):
                all_matched = False
                break

    return all_matched

def route_and_insert_data(excel_path, payload):
    print(f"Routing logic initialized for {excel_path}...")

    # 1. Extract Flags
    is_longitudinal = bool(payload.get("is_longitudinal", False))
    is_imputed = bool(payload.get("is_imputed", False))
    is_partial_mixed = bool(payload.get("is_partial_mixed", False))
    is_transformed = bool(payload.get("is_transformed", False))
    fingerprint = payload.get("dataset_fingerprint", {})
    is_salami_suspect = False

    print(f"Flags -> Longitudinal: {is_longitudinal}, Imputed: {is_imputed}, Partial: {is_partial_mixed}, Transformed: {is_transformed}")

    # 2. Extract Data
    variables = payload.get("variables", [])
    correlations = payload.get("correlations", [])
    measure_details = payload.get("measure_details", [])

    # 3. Inner Join (Smart Matching with Demographic Filter)
    joined_vars = []
    unmatched_vars = []

    for var in variables:
        anchor = var.get("table_anchor_name", "")
        if is_demographic_anchor(anchor):
            print(f"  [DEMOGRAPHIC_PRUNED] Dropped control variable: '{anchor}'")
            continue

        match = None
        for detail in measure_details:
            detail_anchor = detail.get("table_anchor_name", "")
            if smart_anchor_match(anchor, detail_anchor):
                match = detail
                break

        if match:
            rel_sanitized = sanitize_reliability(match.get("reliability"))
            joined_vars.append({
                "anchor": anchor,
                "mean": sanitize_numeric(var.get("mean")),
                "sd": sanitize_numeric(var.get("sd")),
                "classification_type": match.get("classification_type", "NB"),
                "items": sanitize_numeric(match.get("items")),
                "items_quote": sanitize_text(match.get("items_quote")),
                "min": sanitize_numeric(match.get("min")),
                "max": sanitize_numeric(match.get("max")),
                "reliability_type": rel_sanitized["type"],
                "reliability": rel_sanitized["value"],
                "specific_measure": sanitize_text(match.get("specific_measure")),
                "source_quote": sanitize_text(match.get("source_quote"))
            })
        else:
            unmatched_vars.append(anchor)

    if unmatched_vars:
        print(f"  [WARNING] Unmatched table variables (could not link to measures): {unmatched_vars}")

    # 4. Separate into BS and NB
    bs_vars = [v for v in joined_vars if v["classification_type"] == "BS"]
    nb_vars = [v for v in joined_vars if v["classification_type"] == "NB"]

    if not bs_vars:
        print("  [ZERO_BSB_CONSTRUCT] No variables classified as BS. Triggering Zero-BSB Circuit Breaker.")
        return False, "ZERO_BSB_CONSTRUCT"

    # 5. Cartesian Product (N x M pairs)
    pairs = []
    for bs in bs_vars:
        for nb in nb_vars:
            r_val = 999
            cell_proof = None
            for corr in correlations:
                v1 = corr.get("var1_anchor", "")
                v2 = corr.get("var2_anchor", "")
                if (smart_anchor_match(bs["anchor"], v1) and smart_anchor_match(nb["anchor"], v2)) or \
                   (smart_anchor_match(bs["anchor"], v2) and smart_anchor_match(nb["anchor"], v1)):
                    r_val = sanitize_numeric(corr.get("r"))
                    cell_proof = corr.get("cell_proof")
                    break

            pair_row = [
                # BS Variables (Cols 18-26)
                bs["items"], bs["min"], bs["max"], "Not Reported", bs["specific_measure"], bs["anchor"], bs["mean"], bs["sd"], bs["reliability"],
                # NB Variables (Cols 27-35)
                nb["items"], nb["min"], nb["max"], "Not Reported", nb["specific_measure"], nb["anchor"], nb["mean"], nb["sd"], nb["reliability"],
                # Correlation (Col 36)
                r_val,
                # Cell Proof metadata
                cell_proof
            ]
            pairs.append(pair_row)

    print(f"Generated {len(pairs)} Cartesian Pairs.")

    # 6. Routing Logic
    if is_transformed:
        target_sheet = "Transformed_Metrics"
    elif is_imputed:
        target_sheet = "Imputed_Metrics"
    elif is_salami_suspect:
        target_sheet = "Salami_Review_Queue"
    else:
        target_sheet = "Raw_Metrics"

    print(f"Routing to target sheet: {target_sheet}")
    print("Insertion completed successfully (Simulated).")

    # Automated backup
    backup_databases()
    return True, f"SUCCESS_{len(pairs)}_PAIRS"

def main():
    parser = argparse.ArgumentParser(description="Universal Excel Inserter with Defense-in-Depth & Type Sanitizer")
    parser.add_argument("--excel", required=True, help="Path to the Master Excel file")
    parser.add_argument("--data-file", required=True, help="Path to the JSON payload file")

    args = parser.parse_args()

    if not os.path.exists(args.data_file):
        print(f"Error: Data file {args.data_file} not found.")
        sys.exit(1)

    payload_id = os.path.basename(args.data_file).replace(".json", "")

    # Read raw text
    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except Exception as e:
        print(f"Error reading file {args.data_file}: {e}")
        move_to_quarantine(args.data_file, f"read_error:{e}", payload_id)
        sys.exit(1)

    # Layer 1: Contamination Check
    contam = check_contamination(raw_text, payload_id)
    if contam:
        move_to_quarantine(args.data_file, f"contamination:{contam}", payload_id)
        sys.exit(1)

    # Layer 2: Truncation Check & Auto-Repair
    trunc = detect_truncation(raw_text, payload_id)
    if trunc:
        payload = attempt_json_repair(raw_text, payload_id)
        if payload is None:
            move_to_quarantine(args.data_file, f"truncation_unrecoverable:{trunc}", payload_id)
            sys.exit(1)
    else:
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError as e:
            payload = attempt_json_repair(raw_text, payload_id)
            if payload is None:
                move_to_quarantine(args.data_file, f"json_decode_error:{e}", payload_id)
                sys.exit(1)

    # Layer 4 & 5: Execute Routing & Insertion
    success, msg = route_and_insert_data(args.excel, payload)
    if not success:
        move_to_quarantine(args.data_file, f"routing_error:{msg}", payload_id)
        sys.exit(1)

if __name__ == "__main__":
    main()
