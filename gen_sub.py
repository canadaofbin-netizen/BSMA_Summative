import json
with open('scratch/batch_chunk_7.json', 'r', encoding='utf-8') as f:
    chunk = json.load(f)

subagents = []
for p in chunk:
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f"Review paper {p['id']}",
        'Prompt': f"Now review {p['id']}. The PDF is at {p['pdf']}. Output to {p['out']}."
    })

with open('scratch/temp_subagents.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=2)
