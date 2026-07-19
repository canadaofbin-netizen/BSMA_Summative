import glob, json, os

files = glob.glob(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\13team_judgments\*.json')
out_file = r'C:\Users\yunky\.gemini\antigravity\brain\75959b0d-11da-4ec8-97cb-bfc5fad81a42\Swarm_Adjudication_Report.md'

with open(out_file, 'w', encoding='utf-8') as out:
    out.write('# 13-Agent Swarm Adjudication Report\n\n')
    out.write('This report resolves the 13 discrepancies between Human Ground Truth and AI Validation1 through independent Swarm Auditor review.\n\n')

    out.write('## Summary of Adjudication\n\n')
    gt_map = {'BSMA0194':'1', 'BSMA0211':'0', 'BSMA0304':'0', 'BSMA0356':'0', 'BSMA0387':'1', 'BSMA0501':'0', 'BSMA0512':'0', 'BSMA0573':'1', 'BSMA0580':'1', 'BSMA0612':'1', 'BSMA0685':'1', 'BSMA0698':'0', 'BSMA0700':'0'}
    ai_map = {'BSMA0194':'0', 'BSMA0211':'1', 'BSMA0304':'1', 'BSMA0356':'ERROR', 'BSMA0387':'0', 'BSMA0501':'1', 'BSMA0512':'1', 'BSMA0573':'0', 'BSMA0580':'0', 'BSMA0612':'0', 'BSMA0685':'0', 'BSMA0698':'1', 'BSMA0700':'1'}

    ai_correct = 0
    human_correct = 0

    details = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
        pid = data['ID']
        gt = gt_map.get(pid, 'N/A')
        ai = ai_map.get(pid, 'N/A')
        fj = str(data['Final_Judgment'])
        
        if fj == gt:
            winner = 'Human (GT) was Correct'
            human_correct += 1
        elif fj == ai:
            winner = 'AI (Validation1) was Correct'
            ai_correct += 1
        else:
            winner = f'Both Incorrect (Swarm concludes {fj})'
        
        details.append(f'### {pid}\n- **Human GT:** {gt}\n- **AI Validation1:** {ai}\n- **Swarm Final Judgment:** {fj} ({winner})\n\n**Rationale:**\n{data.get("Rationale", "")}\n')

    out.write(f'- **Total Adjudicated:** {len(files)}\n')
    out.write(f'- **Human GT Correct:** {human_correct}\n')
    out.write(f'- **AI Validation1 Correct:** {ai_correct}\n\n')
    out.write('## Detailed Rationale\n\n')
    for d in details:
        out.write(d + '\n')
