import json

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    print(f"{d['id']}|{d['pdf']}|{d['out']}")
