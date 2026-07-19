import json

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_11.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

subagents = []
for p in batch:
    prompt = f"Now review {p['id']}. The PDF is at {p['pdf']}. Output to {p['out']}."
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f"Review {p['id']}",
        'Prompt': prompt
    })

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/invoke_short.json', 'w', encoding='utf-8') as f:
    json.dump({'Subagents': subagents}, f, indent=2)
