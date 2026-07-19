import json
data=json.load(open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_1.json', encoding='utf-8'))
out=[{'TypeName': 'bsma_reviewer_v3', 'Role': 'Reviewer for '+d['id'], 'Prompt': 'Now review ' + d['id'] + '. The PDF is at ' + d['pdf'] + '. Output to ' + d['out'] + '.'} for d in data]
open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/invoke_payload.json', 'w', encoding='utf-8').write(json.dumps(out))
