"""
universal_excel_inserter.py — Defense-in-Depth 50-Column OpenPyXL Data Inserter
================================================================================
Layer 1: Contamination Detection
Layer 2: Truncation Detection & JSON Auto-Repair
Layer 3: Quarantine Containment
Layer 4: Zero Guesswork Coercion (Type-Safe Sanitizer, Rule 1 & Trap 2 Range/Minus Normalization)
Layer 5: Token-Aware Anchor Reconciliation, Multi-Schema/Multi-Study Unpacking & 50-Column OpenPyXL Insertion
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
import openpyxl

# Ensure UTF-8 console output
sys.stdout.reconfigure(encoding='utf-8')

# Import sibling utilities
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from backup_manager import backup_databases
from excel_template_util import create_blank_coding_sheet

CWD = os.getcwd()
QUARANTINE_DIR = os.path.join(CWD, "scratch", "quarantine")

EXCLUSION_CODE_MAP = {
    "1": "1 = No effect size of interest",
    "2": "2 = Non-employee samples",
    "3": "3 = Non-individual level (team/firm/org analysis)",
    "4": "4 = Non-primary study",
    "5": "5 = Multiple reasons",
    "6": "6 = Duplicate / retracted",
    "7": "7 = Non-English language",
}

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

    if in_string:
        repaired += '"'

    trimmed = repaired.rstrip()
    if trimmed.endswith(':'):
        repaired += ' null'
    elif trimmed.endswith(','):
        repaired = trimmed[:-1]

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
    """
    Strictly coerce missing, null, or corrupted numbers to type-safe 999 (Rule 1).
    Normalizes Unicode minus (\u2212) and dashes (\u2013, \u2014) to ASCII '-' and
    extracts the leading numeric value (conservative minimum bound for ranges per Trap 2).
    """
    if val is None or isinstance(val, bool):
        return default
    if isinstance(val, (int, float)):
        return default if val == 999 else val
    val_str = str(val).strip()
    if val_str.lower() in ["", "-", "–", "—", "−", "n/a", "na", "null", "none", "not reported", "not_reported", "999"]:
        return default
    # Normalize Unicode minus and en/em dashes to ASCII hyphen-minus
    normalized = val_str.replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-')
    # Extract the first signed float/int token (handles ".570**", "-0.368*", "0.78-0.85", "240-275")
    m = re.search(r'[-+]?(?:\d+\.?\d*|\.\d+)', normalized)
    if not m:
        return default
    try:
        f_val = float(m.group(0))
        if f_val == 999:
            return default
        return int(f_val) if f_val.is_integer() else f_val
    except (ValueError, TypeError):
        return default


def clean_ellipses_for_rule13(text):
    """Ensure verbatim quotes never contain prohibited '...' or '…' ellipses (Rule 13)."""
    if not text:
        return text
    s = str(text).replace('…', '...')
    if '...' not in s:
        return s
    s = re.sub(r'\s*\[\s*\.\.\.+\s*\]\s*', ' | ', s)
    s = re.sub(r'\s*\(\s*\.\.\.+\s*\)\s*', ' | ', s)
    s = re.sub(r'([\'\"“‘\[])\s*\.\.\.+\s*', r'\1', s)
    s = re.sub(r'\s*\.\.\.+\s*([\'\"”’\)\]])', r'\1', s)
    s = re.sub(r'\s*\.\.\.+\s*$', '', s)
    s = re.sub(r'\s*\.\.\.+\s*', ' | ', s)
    s = re.sub(r'(?:\s*\|\s*){2,}', ' | ', s)
    return s.strip()


def sanitize_text(val, default=None):
    """Strictly coerce missing or placeholder strings to None (clean blank in Excel, Rule 1 & Rule 13)."""
    if val is None:
        return default
    val_str = clean_ellipses_for_rule13(str(val).strip())
    if val_str.lower() in ["", "-", "n/a", "na", "null", "none", "999", "not reported", "not_reported"]:
        return default
    return val_str


def sanitize_reliability(rel_dict):
    """Normalize polymorphic reliability object: {'type': ..., 'value': ...}."""
    if isinstance(rel_dict, dict):
        rel_type = sanitize_text(rel_dict.get("type"), default=None)
        rel_val = sanitize_numeric(rel_dict.get("value"), default=999)
        return {"type": rel_type, "value": rel_val}
    elif isinstance(rel_dict, (int, float, str)):
        rel_val = sanitize_numeric(rel_dict, default=999)
        return {"type": "Alpha" if rel_val != 999 else None, "value": rel_val}
    else:
        return {"type": None, "value": 999}


def extract_table_index(name):
    """Extract numeric table index prefix if present (e.g., '10. Org. Comm.' -> 10)."""
    if not name:
        return None
    m = re.match(r'^\s*(?:\((\d+)\)|(\d+)[\.\)])\s*', str(name).strip())
    if m:
        return int(m.group(1) or m.group(2))
    return None


def prune_table_index_prefix(name):
    """Prune purely layout-indexing prefixes like '1. ', '2) ', '(3) ' per Rule 14."""
    if not name:
        return ""
    cleaned = re.sub(r'^\s*(?:\(\d+\)|\d+[\.\)])\s*', '', str(name).strip())
    return cleaned if cleaned else str(name).strip()


# ============================================================
# Layer 5: Token-Aware Anchor Reconciliation & Safe Matching
# ============================================================
def is_internal_anchor(text):
    tokens = re.findall(r'\w+', text.lower())
    return any(t in ['internal', 'intra', 'inside', 'int'] for t in tokens)


def is_external_anchor(text):
    tokens = re.findall(r'\w+', text.lower())
    return any(t in ['external', 'extra', 'outside', 'inter', 'ext'] for t in tokens)


def _tokens_match(t1, t2):
    """Check if two individual word tokens match or are valid abbreviations of each other."""
    if t1 == t2:
        return True
    shorter, longer = (t1, t2) if len(t1) <= len(t2) else (t2, t1)
    if len(shorter) < 3:
        return False
    # Prevent 'com' / 'comm' (communication/commitment) from matching 'complexity' or 'competence'
    if shorter in ('com', 'comm'):
        return longer.startswith('commun') or longer.startswith('commit')
    return longer.startswith(shorter)


def smart_anchor_match(anchor1, anchor2, threshold=0.88):
    """Token-aware safe fuzzy match with table-index guardrail, abbreviation prefix support, and directional protection."""
    if not anchor1 or not anchor2:
        return False

    # Table-Index Guardrail: If both strings carry explicit table index prefixes (e.g. '10.' vs '11.'),
    # different index numbers NEVER match each other.
    idx1 = extract_table_index(anchor1)
    idx2 = extract_table_index(anchor2)
    if idx1 is not None and idx2 is not None and idx1 != idx2:
        return False

    a1 = prune_table_index_prefix(anchor1).lower().strip()
    a2 = prune_table_index_prefix(anchor2).lower().strip()

    if a1 == a2:
        return True

    # Directional Guardrail: NEVER match 'internal' with 'external'
    if is_internal_anchor(a1) and is_external_anchor(a2):
        return False
    if is_external_anchor(a1) and is_internal_anchor(a2):
        return False

    tokens1 = re.findall(r'\w+', a1)
    tokens2 = re.findall(r'\w+', a2)
    if not tokens1 or not tokens2:
        return False

    # Acronym / Initialism check (e.g., 'bsa' <-> 'boundary spanning activity')
    if len(tokens1) == 1 and len(tokens2) >= 2 and tokens1[0] == ''.join(w[0] for w in tokens2):
        return True
    if len(tokens2) == 1 and len(tokens1) >= 2 and tokens2[0] == ''.join(w[0] for w in tokens1):
        return True

    # Bijective token-by-token abbreviation match when token counts are equal
    if len(tokens1) == len(tokens2):
        if all(_tokens_match(t1, t2) for t1, t2 in zip(tokens1, tokens2)):
            return True

    # High-confidence character similarity only when leading tokens match
    if _tokens_match(tokens1[0], tokens2[0]):
        ratio = SequenceMatcher(None, a1, a2).ratio()
        if ratio >= threshold:
            return True

    return False


def extract_paper_id(payload, fallback_id=None):
    """Extract numeric paper ID from payload, nested blocks, or fallback string."""
    blocks = [
        payload,
        payload.get("study_sample") or {},
        payload.get("sample_descriptors") or {},
        payload.get("study_sample_descriptor") or {},
        payload.get("study_details") or {},
        payload.get("node_0_screening") or {},
        payload.get("screening") or {},
    ]
    for blk in blocks:
        if not isinstance(blk, dict):
            continue
        for key in ("paper_id", "article_id", "id", "BSMA_ID"):
            val = blk.get(key)
            if val is not None and str(val).strip() not in ("", "999"):
                m = re.search(r'(\d+)', str(val))
                if m:
                    return int(m.group(1))
    if fallback_id:
        m = re.search(r'(\d+)', str(fallback_id))
        if m:
            return int(m.group(1))
    return 999


def normalize_measure_details(payload):
    """Normalize measure descriptors from unified 'measure_details', 'text_measures', or Specialist C lists."""
    details = []
    for key in ("measure_details", "text_measures", "measure_descriptor", "measures"):
        if key in payload and isinstance(payload[key], list):
            for m in payload[key]:
                if isinstance(m, dict):
                    details.append(m)
    if "boundary_spanning_measures" in payload and isinstance(payload["boundary_spanning_measures"], list):
        for m in payload["boundary_spanning_measures"]:
            if isinstance(m, dict):
                m_copy = dict(m)
                m_copy.setdefault("classification_type", "BS")
                details.append(m_copy)
    if "non_bs_measures" in payload and isinstance(payload["non_bs_measures"], list):
        for m in payload["non_bs_measures"]:
            if isinstance(m, dict):
                m_copy = dict(m)
                m_copy.setdefault("classification_type", "NB")
                details.append(m_copy)
    return details


def compose_measure_quote_col(match_dict, specific_measure):
    """Compose Col 33 / Col 40 verbatim measure quote while ensuring Rule 14 substring fidelity."""
    parts = []
    for k in ("source_quote", "items_quote", "notes", "broad_category"):
        v = sanitize_text(match_dict.get(k))
        if v and v not in parts:
            parts.append(v)
    combined = " ".join(parts).strip() if parts else None
    if combined and specific_measure and specific_measure not in combined:
        combined = f'Measured using {specific_measure}. {combined}'
    elif not combined and specific_measure:
        combined = f'Measured using {specific_measure}.'
    return combined


def extract_screening_verdict(payload):
    """Extract inclusion/exclusion verdict and canonical exclusion reason across top-level or nested screening blocks."""
    scr = payload.get("node_0_screening") or payload.get("screening") or {}
    if not isinstance(scr, dict):
        scr = {}

    raw_v = None
    for k in ("judgment", "verdict", "Verdict", "status"):
        if payload.get(k) is not None:
            raw_v = payload.get(k)
            break
        if scr.get(k) is not None:
            raw_v = scr.get(k)
            break

    v_str = str(raw_v if raw_v is not None else "1 = include").strip().lower()
    is_excluded = v_str in ("0", "0 = exclude", "exclude", "excluded", "false") or v_str.startswith("0")

    raw_reason = None
    for k in ("reason_for_exclusion", "exclusion_reason", "exclusion_code", "Exclusion_Code"):
        if payload.get(k) is not None:
            raw_reason = payload.get(k)
            break
        if scr.get(k) is not None:
            raw_reason = scr.get(k)
            break

    reason_str = sanitize_text(raw_reason, default="1 = No effect size of interest")
    if reason_str and str(reason_str).strip() in EXCLUSION_CODE_MAP:
        reason_str = EXCLUSION_CODE_MAP[str(reason_str).strip()]

    return is_excluded, reason_str


def build_rows_for_single_study(study_payload, paper_id, coder_initials, start_eff_id=1):
    """Build 50-column Cartesian pair rows for a single study payload dict."""
    sample_blocks = [
        study_payload.get("study_sample") or {},
        study_payload.get("sample_descriptors") or {},
        study_payload.get("study_sample_descriptor") or {},
        study_payload.get("study_details") or {},
        study_payload.get("design") or {},
        study_payload.get("node_0_screening") or {},
        study_payload.get("screening") or {},
        study_payload,
    ]

    def get_sample_field(*keys, is_num=False, default=None):
        for blk in sample_blocks:
            if not isinstance(blk, dict):
                continue
            for k in keys:
                if k in blk and blk[k] is not None:
                    res = sanitize_numeric(blk[k]) if is_num else sanitize_text(blk[k], default=default)
                    if (is_num and res != 999) or (not is_num and res is not None):
                        return res
        return 999 if is_num else default

    study_design = get_sample_field("study_design")
    study_design_other = get_sample_field("study_design_other")
    country = get_sample_field("country", "country_of_sample")
    country_specify = get_sample_field("country_specify")
    international_context = get_sample_field("international_context")
    sample_size_n = get_sample_field("listwise_n", "sample_size_n", "sample_n", "effective_sample_size", "effective_n", is_num=True)
    mean_age = get_sample_field("mean_age", is_num=True)
    pct_female = get_sample_field("pct_female", "percent_female", is_num=True)
    org_tenure = get_sample_field("org_tenure", "tenure", is_num=True)
    occupation_type = get_sample_field("occupation_type", "occupation", "sample_type")

    # Unpack matrix block (top-level or nested under 'table_matrix' / 'boundary_spanning_matrix')
    matrix_block = study_payload.get("table_matrix") or study_payload.get("boundary_spanning_matrix") or {}
    if not isinstance(matrix_block, dict):
        matrix_block = {}

    raw_vars = study_payload.get("variables") if study_payload.get("variables") is not None else matrix_block.get("variables", [])
    if isinstance(raw_vars, dict):
        variables = []
        for k, v in raw_vars.items():
            v_copy = dict(v)
            v_copy.setdefault("table_anchor_name", v.get("name") or str(k))
            variables.append(v_copy)
    else:
        variables = list(raw_vars) if isinstance(raw_vars, list) else []

    correlations = study_payload.get("correlations") if study_payload.get("correlations") is not None else matrix_block.get("correlations", [])
    measure_details = normalize_measure_details(study_payload)

    table_number_default = study_payload.get("table_number") or matrix_block.get("table_number") or "Table 1"
    table_page_default = study_payload.get("table_page_number") or matrix_block.get("table_page_number")
    latent_quote = sanitize_text(study_payload.get("latent_evidence_quote") or matrix_block.get("latent_evidence_quote"))
    footnote_quote = sanitize_text(study_payload.get("table_footnote_quote") or matrix_block.get("table_footnote_quote"))

    # Safe Construct Join (Exact Match First, then Smart Matching — Lossless Zero-Drop Policy per Rule 27 & Rule 28)
    joined_vars = []
    unmatched_vars = []

    for var in variables:
        raw_anchor = var.get("table_anchor_name") or var.get("name") or ""
        anchor = prune_table_index_prefix(raw_anchor)

        match = None
        # Pass 1: Exact match on raw_anchor or pruned anchor
        for detail in measure_details:
            detail_anchor = detail.get("table_anchor_name") or detail.get("name") or ""
            if raw_anchor.strip().lower() == detail_anchor.strip().lower() or \
               anchor.lower() == prune_table_index_prefix(detail_anchor).lower():
                match = detail
                break
        # Pass 2: Smart fuzzy match (respecting table index prefix)
        if match is None:
            for detail in measure_details:
                detail_anchor = detail.get("table_anchor_name") or detail.get("name") or ""
                if smart_anchor_match(raw_anchor, detail_anchor):
                    match = detail
                    break

        if match:
            rel_sanitized = sanitize_reliability(match.get("reliability"))
            if rel_sanitized["value"] == 999 and var.get("reliability_table") not in [None, 999, "", "-", "n/a", "N/A"]:
                table_rel = sanitize_numeric(var.get("reliability_table"), default=999)
                if table_rel != 999:
                    rel_sanitized = {"type": "Alpha", "value": table_rel}
            elif rel_sanitized["value"] == 999 and var.get("alpha") not in [None, 999, "", "-", "n/a", "N/A"]:
                table_rel = sanitize_numeric(var.get("alpha"), default=999)
                if table_rel != 999:
                    rel_sanitized = {"type": "Alpha", "value": table_rel}

            spec_meas = sanitize_text(match.get("specific_measure_used") or match.get("specific_measure"))
            quote_col = compose_measure_quote_col(match, spec_meas)

            joined_vars.append({
                "anchor": anchor,
                "raw_anchor": raw_anchor,
                "mean": sanitize_numeric(var.get("mean") if var.get("mean") not in [None, 999, "", "-", "n/a", "N/A"] else match.get("mean", 999)),
                "sd": sanitize_numeric(var.get("sd") if var.get("sd") not in [None, 999, "", "-", "n/a", "N/A"] else match.get("sd", 999)),
                "classification_type": match.get("classification_type", var.get("classification_type", "NB")),
                "items": sanitize_numeric(match.get("number_of_items") if match.get("number_of_items") is not None else match.get("items")),
                "min": sanitize_numeric(match.get("min_score") if match.get("min_score") is not None else match.get("min")),
                "max": sanitize_numeric(match.get("max_score") if match.get("max_score") is not None else match.get("max")),
                "report_type": sanitize_text(match.get("report_type")),
                "report_type_note": sanitize_text(match.get("report_type_note")),
                "specific_measure": spec_meas,
                "quote_col": quote_col,
                "reliability_type": rel_sanitized["type"],
                "reliability": rel_sanitized["value"],
                "composite_quote": sanitize_text(match.get("composite_quote") or var.get("composite_quote"))
            })
        else:
            unmatched_vars.append(anchor)
            table_rel = sanitize_numeric(var.get("reliability_table") if var.get("reliability_table") is not None else var.get("alpha"), default=999)
            rel_type = "Alpha" if table_rel != 999 else "Not_Applicable"
            rel_val = table_rel if table_rel != 999 else 999
            spec_meas = sanitize_text(var.get("specific_measure_used") or var.get("specific_measure"), default=anchor)
            quote_col = compose_measure_quote_col(var, spec_meas)
            joined_vars.append({
                "anchor": anchor,
                "raw_anchor": raw_anchor,
                "mean": sanitize_numeric(var.get("mean"), default=999),
                "sd": sanitize_numeric(var.get("sd"), default=999),
                "classification_type": var.get("classification_type", "NB"),
                "items": sanitize_numeric(var.get("number_of_items") if var.get("number_of_items") is not None else var.get("items"), default=1),
                "min": sanitize_numeric(var.get("min_score") if var.get("min_score") is not None else var.get("min"), default=999),
                "max": sanitize_numeric(var.get("max_score") if var.get("max_score") is not None else var.get("max"), default=999),
                "report_type": sanitize_text(var.get("report_type")),
                "report_type_note": sanitize_text(match_dict_note if (match_dict_note := var.get("report_type_note")) else None),
                "specific_measure": spec_meas,
                "quote_col": quote_col,
                "reliability_type": rel_type,
                "reliability": rel_val,
                "composite_quote": sanitize_text(var.get("composite_quote"))
            })

    if unmatched_vars:
        print(f"  [ROUTED_DEFAULT_NB] Unmatched table variables routed as default constructs: {unmatched_vars}")

    bs_vars = [v for v in joined_vars if v["classification_type"] == "BS"]
    nb_vars = [v for v in joined_vars if v["classification_type"] == "NB"]

    if not bs_vars:
        return [], start_eff_id

    rows_to_write = []
    eff_id = start_eff_id

    for bs in bs_vars:
        composite_quote = bs.get("composite_quote") or sanitize_text(study_payload.get("global_composite_quote") or study_payload.get("composite_quote"))
        for nb in nb_vars:
            r_val = 999
            cell_proof_note = None
            matched_corr = None
            # Pass 1: Exact pruned anchor match
            for corr in correlations:
                v1 = prune_table_index_prefix(corr.get("var1_anchor", "")).lower()
                v2 = prune_table_index_prefix(corr.get("var2_anchor", "")).lower()
                if (bs["anchor"].lower() == v1 and nb["anchor"].lower() == v2) or \
                   (bs["anchor"].lower() == v2 and nb["anchor"].lower() == v1):
                    matched_corr = corr
                    break
            # Pass 2: Smart anchor match (respecting table index prefix)
            if matched_corr is None:
                for corr in correlations:
                    v1 = corr.get("var1_anchor", "")
                    v2 = corr.get("var2_anchor", "")
                    if (smart_anchor_match(bs["raw_anchor"], v1) and smart_anchor_match(nb["raw_anchor"], v2)) or \
                       (smart_anchor_match(bs["raw_anchor"], v2) and smart_anchor_match(nb["raw_anchor"], v1)):
                        matched_corr = corr
                        break

            if matched_corr is not None:
                r_val = sanitize_numeric(matched_corr.get("r"))
                cp = matched_corr.get("cell_proof")
                if cp and isinstance(cp, dict):
                    t_num = cp.get("table_number") or table_number_default
                    if not str(t_num).lower().startswith("table"):
                        t_num = f"Table {t_num}"
                    t_page = cp.get("table_page_number") or table_page_default
                    page_str = f" (p. {t_page})" if t_page else ""
                    row_h = clean_ellipses_for_rule13(cp.get("row_header_quote", nb["raw_anchor"]))
                    col_h = clean_ellipses_for_rule13(cp.get("col_header_quote", bs["raw_anchor"]))
                    raw_v = cp.get("raw_cell_value", str(r_val))
                    base_str = f"{t_num}{page_str}, Row: {row_h}, Col: {col_h}, Raw: {raw_v}"
                    flags = []
                    if latent_quote:
                        flags.append(f"Latent correlation: {latent_quote}")
                    if composite_quote:
                        flags.append(f"Global composite: {composite_quote}")
                    if footnote_quote:
                        flags.append(f"Sample N footnote: {footnote_quote}")
                    cell_proof_note = base_str + (" | " + " | ".join(flags) if flags else "")
                elif cp and isinstance(cp, str):
                    cp_clean = clean_ellipses_for_rule13(cp)
                    cell_proof_note = cp_clean if cp_clean.lower().startswith("table") else f"Table 1, {cp_clean}"

            if cell_proof_note is None:
                t_num = table_number_default
                if not str(t_num).lower().startswith("table"):
                    t_num = f"Table {t_num}"
                t_page = table_page_default
                page_str = f" (p. {t_page})" if t_page else ""
                cell_proof_note = f"{t_num}{page_str}, Row: {nb['raw_anchor']}, Col: {bs['raw_anchor']}, Raw: {r_val}"

            full_50_col_row = [
                # Cols 1-6: Identifiers & Screening Verdict
                coder_initials,          # Col 1: Coder Initials
                paper_id,                # Col 2: Article ID
                None,                    # Col 3: Sample ID (blank per Rule 19)
                eff_id,                  # Col 4: Effect size ID
                "1 = include",           # Col 5: Inclusion-Exclusion Judgment
                None,                    # Col 6: Reason for Exclusion (blank per Rule 19)
                # Cols 7-16: Article Descriptors (strictly blank in batch sheets per Rule 19)
                None, None, None, None, None, None, None, None, None, None,
                # Cols 17-26: Study/Sample Descriptors
                study_design,            # Col 17: Study Design
                study_design_other,      # Col 18: Other (specify)
                country,                 # Col 19: Country
                country_specify,         # Col 20: Country (specify)
                international_context,   # Col 21: International Context
                sample_size_n,           # Col 22: Sample size (N)
                mean_age,                # Col 23: Mean Age
                pct_female,              # Col 24: % Female
                org_tenure,              # Col 25: Org Tenure
                occupation_type,         # Col 26: Occupation Type
                # Cols 27-33: BSB Measure Descriptors
                bs["items"],             # Col 27: Number of Items
                bs["min"],               # Col 28: Min Score
                bs["max"],               # Col 29: Max Score
                bs["report_type"],       # Col 30: Report Type
                bs["report_type_note"],  # Col 31: Report Type Note
                bs["specific_measure"],  # Col 32: Specific Measure Used
                bs["quote_col"],         # Col 33: Notes / Verbatim Measure Quote
                # Cols 34-40: Non-BS Measure Descriptors
                nb["items"],             # Col 34: Number of Items
                nb["min"],               # Col 35: Min Score
                nb["max"],               # Col 36: Max Score
                nb["report_type"],       # Col 37: Report Type
                nb["report_type_note"],  # Col 38: Report Type Note
                nb["specific_measure"],  # Col 39: Specific Measure Used
                nb["quote_col"],         # Col 40: Notes / Verbatim Measure Quote
                # Cols 41-44: BSB Effect Size Stats
                bs["anchor"],            # Col 41: BSB Name
                bs["mean"],              # Col 42: BSB Mean
                bs["sd"],                # Col 43: BSB SD
                bs["reliability"],       # Col 44: BSB Reliability (Alpha)
                # Cols 45-48: Non-BS Effect Size Stats
                nb["anchor"],            # Col 45: Non-BS Name
                nb["mean"],              # Col 46: Non-BS Mean
                nb["sd"],                # Col 47: Non-BS SD
                nb["reliability"],       # Col 48: Non-BS Reliability (Alpha)
                # Cols 49-50: Effect Size & Provenance Coordinates
                r_val,                   # Col 49: Correlation r
                cell_proof_note          # Col 50: Notes (Rule 9 coordinates + flags)
            ]
            rows_to_write.append(full_50_col_row)
            eff_id += 1

    return rows_to_write, eff_id


def write_rows_to_excel(excel_path, paper_id, rows_to_write):
    """Write 50-column rows for paper_id into excel_path, initializing template if needed."""
    if not os.path.exists(excel_path):
        os.makedirs(os.path.dirname(os.path.abspath(excel_path)), exist_ok=True)
        create_blank_coding_sheet(excel_path)

    wb = openpyxl.load_workbook(excel_path)
    ws = wb["Extracted Data"] if "Extracted Data" in wb.sheetnames else wb.active

    # Remove any existing rows for this paper_id (idempotent update)
    existing_rows = []
    for r in range(4, ws.max_row + 1):
        val = ws.cell(r, 2).value
        if val is not None:
            try:
                if int(re.search(r'(\d+)', str(val)).group(1)) == int(paper_id):
                    existing_rows.append(r)
            except Exception:
                pass
    for r in reversed(existing_rows):
        ws.delete_rows(r, 1)

    # Find next available row starting from Row 4
    start_row = 4
    for r in range(4, ws.max_row + 1):
        if any(ws.cell(r, c).value is not None for c in range(1, 51)):
            start_row = r + 1

    for offset, row_vals in enumerate(rows_to_write):
        target_r = start_row + offset
        for c_idx, val in enumerate(row_vals[:50], start=1):
            ws.cell(row=target_r, column=c_idx, value=val)

    wb.save(excel_path)
    wb.close()
    return start_row, start_row + len(rows_to_write) - 1


def route_and_insert_data(excel_path, payload, payload_id="PAYLOAD", do_backup=False):
    print(f"Routing and inserting 50-column data into {excel_path}...")

    paper_id = extract_paper_id(payload, fallback_id=payload_id)
    coder_initials = sanitize_text(
        payload.get("coder_initials") or (payload.get("study_sample_descriptor") or {}).get("coder_initials"),
        default="KY"
    )

    is_excluded, reason = extract_screening_verdict(payload)
    if is_excluded:
        excluded_row = [coder_initials, paper_id, None, None, "0 = exclude", reason] + [None] * 44
        r_start, r_end = write_rows_to_excel(excel_path, paper_id, [excluded_row])
        print(f"Inserted Excluded Paper [{paper_id}] at Row {r_start} (Cols 7-50 blank per Rule 19).")
        if do_backup:
            backup_databases()
        return True, "SUCCESS_EXCLUDED_1_ROW"

    # Support multi-study payloads ('studies' array) or single-study payload
    studies_list = payload.get("studies")
    if isinstance(studies_list, list) and studies_list:
        study_payloads = []
        for st in studies_list:
            if isinstance(st, dict):
                merged = dict(payload)
                merged.pop("studies", None)
                merged.update(st)
                study_payloads.append(merged)
    else:
        study_payloads = [payload]

    all_rows_to_write = []
    eff_id = 1
    for st_payload in study_payloads:
        st_rows, eff_id = build_rows_for_single_study(st_payload, paper_id, coder_initials, start_eff_id=eff_id)
        all_rows_to_write.extend(st_rows)

    if not all_rows_to_write:
        print("  [ZERO_BSB_CONSTRUCT] No variables classified as BS. Triggering Zero-BSB Circuit Breaker.")
        return False, "ZERO_BSB_CONSTRUCT"

    r_start, r_end = write_rows_to_excel(excel_path, paper_id, all_rows_to_write)
    print(f"Inserted {len(all_rows_to_write)} Cartesian Pair row(s) for Paper [{paper_id}] into {excel_path} (Rows {r_start}-{r_end}).")

    if do_backup:
        backup_databases()
    return True, f"SUCCESS_{len(all_rows_to_write)}_PAIRS"


def main():
    parser = argparse.ArgumentParser(description="Universal 50-Column Excel Inserter with Defense-in-Depth & Type Sanitizer")
    parser.add_argument("--excel", required=True, help="Path to the target Excel coding sheet")
    parser.add_argument("--data-file", required=True, help="Path to the JSON payload file")
    parser.add_argument("--backup", action="store_true", help="Trigger milestone backup after insertion")

    args = parser.parse_args()

    if not os.path.exists(args.data_file):
        print(f"Error: Data file {args.data_file} not found.")
        sys.exit(1)

    payload_id = os.path.basename(args.data_file).replace(".json", "")

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
    success, msg = route_and_insert_data(args.excel, payload, payload_id=payload_id, do_backup=args.backup)
    if not success:
        move_to_quarantine(args.data_file, f"routing_error:{msg}", payload_id)
        sys.exit(1)


if __name__ == "__main__":
    main()
