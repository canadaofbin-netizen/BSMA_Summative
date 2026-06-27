import os
import shutil
import re

base_dir = r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY'
rulebook_dir = os.path.join(base_dir, '05_Coding_Rulebook')
backup_dir = os.path.join(base_dir, '04_System_Backups')

os.makedirs(rulebook_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)

with open(os.path.join(base_dir, 'read.md'), 'r', encoding='utf-8') as f:
    read_text = f.read()

# 1. Find highest backup version and backup
versions = []
for f in os.listdir(backup_dir):
    if f.startswith('read_v') and f.endswith('.md'):
        v = re.search(r'read_v(\d+)\.md', f)
        if v:
            versions.append(int(v.group(1)))
highest_v = max(versions) if versions else 0
next_v = highest_v + 1
backup_path = os.path.join(backup_dir, f'read_v{next_v}.md')
shutil.copy2(os.path.join(base_dir, 'read.md'), backup_path)
print(f'Backed up to {backup_path}')

# 2. Extract sections
sections = re.split(r'\n## ', '\n' + read_text)

def get_section(title):
    for s in sections:
        if s.startswith(title):
            return '## ' + s
    return ''

core_process = get_section('Coding Process Overview')
dyadic_rules = get_section('Special Cases: Dyadic Data')
author_disc = get_section('Special Cases: Author Discrepancies')
sem_rules = get_section('Special Cases: Misleading Correlation Tables (SEM)')
shadow_workflow = get_section('Automated Extraction Features (Shadow Reports Workflow)')
update_rules = get_section('Rules for Updating This Document')

with open(os.path.join(rulebook_dir, '00_core_process.md'), 'w', encoding='utf-8') as f:
    f.write(core_process)

with open(os.path.join(rulebook_dir, '01_dyadic_data_rules.md'), 'w', encoding='utf-8') as f:
    f.write(dyadic_rules)

with open(os.path.join(rulebook_dir, '02_sem_and_latent_rules.md'), 'w', encoding='utf-8') as f:
    f.write(sem_rules)

with open(os.path.join(rulebook_dir, '03_automated_workflow.md'), 'w', encoding='utf-8') as f:
    f.write(shadow_workflow)

with open(os.path.join(rulebook_dir, '04_general_exceptions.md'), 'w', encoding='utf-8') as f:
    f.write(author_disc)

with open(os.path.join(rulebook_dir, '05_document_management.md'), 'w', encoding='utf-8') as f:
    f.write(update_rules)

# 3. Rewrite read.md
new_read = """# BSMA Archive

> [!IMPORTANT]  
> **AI SYSTEM GUIDELINE**  
> This document serves as the absolute instruction manual and guideline for any AI assistant or coding agent extracting data from academic papers for this meta-analysis project. You must strictly follow all rules, workflows, and extraction protocols defined herein.

This folder contains archived documents and resources for the **Boundary Spanning Meta-Analysis (BSMA)** project, specifically focusing on the actual coding phase.

## Folder Contents
- **BSMA_Actual Coding Sheet_v2.gsheet / .xlsx**: The actual coding spreadsheet where data from various articles is recorded.
- **Coding manual for students.docx / .pdf**: The Actual Coding Manual providing instructions on how to code articles.
- **png of coding sheet.png**: A screenshot visually demonstrating the layout of the coding spreadsheet.
- **05_Coding_Rulebook**: A modular directory containing the explicit coding rules and workflows.

## Modular Coding Rulebook
To prevent this document from becoming bloated, all coding rules, paradigms, and edge-case handlers have been split into the `05_Coding_Rulebook` directory. 

Whenever you encounter a specific study design or paradigm, you **MUST** consult the corresponding rule module below:

- [00_core_process.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/00_core_process.md): The basic coding process overview and variable mapping rules.
- [01_dyadic_data_rules.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/01_dyadic_data_rules.md): Rules for Dyadic Data (Anchor Identification, Report Type flip, filtering demographics).
- [02_sem_and_latent_rules.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/02_sem_and_latent_rules.md): Warnings regarding Discriminant Validity tables and entering `999` for missing Pearson *r*.
- [03_automated_workflow.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/03_automated_workflow.md): The mandatory Two-Step Shadow Reports Workflow and the `[UNRECOGNIZED PARADIGM]` flag.
- [04_general_exceptions.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/04_general_exceptions.md): The Table Over Text rule for resolving author discrepancies.
- [05_document_management.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/05_document_management.md): Rules for updating and backing up this rulebook system.

> [!WARNING]  
> **Unrecognized Paradigms**  
> If you encounter a paradigm that is not covered by any of these modules, halt coding and ask the user. Once a ruling is made, create a new rule module (e.g., `06_new_rule.md`) and link it in this index.
"""

with open(os.path.join(base_dir, 'read.md'), 'w', encoding='utf-8') as f:
    f.write(new_read)

shutil.copy2(os.path.join(base_dir, 'read.md'), os.path.join(backup_dir, f'read_v{next_v + 1}.md'))
print('Split successful and index written.')
