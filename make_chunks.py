import json
with open('scratch/base_prompt.txt', 'r', encoding='utf-8') as f:
    base = f.read()

with open('scratch/batch_chunk_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(0, len(data), 10):
    chunk = data[i:i+10]
    subs = []
    for d in chunk:
        subs.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': 'Paper Data Extractor',
            'Prompt': base + '\nNow review ' + d['id'] + '. The PDF is at ' + d['pdf'] + '. Output to ' + d['out'] + '.'
        })
    with open('scratch/invoke_chunk_' + str(i) + '.json', 'w', encoding='utf-8') as f:
        json.dump({'Subagents': subs}, f)
