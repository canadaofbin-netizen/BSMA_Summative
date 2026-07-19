import json

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_8.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

subagents = []
for item in batch:
    pdf_clean = item['pdf'].replace('\\\\', '/')
    id = item['id']
    out_path = item['out']
    prompt = f"1. First, read your complete project rules from G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/base_prompt.txt using your view_file tool. You MUST follow these rules exactly.\n2. Now review {id}. The PDF is at {pdf_clean}. Output to {out_path}."
    
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Validation3 for {id}',
        'Prompt': prompt
    })

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/invoke_payload.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=2)

