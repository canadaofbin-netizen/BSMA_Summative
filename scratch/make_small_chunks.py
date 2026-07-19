import json
data = json.load(open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\batch_chunk_0.json', encoding='utf-8'))
for i in range(4):
    chunk = data[i*10:(i+1)*10]
    out = []
    for item in chunk:
        out.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': f"Rev {item['id']}",
            'Prompt': f"Now review {item['id']}. The PDF is at {item['pdf']}. Output to {item['out']}."
        })
    with open(rf'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\small_chunk_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1)
print("Created small chunks.")
