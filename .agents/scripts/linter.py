import os
import re
import sys
import glob
import shutil
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
        """Audit Area 1: Workspace & Directory Hygiene (AGENTS.md & workspace_hygiene.md)"""
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
                                     "Only .gitignore and README.md are permitted in the root directory. Coding sheets must be in 03_Coding_Sheets/.")
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
                    self.add_finding("WARNING", category, f"Ghost/Lock file detected: '{rel_f}'", "Run linter with --fix to remove temporary OS/Excel lock files.")

        # 3. Python cache (.pyc / __pycache__)
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root:
                continue
            if "__pycache__" in dirs:
                rel_p = os.path.relpath(os.path.join(root, "__pycache__"), self.root_dir)
                self.add_finding("WARNING", category, f"Python cache directory detected: '{rel_p}'", "Run linter with --fix to clean.")
            for file in files:
                if file.endswith(".pyc"):
                    rel_pyc = os.path.relpath(os.path.join(root, file), self.root_dir)
                    self.add_finding("WARNING", category, f"Compiled Python file detected: '{rel_pyc}'", "Run linter with --fix to clean.")

        # 4. Scratch directory containment (recursive check)
        scratch_dir = os.path.join(self.root_dir, "scratch")
        if os.path.exists(scratch_dir):
            scratch_items = []
            for root, dirs, files in os.walk(scratch_dir):
                for d in dirs:
                    scratch_items.append(os.path.relpath(os.path.join(root, d), scratch_dir))
                for f in files:
                    if f != ".gitkeep":
                        scratch_items.append(os.path.relpath(os.path.join(root, f), scratch_dir))
            if scratch_items:
                self.add_finding("WARNING", category, f"Scratch directory contains {len(scratch_items)} temporary item(s): {scratch_items[:5]}",
                                 "Scratch directory holds temporary files. Clean scratch/ after batch completion.")
            else:
                self.add_finding("PASS", category, "Scratch directory is recursively clean (0 items)")

        if not self.findings["CRITICAL"] and not [f for f in self.findings["WARNING"] if f["category"] == category]:
            self.add_finding("PASS", category, "Root directory zero-pollution and hygiene verified.")

    def audit_academic_papers(self):
        """Audit Area 2: Academic Paper Registry (Rule 17)"""
        category = "Academic Papers Registry"
        papers_dir = os.path.join(self.root_dir, "01_Academic_Papers")

        if not os.path.exists(papers_dir):
            self.add_finding("CRITICAL", category, "Directory '01_Academic_Papers' does not exist!")
            return

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
            self.add_finding("PASS", category, "All 701 Academic Papers perfectly present and conform to '[ID] Author (Year) - Title.pdf'")

    def audit_excel_data_integrity(self):
        """Audit Area 3: Excel Data Integrity (Rules 1, 3, 9, 13, 14, 19, 20, 27)"""
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

            col_count = len(header)
            if col_count != 50:
                self.add_finding("CRITICAL", category, f"Master sheet has {col_count} columns. Expected exactly 50 (Rule 19).")
            else:
                self.add_finding("PASS", category, "Master sheet has exact 50-column full-extraction structure.")

            bold_headers = [str(h) for h in header if h and "**" in str(h)]
            if bold_headers:
                self.add_finding("WARNING", category, f"Headers contain bold markdown '**' (Rule 3 violation): {bold_headers}")
            else:
                self.add_finding("PASS", category, "No bold markdown in header cells.")

            ellipsis_count = 0
            coded_rows = 0
            row_idx = 1
            for row in rows_iter:
                row_idx += 1
                if row_idx == 2:
                    continue
                art_id = row[1] if len(row) > 1 else None
                if art_id is not None:
                    coded_rows += 1
                    if len(row) >= 16:
                        notes = str(row[15] or "")
                        if "..." in notes:
                            ellipsis_count += 1

            self.add_finding("INFO", category, f"Master sheet contains {coded_rows} coded paper entries.")
            if coded_rows != 701:
                self.add_finding("WARNING", category, f"Master sheet has {coded_rows} coded entries (expected 701).")
            if ellipsis_count > 0:
                self.add_finding("WARNING", category, f"{ellipsis_count} row(s) contain ellipsis '...' in Master Sheet Notes (Col 16)",
                                 "Rule 13 strictly forbids ellipses or truncation in verbatim quotes.")
            else:
                self.add_finding("PASS", category, "Zero ellipses detected in Master Sheet Col 16 Notes (Verbatim fidelity confirmed).")

            wb.close()

            # Audit all coding sheets in 03_Coding_Sheets/
            batch_files = sorted([
                f for f in glob.glob(os.path.join(coding_dir, "*.xlsx"))
                if not os.path.basename(f).startswith("~$")
            ])
            clean_3tier_sheets = []
            unnamed_violations = []

            heuristic_missing_papers = []
            forbidden_string_cells = []
            rule9_violations = []
            rule13_batch_ellipses = []
            rule14_violations = []
            rule19_violations = []
            populated_papers_count = 0

            for bf in batch_files:
                bname = os.path.basename(bf)
                try:
                    b_wb = openpyxl.load_workbook(bf, data_only=True)
                    b_ws = b_wb["Extracted Data"] if "Extracted Data" in b_wb.sheetnames else b_wb.active

                    # Rule 20 check
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

                    # Detailed batch sheet row checks for [start]_[end].xlsx
                    if bname != "BSMA_Master_Coding_Sheet.xlsx" and re.match(r"^\d+_\d+", bname):
                        papers_data = {}
                        for r in range(4, b_ws.max_row + 1):
                            art_id = b_ws.cell(r, 2).value
                            if art_id is None:
                                continue
                            try:
                                art_id = int(re.search(r'(\d+)', str(art_id)).group(1))
                            except Exception:
                                continue

                            inc_val = str(b_ws.cell(r, 5).value or "").strip()

                            # Rule 13: Check all text/quote columns for '...'
                            for c in [16, 31, 33, 38, 40, 50]:
                                c_txt = str(b_ws.cell(r, c).value or "")
                                if "..." in c_txt:
                                    rule13_batch_ellipses.append(f"{bname} R{r}C{c} (Paper {art_id})")

                            if inc_val.startswith("1"):
                                if art_id not in papers_data:
                                    papers_data[art_id] = []
                                bs_mean = b_ws.cell(r, 42).value
                                bs_sd = b_ws.cell(r, 43).value
                                notes_col = str(b_ws.cell(r, 50).value or "").strip()
                                papers_data[art_id].append((r, bs_mean, bs_sd, notes_col))

                                # Rule 1: Forbidden strings in numeric columns
                                for c in [22, 23, 24, 25, 27, 28, 29, 34, 35, 36, 42, 43, 44, 46, 47, 48, 49]:
                                    c_val = b_ws.cell(r, c).value
                                    if isinstance(c_val, str) and c_val.strip().lower() in ("not reported", "n/a", "none", "-"):
                                        forbidden_string_cells.append(f"{bname} R{r}C{c}: '{c_val}'")

                                # Rule 9: Col 50 must start with Table
                                if not notes_col.lower().startswith("table"):
                                    rule9_violations.append(f"{bname} R{r}C50 (Paper {art_id}): '{notes_col[:40]}'")

                                # Rule 14: Specific Measure Used substring of Quote column when both present
                                c32 = b_ws.cell(r, 32).value
                                c33 = b_ws.cell(r, 33).value
                                if c32 and c33 and str(c32).strip() not in str(c33):
                                    rule14_violations.append(f"{bname} R{r}C32 '{c32}' not in Col 33")
                                c39 = b_ws.cell(r, 39).value
                                c40 = b_ws.cell(r, 40).value
                                if c39 and c40 and str(c39).strip() not in str(c40):
                                    rule14_violations.append(f"{bname} R{r}C39 '{c39}' not in Col 40")

                                # Rule 19: Col 3 and Cols 7-16 must be blank in batch extraction sheets
                                for c in [3] + list(range(7, 17)):
                                    v = b_ws.cell(r, c).value
                                    if v is not None and str(v).strip() != "":
                                        rule19_violations.append(f"{bname} R{r}C{c} (Included Paper {art_id} non-blank)")

                            elif inc_val.startswith("0"):
                                # Rule 19: Excluded paper must have Cols 7-50 completely blank
                                for c in range(7, 51):
                                    v = b_ws.cell(r, c).value
                                    if v is not None and str(v).strip() != "":
                                        rule19_violations.append(f"{bname} R{r}C{c} (Excluded Paper {art_id} non-blank)")

                        for art_id, rows in papers_data.items():
                            total_rows = len(rows)
                            if total_rows == 0:
                                continue
                            all_missing_mean = all(m is None or str(m).strip() in ("999", "999.0", "") for _, m, _, _ in rows)
                            all_missing_sd = all(s is None or str(s).strip() in ("999", "999.0", "") for _, _, s, _ in rows)
                            is_latent = any("latent" in note.lower() for _, _, _, note in rows)
                            if all_missing_mean and all_missing_sd:
                                heuristic_missing_papers.append((bname, art_id, total_rows, is_latent))
                            else:
                                populated_papers_count += 1

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
                self.add_finding("PASS", category, f"Rule 20 canonical 3-tier headers verified in {len(clean_3tier_sheets)} sheets: {clean_3tier_sheets} (zero 'Unnamed' headers).")

            if forbidden_string_cells:
                self.add_finding("CRITICAL", category, f"Rule 1 violation: {len(forbidden_string_cells)} numeric cell(s) contain forbidden text strings.",
                                 f"Samples: {forbidden_string_cells[:5]}. Numeric missing fields must be '999'.")
            else:
                self.add_finding("PASS", category, "Rule 1 Dual Missing Data verified: Zero forbidden text strings in numeric columns across all batch sheets.")

            if rule9_violations:
                self.add_finding("WARNING", category, f"Rule 9 violation: {len(rule9_violations)} row(s) missing 'Table X' coordinate prefix in Col 50.",
                                 f"Samples: {rule9_violations[:5]}")
            else:
                self.add_finding("PASS", category, "Rule 9 Provenance Coordinates verified: 100% of included batch rows start with 'Table X' in Col 50.")

            if rule13_batch_ellipses:
                self.add_finding("WARNING", category, f"Rule 13 violation: {len(rule13_batch_ellipses)} cell(s) in batch sheets contain ellipsis '...'",
                                 f"Samples: {rule13_batch_ellipses[:5]}")
            else:
                self.add_finding("PASS", category, "Rule 13 Verbatim Quotes verified: Zero ellipses ('...') across all 7 batch extraction sheets.")

            if rule14_violations:
                self.add_finding("WARNING", category, f"Rule 14 violation: {len(rule14_violations)} specific measure name(s) not verbatim substrings of quote columns.",
                                 f"Samples: {rule14_violations[:5]}")
            else:
                self.add_finding("PASS", category, "Rule 14 Measure Substring Fidelity verified across all 7 batch extraction sheets.")

            if rule19_violations:
                self.add_finding("WARNING", category, f"Rule 19 violation: {len(rule19_violations)} cell(s) violate batch sheet blank-column rules.",
                                 f"Samples: {rule19_violations[:5]}")
            else:
                self.add_finding("PASS", category, "Rule 19 Streamlined Batch Schema verified (Cols 3 & 7-16 blank on included; Cols 7-50 blank on excluded).")

            if heuristic_missing_papers:
                for bname, art_id, total_rows, is_latent in heuristic_missing_papers:
                    latent_info = " (Latent correlation matrix verified in Col 50 Notes)" if is_latent else " (Action: check if source correlation table reported Means/SDs)"
                    self.add_finding("INFO", category, f"Heuristic Data Notice in '{bname}': Paper [{art_id}] has 100% missing Mean and SD across {total_rows} rows{latent_info}.",
                                     "Rule 27: Ensure source paper correlation table was thoroughly audited for descriptive statistics.")
            if populated_papers_count > 0:
                self.add_finding("PASS", category, f"Rule 27 Lossless Parity verified: {populated_papers_count} included paper(s) in batch sheets have populated empirical Mean/SD metrics.")

        except Exception as e:
            self.add_finding("CRITICAL", category, f"Failed to audit Excel coding sheets: {e}")

    def audit_agent_protocols(self):
        """Audit Area 4: Agent Protocols & SSOT Consistency (AGENTS.md, Rules, Skills, Scripts)"""
        category = "Agent Protocols & SSOT"
        agents_dir = os.path.join(self.root_dir, ".agents")
        agents_md_path = os.path.join(agents_dir, "AGENTS.md")

        if not os.path.exists(agents_md_path):
            self.add_finding("CRITICAL", category, "'.agents/AGENTS.md' is missing! SSOT violated.")
            return

        with open(agents_md_path, "r", encoding="utf-8") as f:
            agents_md_content = f.read()

        if "## Agent Customizations Index" not in agents_md_content:
            self.add_finding("CRITICAL", category, "AGENTS.md is missing '## Agent Customizations Index' section",
                             "Interlinked_Architecture_Protocol mandates centralized indexing.")
        else:
            # 1. Check Skills synchronization
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

            # 2. Check Rules synchronization
            rules_dir = os.path.join(agents_dir, "rules")
            actual_rules = set(os.listdir(rules_dir)) if os.path.exists(rules_dir) else set()
            indexed_rules = set(re.findall(r"file:///\.agents/rules/([^/\)]+)\.md", agents_md_content))
            indexed_rules_with_ext = {f"{r}.md" for r in indexed_rules}

            missing_rules_in_index = actual_rules - indexed_rules_with_ext
            missing_rules_in_disk = indexed_rules_with_ext - actual_rules

            if missing_rules_in_index:
                self.add_finding("WARNING", category, f"Rules exist on disk but missing in AGENTS.md index: {missing_rules_in_index}")
            if missing_rules_in_disk:
                self.add_finding("WARNING", category, f"Rules indexed in AGENTS.md but missing on disk: {missing_rules_in_disk}")

            if not missing_rules_in_index and not missing_rules_in_disk and actual_rules:
                self.add_finding("PASS", category, f"All {len(actual_rules)} rule modules are perfectly synchronized with AGENTS.md index.")

            # 3. Check Scripts synchronization
            scripts_dir = os.path.join(agents_dir, "scripts")
            actual_scripts = {f for f in os.listdir(scripts_dir) if f.endswith(".py")} if os.path.exists(scripts_dir) else set()
            indexed_scripts = set(re.findall(r"file:///\.agents/scripts/([^/\)]+\.py)", agents_md_content))

            missing_scripts_in_index = actual_scripts - indexed_scripts
            missing_scripts_in_disk = indexed_scripts - actual_scripts

            if missing_scripts_in_index:
                self.add_finding("WARNING", category, f"Scripts exist on disk but missing in AGENTS.md index: {missing_scripts_in_index}")
            if missing_scripts_in_disk:
                self.add_finding("WARNING", category, f"Scripts indexed in AGENTS.md but missing on disk: {missing_scripts_in_disk}")

            if not missing_scripts_in_index and not missing_scripts_in_disk and actual_scripts:
                self.add_finding("PASS", category, f"All {len(actual_scripts)} core scripts in .agents/scripts/ are synchronized with AGENTS.md index.")

        # 4. Check for legacy/stale path strings across all scripts and skills
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
        """Auto-clean safe items: __pycache__, .pyc, ghost/lock files (~$*.xlsx, Thumbs.db, .DS_Store)"""
        cleaned = []
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root:
                continue
            if "__pycache__" in dirs:
                p = os.path.join(root, "__pycache__")
                shutil.rmtree(p, ignore_errors=True)
                cleaned.append(p)
            for file in files:
                if file.endswith(".pyc") or file in ("Thumbs.db", ".DS_Store") or (file.startswith("~$") and file.endswith(".xlsx")):
                    fp = os.path.join(root, file)
                    try:
                        os.remove(fp)
                        cleaned.append(fp)
                    except Exception:
                        pass
        print(f"[AUTO_FIX] Cleaned {len(cleaned)} cache/ghost items.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BSMA Unified Project Linter")
    parser.add_argument("--root", default=".", help="Workspace root path")
    parser.add_argument("--fix", action="store_true", help="Automatically clean pycache and temporary ghost files")
    parser.add_argument("--report", default="04_Reports/workspace_lint_report.md", help="Path to save markdown report")
    args = parser.parse_args()

    linter = BSMAProjectLinter(args.root)
    if args.fix:
        linter.auto_fix()

    linter.run_all()
    report = linter.generate_report()

    report_path = os.path.join(args.root, args.report)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n[REPORT_SAVED] Full diagnostic report written to {report_path}")

    if linter.findings["CRITICAL"]:
        sys.exit(1)
    sys.exit(0)
