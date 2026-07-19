import json
with open('scratch/batch_chunk_7.json', 'r', encoding='utf-8') as f:
    chunk = json.load(f)
for p in chunk[:15]:
    pdf_name = p['pdf'].split('\\')[-1]
    print(f"{p['id']}: {pdf_name}")
