import argparse
import json
import os
import sys
from difflib import SequenceMatcher

def fuzzy_match(anchor1, anchor2, threshold=0.8):
    if not anchor1 or not anchor2:
        return False
    # Simple similarity ratio
    ratio = SequenceMatcher(None, anchor1.lower(), anchor2.lower()).ratio()
    return ratio >= threshold

def route_and_insert_data(excel_path, payload):
    print(f"Routing logic initialized for {excel_path}...")
    
    # 1. Extract Flags
    is_longitudinal = payload.get("is_longitudinal", False)
    is_imputed = payload.get("is_imputed", False)
    is_partial_mixed = payload.get("is_partial_mixed", False)
    is_transformed = payload.get("is_transformed", False)
    
    # Check Salami Slicing (mock logic for now, in reality queries a DB)
    fingerprint = payload.get("dataset_fingerprint", {})
    is_salami_suspect = False # Placeholder
    
    print(f"Flags -> Longitudinal: {is_longitudinal}, Imputed: {is_imputed}, Partial: {is_partial_mixed}, Transformed: {is_transformed}")
    
    # 2. Extract Data
    variables = payload.get("variables", [])
    correlations = payload.get("correlations", [])
    measure_details = payload.get("measure_details", [])
    
    # 3. Inner Join (Fuzzy Matching)
    # Join `variables` (mean, sd) with `measure_details` (items, min, max, rel, classification)
    joined_vars = []
    for var in variables:
        anchor = var.get("table_anchor_name")
        match = None
        for detail in measure_details:
            if fuzzy_match(anchor, detail.get("table_anchor_name")):
                match = detail
                break
        
        if match:
            joined_vars.append({
                "anchor": anchor,
                "mean": var.get("mean"),
                "sd": var.get("sd"),
                "classification_type": match.get("classification_type"),
                "items": match.get("items"),
                "min": match.get("min"),
                "max": match.get("max"),
                "reliability": match.get("reliability", {}).get("value"),
                "specific_measure": match.get("specific_measure")
            })
        else:
            print(f"[JOIN_FAILURE] Failed to match table variable '{anchor}' with textual measure details.")
            sys.exit(1) # Circuit Breaker triggered
            
    # 4. Separate into BS and NB
    bs_vars = [v for v in joined_vars if v["classification_type"] == "BS"]
    nb_vars = [v for v in joined_vars if v["classification_type"] == "NB"]
    
    # 5. Cartesian Product (N x M pairs)
    pairs = []
    for bs in bs_vars:
        for nb in nb_vars:
            # Find the correlation between BS and NB
            r_val = 999
            for corr in correlations:
                v1 = corr.get("var1_anchor")
                v2 = corr.get("var2_anchor")
                # Fuzzy match both ways
                if (fuzzy_match(bs["anchor"], v1) and fuzzy_match(nb["anchor"], v2)) or \
                   (fuzzy_match(bs["anchor"], v2) and fuzzy_match(nb["anchor"], v1)):
                    r_val = corr.get("r")
                    break
            
            # Map to the 19 columns
            pair_row = [
                # BS Variables
                bs["items"], bs["min"], bs["max"], "Not Reported", bs["specific_measure"], bs["anchor"], bs["mean"], bs["sd"], bs["reliability"],
                # NB Variables
                nb["items"], nb["min"], nb["max"], "Not Reported", nb["specific_measure"], nb["anchor"], nb["mean"], nb["sd"], nb["reliability"],
                # Correlation
                r_val
            ]
            pairs.append(pair_row)
    
    print(f"Generated {len(pairs)} Cartesian Pairs.")
    
    # 6. Routing Logic
    if is_transformed:
        print("Routing to: Transformed_Metrics sheet")
    elif is_imputed:
        print("Routing to: Imputed_Metrics sheet")
    elif is_salami_suspect:
        print("Routing to: Salami_Review_Queue sheet")
    else:
        print("Routing to: Raw_Metrics sheet (Pure Zero-Order Data)")
        
    print("Insertion completed successfully (Simulated).")

def main():
    parser = argparse.ArgumentParser(description="Universal Excel Inserter with Cartesian Pair Routing")
    parser.add_argument("--excel", required=True, help="Path to the Master Excel file")
    parser.add_argument("--data-file", required=True, help="Path to the JSON payload file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_file):
        print(f"Error: Data file {args.data_file} not found.")
        sys.exit(1)
        
    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON payload in {args.data_file}. Details: {e}")
        sys.exit(1)
        
    route_and_insert_data(args.excel, payload)

if __name__ == "__main__":
    main()
