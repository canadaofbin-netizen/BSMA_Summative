import json

with open('scratch/batch_chunk_1.json', 'r') as f:
    data = json.load(f)

subs = []
for d in data:
    subs.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": "Paper Reviewer",
        "Prompt": f"Now review {d['id']}. The PDF is at {d['pdf']}. Output to {d['out']}."
    })

with open('scratch/subs.json', 'w') as f:
    json.dump(subs, f, indent=2)
