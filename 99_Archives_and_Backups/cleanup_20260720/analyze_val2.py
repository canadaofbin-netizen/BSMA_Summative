import pandas as pd
import json

try:
    df = pd.read_excel('BSMA_AI_Run_Validation2.xlsx', skiprows=2)
    # The actual columns based on the file format are likely:
    # df.columns.tolist() showed: ['Coder Initials', 'Article ID', 'Sample ID', 'Effect size ID', 'Inclusion-\nExclusion Judgment', 'Reason for Exclusion', 'Article Descriptors', ...]
    
    # Actually wait, skiprows=2 might be needed depending on how the header is formatted. 
    # Let me just load it without skiprows and check again.
    df = pd.read_excel('BSMA_AI_Run_Validation2.xlsx')
    
    col_judgement = 'Inclusion-\nExclusion Judgment'
    col_reason = 'Reason for Exclusion'
    
    # Drop rows where 'Article ID' is NaN (i.e. empty rows)
    df = df.dropna(subset=['Article ID'])
    
    total = len(df)
    
    # 1 is include, 0 is exclude
    included = len(df[df[col_judgement] == 1])
    excluded = len(df[df[col_judgement] == 0])
    
    # Calculate unprocessed
    unprocessed = len(df[pd.to_numeric(df[col_judgement], errors='coerce').isna()])
    
    # Exclusion breakdown
    excluded_df = df[df[col_judgement] == 0]
    exclusion_codes = excluded_df[col_reason].astype(str).value_counts().to_dict()
    
    stats = {
        'total_papers_in_sheet': total,
        'included': included,
        'excluded': excluded,
        'unprocessed': unprocessed,
        'exclusion_codes': exclusion_codes
    }
    
    print(json.dumps(stats, indent=2))
except Exception as e:
    print(f"Error: {e}")
