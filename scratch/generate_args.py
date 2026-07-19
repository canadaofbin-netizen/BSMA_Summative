import json

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

subagents = []
for d in data:
    subagents.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer {d['id']}",
        "Prompt": f"Now review {d['id']}. The PDF is at {d['pdf']}. Output to {d['out']}."
    })

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/subagents_args.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=2)
