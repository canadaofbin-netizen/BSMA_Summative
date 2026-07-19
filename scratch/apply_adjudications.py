import glob, json, os, datetime
import pandas as pd

# 1. Read JSONs
files = glob.glob(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\13team_judgments\*.json')
judgments = {}
for f in files:
    with open(f, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        judgments[data['ID']] = data

# 2. Update memory.md
memory_file = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\memory.md'
with open(memory_file, 'a', encoding='utf-8') as f:
    f.write(f'\n\n## 3. Swarm OS Adjudication ({datetime.date.today().isoformat()})\n')
    f.write('The 13-Agent Swarm OS was deployed to adjudicate 13 remaining discrepancies between the Human GT and AI Validation1. The final resolved verdicts are below:\n\n')
    for pid, data in judgments.items():
        f.write(f'- {pid}: Swarm Final Judgment -> {data["Final_Judgment"]}. {data.get("Rationale", "")}\n')

# 3. Update Validation1 Excel
excel_file = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_Validation1.xlsx'
df = pd.read_excel(excel_file, dtype=str)

updates = 0
for idx, row in df.iterrows():
    pid = str(row['Article ID']).strip()
    if pid in judgments:
        fj = str(judgments[pid]['Final_Judgment'])
        if str(df.at[idx, 'Inclusion-\nExclusion Judgment']).strip() != fj:
            df.at[idx, 'Inclusion-\nExclusion Judgment'] = fj
            # Put the rationale in the notes column if possible, or just reason code
            rc = judgments[pid].get('Reason_Code')
            if rc and str(rc).lower() not in ['none', 'null', 'na', '']:
                df.at[idx, 'Reason for Exclusion'] = str(rc)
            updates += 1

# Save back to Excel
df.to_excel(excel_file, index=False)
print(f'Successfully appended {len(judgments)} adjudications to memory.md')
print(f'Successfully updated {updates} rows in Validation1 Excel.')
