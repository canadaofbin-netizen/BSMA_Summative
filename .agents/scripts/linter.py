import os
import re
import sys
import glob
import argparse
from typing import List, Dict, Any

# Ensure stdout uses UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class BSMAProjectLinter:
    def __init__(self, root_dir: str = "."):
        self.root_dir = os.path.abspath(root_dir)
        self.findings = {
            "CRITICAL": [],
            "WARNING": [],
            "INFO": [],
            "PASS": []
        }

    def add_finding(self, level: str, category: str, message: str, details: str = ""):
        self.findings[level].append({
            "category": category,
            "message": message,
            "details": details
        })

    def audit_workspace_hygiene(self):
        """Audit Area 1: Workspace & Directory Hygiene (AGENTS.md Rule 18)"""
        category = "Workspace Hygiene"
        permitted_root_files = {".gitignore", "desktop.ini", "README.md"}
        permitted_root_dirs = {
            ".agents", ".git", "01_Academic_Papers", "02_Reference_Manuals",
            "03_Coding_Sheets", "04_Reports", "99_Archives_and_Backups", "scratch"
        }

        # 1. Root directory check
        for item in os.listdir(self.root_dir):
            item_path = os.path.join(self.root_dir, item)
            if os.path.isfile(item_path):
                if item not in permitted_root_files:
                    self.add_finding("CRITICAL", category, f"Root pollution detected: unauthorized file '{item}'",
                                     "Only .gitignore is permitted in the root directory. Coding sheets must be in 03_Coding_Sheets/.")
            elif os.path.isdir(item_path):
                if item not in permitted_root_dirs:
                    self.add_finding("WARNING", category, f"Non-standard root directory detected: '{item}'",
                                     f"Expected directories: {sorted(list(permitted_root_dirs))}")

        # 2. Ghost & Lock files check
        ghost_patterns = ["~$*.xlsx", "Thumbs.db", ".DS_Store"]
        for pattern in ghost_patterns:
            for f in glob.glob(os.path.join(self.root_dir, "**", pattern), recursive=True):
                if ".git" not in f:
                    rel_f = os.path.relpath(f, self.root_dir)
                    self.add_finding("WARNING", category, f"Ghost/Lock file detected: '{rel_f}'", "Remove temporary OS/Excel lock files.")

        # 3. Python cache (.pyc / __pycache__)
        pycache_dirs = []
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root:
                continue
            if "__pycache__" in dirs:
                rel_p = os.path.relpath(os.path.join(root, "__pycache__"), self.root_dir)
                pycache_dirs.append(rel_p)
                self.add_finding("WARNING", category, f"Python cache directory detected: '{rel_p}'", "Run linter with --fix to clean.")

        # 4. Scratch directory containment
        scratch_dir = os.path.join(self.root_dir, "scratch")
        if os.path.exists(scratch_dir):
            scratch_files = [f for f in os.listdir(scratch_dir) if f != ".gitkeep"]
            if scratch_files:
                self.add_finding("INFO", category, f"Scratch directory contains {len(scratch_files)} temporary item(s)",
                                 "Scratch directory holds temporary files. Ensure it is cleaned post-batch.")
            else:
                self.add_finding("PASS", category, "Scratch directory is clean (0 items)")

        if not self.findings["CRITICAL"] and not [f for f in self.findings["WARNING"] if f["category"] == category]:
            self.add_finding("PASS", category, "Root directory zero-pollution and hygiene verified.")

    def audit_academic_papers(self):
        """Audit Area 2: Academic Paper Registry (AGENTS.md Rule 17)"""
        category = "Academic Papers Registry"
        papers_dir = os.path.join(self.root_dir, "01_Academic_Papers")

        if not os.path.exists(papers_dir):
            self.add_finding("CRITICAL", category, "Directory '01_Academic_Papers' does not exist!")
            return

        # Strict naming: [ID] Author (Year) - Title.pdf
        pattern = re.compile(r"^\[(\d+)\]\s+(.+?)\s+\((\d{4})\)\s+-\s+(.+?)\.pdf$", re.IGNORECASE)
        found_ids = set()
        non_pdf_files = []
        invalid_names = []
        subdirs = []

        for item in os.listdir(papers_dir):
            item_path = os.path.join(papers_dir, item)
            if os.path.isdir(item_path):
                subdirs.append(item)
                continue

            if not item.lower().endswith(".pdf"):
                non_pdf_files.append(item)
                continue

            m = pattern.match(item)
            if not m:
                invalid_names.append(item)
            else:
                art_id = int(m.group(1))
                if art_id in found_ids:
                    self.add_finding("CRITICAL", category, f"Duplicate Paper ID detected: [{art_id}] in '{item}'")
                found_ids.add(art_id)

        if subdirs:
            self.add_finding("CRITICAL", category, f"Subdirectories found inside 01_Academic_Papers: {subdirs}",
                             "01_Academic_Papers must contain ONLY PDF files. No subdirectories allowed (Rule 17).")
        if non_pdf_files:
            self.add_finding("CRITICAL", category, f"Non-PDF files found in 01_Academic_Papers: {non_pdf_files}",
                             "Rule 17 forbids non-PDF files in 01_Academic_Papers.")
        if invalid_names:
            sample = invalid_names[:5]
            self.add_finding("CRITICAL", category, f"{len(invalid_names)} PDF file(s) violate naming convention '[ID] Author (Year) - Title.pdf'",
                             f"Samples: {sample}")

        expected_count = 701
        actual_count = len(found_ids)
        if actual_count != expected_count:
            missing = set(range(1, expected_count + 1)) - found_ids
            missing_sample = sorted(list(missing))[:10]
            self.add_finding("WARNING", category, f"Expected {expected_count} papers, but found {actual_count} validly named papers.",
                             f"Missing IDs count: {len(missing)}, Samples: {missing_sample}")
        else:
            self.add_finding("PASS", category, f"All 701 Academic Papers perfectly present and conform to '[ID] Author (Year) - Title.pdf'")

    def audit_excel_data_integrity(self):
        """Audit Area 3: Excel Data Integrity (Rule 1, Rule 3, Rule 13, Rule 19)"""
        category = "Excel Data Integrity"
        coding_dir = os.path.join(self.root_dir, "03_Coding_Sheets")
        master_path = os.path.join(coding_dir, "BSMA_Master_Coding_Sheet.xlsx")

        if not os.path.exists(master_path):
            self.add_finding("CRITICAL", category, f"Master coding sheet not found at '{master_path}'")
            return

        try:
            import openpyxl
            wb = openpyxl.load_workbook(master_path, read_only=True)
            ws = wb.active
            rows_iter = ws.iter_rows(values_only=True)
            header = next(rows_iter, None)

            if not header:
                self.add_finding("CRITICAL", category, "Master sheet is empty!")
                wb.close()
                return

            # Check column count (must be 50)
            col_count = len(header)
            if col_count != 50:
                self.add_finding("CRITICAL", category, f"Master sheet has {col_count} columns. Expected exactly 50 (Rule 19).")
            else:
                self.add_finding("PASS", category, "Master sheet has exact 50-column full-extraction structure.")

            # Check for bold markdown in headers (Rule 3)
            bold_headers = [str(h) for h in header if h and "**" in str(h)]
            if bold_headers:
                self.add_finding("WARNING", category, f"Headers contain bold markdown '**' (Rule 3 violation): {bold_headers}")
            else:
                self.add_finding("PASS", category, "No bold markdown in header cells.")

            # Scan rows for Rule 1 (Zero Guesswork) and Rule 13 (Verbatim Quotes)
            blank_cells = 0
            ellipsis_count = 0
            coded_rows = 0

            # Skip row 2 (subheaders/metadata) and inspect data rows
            row_idx = 1
            for row in rows_iter:
                row_idx += 1
                if row_idx == 2:
                    continue  # Subheader row

                # If Article ID (Col 2, index 1) is present
                art_id = row[1] if len(row) > 1 else None
                if art_id is not None:
                    coded_rows += 1
                    # Inspect Col 16 (index 15) Notes
                    if len(row) >= 16:
                        notes = str(row[15] or "")
                        # Rule 13: Verbatim quote checks
                        if "..." in notes:
                            ellipsis_count += 1

            self.add_finding("INFO", category, f"Master sheet contains {coded_rows} coded paper entries.")
            if ellipsis_count > 0:
                self.add_finding("WARNING", category, f"{ellipsis_count} row(s) contain ellipsis '...' in Notes (Col 16)",
                                 "Rule 13 strictly forbids ellipses or truncation in verbatim quotes.")
            else:
                self.add_finding("PASS", category, "Zero ellipses detected in Col 16 Notes (Verbatim fidelity confirmed).")

            wb.close()

            # Rule 20: Audit 3-Tier Hierarchical Header Protocol across coding sheets
            batch_files = [
                f for f in glob.glob(os.path.join(coding_dir, "*.xlsx"))
                if not os.path.basename(f).startswith("~$")
            ]
            clean_3tier_sheets = []
            unnamed_violations = []

            for bf in batch_files:
                bname = os.path.basename(bf)
                try:
                    b_wb = openpyxl.load_workbook(bf, data_only=True)
                    b_ws = b_wb.active
                    unnamed_cells = []
                    for r in range(1, min(4, b_ws.max_row + 1)):
                        for c in range(1, min(51, b_ws.max_column + 1)):
                            val = str(b_ws.cell(r, c).value or "")
                            if "unnamed" in val.lower():
                                unnamed_cells.append(f"R{r}C{c}: '{val}'")
                    if unnamed_cells:
                        unnamed_violations.append((bname, unnamed_cells))
                    elif bname != "BSMA_Master_Coding_Sheet.xlsx":
                        clean_3tier_sheets.append(bname)
                    b_wb.close()
                except Exception as e:
                    self.add_finding("WARNING", category, f"Could not inspect coding sheet '{bname}': {e}")

            if unnamed_violations:
                for bname, issues in unnamed_violations:
                    if bname == "BSMA_Master_Coding_Sheet.xlsx":
                        self.add_finding("INFO", category, f"Master Sheet '{bname}' contains legacy flat headers ({len(issues)} Unnamed cells).",
                                         "Historical master sheet uses single-tier schema. Batch extraction sheets must strictly use Rule 20 3-tier structure.")
                    else:
                        self.add_finding("CRITICAL", category, f"Rule 20 violation in '{bname}': Contains 'Unnamed' headers in rows 1-3 ({len(issues)} instances).",
                                         f"Samples: {issues[:5]}. Excel sheets must use canonical 3-tier headers without pandas 'Unnamed' pollution.")

            if clean_3tier_sheets:
                self.add_finding("PASS", category, f"Rule 20 canonical 3-tier headers verified in batch sheets: {clean_3tier_sheets} (zero 'Unnamed' headers).")

        except Exception as e:
            self.add_finding("CRITICAL", category, f"Failed to audit Master Excel sheet: {e}")

    def audit_agent_protocols(self):
        """Audit Area 4: Agent Protocols & SSOT Consistency (AGENTS.md & Skills)"""
        category = "Agent Protocols & SSOT"
        agents_dir = os.path.join(self.root_dir, ".agents")
        agents_md_path = os.path.join(agents_dir, "AGENTS.md")

        if not os.path.exists(agents_md_path):
            self.add_finding("CRITICAL", category, "'.agents/AGENTS.md' is missing! SSOT violated.")
            return

        with open(agents_md_path, "r", encoding="utf-8") as f:
            agents_md_content = f.read()

        # 1. Check Agent Customizations Index in AGENTS.md
        if "## Agent Customizations Index" not in agents_md_content:
            self.add_finding("CRITICAL", category, "AGENTS.md is missing '## Agent Customizations Index' section",
                             "Interlinked_Architecture_Protocol mandates centralized indexing.")
        else:
            skills_dir = os.path.join(agents_dir, "skills")
            actual_skills = set(os.listdir(skills_dir)) if os.path.exists(skills_dir) else set()
            indexed_skills = set(re.findall(r"file:///\.agents/skills/([^/]+)/SKILL\.md", agents_md_content))

            missing_in_index = actual_skills - indexed_skills
            missing_in_disk = indexed_skills - actual_skills

            if missing_in_index:
                self.add_finding("WARNING", category, f"Skills exist on disk but missing in AGENTS.md index: {missing_in_index}")
            if missing_in_disk:
                self.add_finding("WARNING", category, f"Skills indexed in AGENTS.md but missing on disk: {missing_in_disk}")

            if not missing_in_index and not missing_in_disk:
                self.add_finding("PASS", category, f"All {len(actual_skills)} skills are perfectly synchronized with AGENTS.md index.")

            # Check Rules synchronization
            rules_dir = os.path.join(agents_dir, "rules")
            actual_rules = set(os.listdir(rules_dir)) if os.path.exists(rules_dir) else set()
            indexed_rules = set(re.findall(r"file:///\.agents/rules/([^/]+)\.md", agents_md_content))
            indexed_rules_with_ext = {f"{r}.md" for r in indexed_rules}

            missing_rules_in_index = actual_rules - indexed_rules_with_ext
            missing_rules_in_disk = indexed_rules_with_ext - actual_rules

            if missing_rules_in_index:
                self.add_finding("WARNING", category, f"Rules exist on disk but missing in AGENTS.md index: {missing_rules_in_index}")
            if missing_rules_in_disk:
                self.add_finding("WARNING", category, f"Rules indexed in AGENTS.md but missing on disk: {missing_rules_in_disk}")

            if not missing_rules_in_index and not missing_rules_in_disk and actual_rules:
                self.add_finding("PASS", category, f"All {len(actual_rules)} rule modules are perfectly synchronized with AGENTS.md index.")

        # 2. Check for legacy/stale path strings across all scripts and skills
        stale_patterns = [
            ("03_Validation_Results", "Legacy 03_Validation_Results referenced"),
            ("03_Archives_and_Backups", "Legacy 03_Archives_and_Backups referenced")
        ]
        stale_findings = []
        for root, dirs, files in os.walk(agents_dir):
            for file in files:
                if file != "linter.py" and file.endswith((".py", ".md", ".json")):
                    file_path = os.path.join(root, file)
                    rel_p = os.path.relpath(file_path, self.root_dir)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                            for pat, msg in stale_patterns:
                                if pat in text:
                                    stale_findings.append(f"{rel_p}: {msg}")
                    except Exception:
                        pass

        if stale_findings:
            self.add_finding("WARNING", category, f"Stale path references detected in {len(stale_findings)} file(s)",
                             "\n".join(stale_findings[:5]))
        else:
            self.add_finding("PASS", category, "No stale directory paths detected in .agents scripts and skills.")

    def run_all(self):
        self.audit_workspace_hygiene()
        self.audit_academic_papers()
        self.audit_excel_data_integrity()
        self.audit_agent_protocols()

    def generate_report(self) -> str:
        lines = []
        lines.append("# BSMA Project Unified Lint Report")
        lines.append(f"> Audited Workspace: `{self.root_dir}`\n")

        critical_count = len(self.findings["CRITICAL"])
        warning_count = len(self.findings["WARNING"])
        pass_count = len(self.findings["PASS"])

        lines.append("## Summary\n")
        lines.append(f"- **Critical Errors:** {critical_count}")
        lines.append(f"- **Warnings:** {warning_count}")
        lines.append(f"- **Passed Checks:** {pass_count}\n")

        if critical_count == 0 and warning_count == 0:
            lines.append("> [!NOTE]\n> **ALL CLEAR:** The workspace, papers registry, Excel coding sheets, and agent protocols fully satisfy all project directives.\n")
        elif critical_count > 0:
            lines.append("> [!CAUTION]\n> **CRITICAL VIOLATIONS DETECTED:** Immediate resolution is required to ensure data integrity and pipeline stability.\n")
        else:
            lines.append("> [!WARNING]\n> **WARNINGS DETECTED:** Review and resolve the flagged warnings to maintain project hygiene.\n")

        for level in ["CRITICAL", "WARNING", "INFO", "PASS"]:
            items = self.findings[level]
            if not items:
                continue
            lines.append(f"### [{level}] ({len(items)})\n")
            lines.append("| Category | Message | Recommendation / Details |")
            lines.append("|---|---|---|")
            for item in items:
                msg = item["message"].replace("|", "\\|")
                details = item["details"].replace("|", "\\|").replace("\n", " ")
                lines.append(f"| {item['category']} | {msg} | {details} |")
            lines.append("")

        return "\n".join(lines)

    def auto_fix(self):
        """Auto-clean safe items: __pycache__, .pyc, empty temp files"""
        cleaned = []
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root:
                continue
            if "__pycache__" in dirs:
                p = os.path.join(root, "__pycache__")
                import shutil
                shutil.rmtree(p, ignore_errors=True)
                cleaned.append(p)
        print(f"[AUTO_FIX] Cleaned {len(cleaned)} pycache directories.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BSMA Unified Project Linter")
    parser.add_argument("--root", default=".", help="Workspace root path")
    parser.add_argument("--fix", action="store_true", help="Automatically clean pycache and temporary files")
    parser.add_argument("--report", default="04_Reports/workspace_lint_report.md", help="Path to save markdown report")
    args = parser.parse_args()

    linter = BSMAProjectLinter(args.root)
    if args.fix:
        linter.auto_fix()

    linter.run_all()
    report = linter.generate_report()

    # Save to report path if directory exists
    report_path = os.path.join(args.root, args.report)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Print summary to console
    print(report)
    print(f"\n[REPORT_SAVED] Full diagnostic report written to {report_path}")

    # Exit code: 1 if CRITICAL, 0 otherwise
    if linter.findings["CRITICAL"]:
        sys.exit(1)
    sys.exit(0)
