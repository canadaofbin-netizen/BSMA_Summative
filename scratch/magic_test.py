import sys, json

papers = json.load(open('scratch/batch_chunk_2.json', 'r', encoding='utf-8'))
base = open('scratch/base_prompt.txt', 'r', encoding='utf-8').read()

payload = {'Subagents': []}
for p in papers[:2]:
    payload['Subagents'].append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Reviewer {p["id"]}',
        'Prompt': f'{base}Now review `{p["id"]}`. The PDF is at `{p["pdf"]}`. Output to `{p["out"]}`.'
    })

sys.stdout.write('\x0fcall:invoke_subagent' + json.dumps(payload) + '\x10')
sys.stdout.flush()
