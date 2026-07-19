import json

with open("scratch/batch_chunk_13.json", "r", encoding="utf-8") as f:
    data = json.load(f)

out_array = []
for p in data:
    id = p["id"]
    pdf = p["pdf"].replace("\\", "/")
    out = p["out"]
    out_array.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer for {id}",
        "Prompt": f"Now review {id}. The PDF is at {pdf}. Output to {out}.",
        "Model": "pro"
    })

with open("scratch/invoke_payload.json", "w", encoding="utf-8") as f:
    json.dump(out_array, f, indent=2, ensure_ascii=False)
