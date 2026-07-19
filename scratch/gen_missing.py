import os, glob, json

out_dir = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2'
pdf_dir = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\01_Academic_Papers'

expected = [f'BSMA{str(i).zfill(4)}' for i in range(4, 22)]
expected.remove('BSMA0008')
expected.remove('BSMA0013')

pdfs = glob.glob(os.path.join(pdf_dir, '*.pdf'))

subagents = []
for bsma_id in expected:
    num_str = str(int(bsma_id.replace('BSMA', '')))
    matched_pdf = None
    for pdf in pdfs:
        if os.path.basename(pdf).startswith(f'[{num_str}] '):
            matched_pdf = pdf
            break
    
    if matched_pdf:
        pdf_path = matched_pdf.replace('\\', '/')
        prompt = (
            f'=== CRITICAL OVERRIDE RULES 1-8 ===\n'
            f'1. Leader BSB (Rule 16) -> INCLUDE. 2. Intra-Org BSB (Rule 17) -> INCLUDE. '
            f'3. CEO BSB (Rule 15) -> INCLUDE. 4. 1:1 Dyad Safe Harbor -> NOT Code 3. '
            f"5. Proxy Trap -> 'I'=valid. 6. AI Tool -> Code 1. 7. Network BSB -> INCLUDE. "
            f'8. Implanted BSB -> INCLUDE.\n=== END ===\n'
            f'Review `{bsma_id}`. PDF: `{pdf_path}`. Save verdict JSON to `G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/{bsma_id}.json`.'
        )
        
        subagents.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': f'V2 {bsma_id}',
            'Prompt': prompt,
            'Model': 'flash'
        })

with open('scratch/missing_payload.json', 'w', encoding='utf-8') as f:
    json.dump({'Subagents': subagents}, f, indent=2)

print(f'Generated payload for {len(subagents)} subagents in scratch/missing_payload.json')
