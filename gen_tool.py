import json
with open('scratch/batch_chunk_4.json', 'r') as f:
    data = json.load(f)
subs = []
for d in data:
    subs.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': 'Paper Data Extractor',
        'Prompt': 'Now review ' + d['id'] + '. The PDF is at ' + d['pdf'] + '. Output to ' + d['out'] + '.'
    })
with open('tool_call.json', 'w') as f:
    json.dump({'Subagents': subs}, f)
