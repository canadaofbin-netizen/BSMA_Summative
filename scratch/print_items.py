import json

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, d in enumerate(data):
    print(f"Item {i}: id={d['id']}, pdf={d['pdf']}")
