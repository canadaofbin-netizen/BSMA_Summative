import json
papers = json.load(open('scratch/batch_chunk_2.json', 'r', encoding='utf-8'))
for p in papers[:10]:
    print(f'{p["id"]}|{p["pdf"]}|{p["out"]}')
