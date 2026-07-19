import json

with open(r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\batch_chunk_0.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

subagents = []
for p in papers:
    pid = p["id"]
    pdf = p["pdf"]
    out = p["out"]
    prompt = f"Now review {pid}. The PDF is at {pdf}. Output to {out}."
    subagents.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer {pid}",
        "Prompt": prompt
    })

payload = {
    "Subagents": subagents,
    "toolSummary": "Invoking reviewers",
    "toolAction": "Invoke subagents"
}

with open("payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f)
