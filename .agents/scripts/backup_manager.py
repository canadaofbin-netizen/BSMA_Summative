import os
import glob
import hashlib
import zipfile
from datetime import datetime


def _compute_fileset_digest(file_paths: list[str], root_dir: str) -> str:
    """Compute a deterministic SHA-256 digest over sorted (arcname, content_sha256) pairs."""
    hasher = hashlib.sha256()
    entries = []
    for fpath in file_paths:
        if not os.path.isfile(fpath):
            continue
        arcname = os.path.relpath(fpath, root_dir).replace("\\", "/")
        with open(fpath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        entries.append((arcname, file_hash))
    for arcname, file_hash in sorted(entries):
        hasher.update(f"{arcname}:{file_hash}\n".encode("utf-8"))
    return hasher.hexdigest()


def _compute_zip_digest(zip_path: str) -> str | None:
    """Compute the same deterministic SHA-256 digest for an existing zip archive."""
    try:
        hasher = hashlib.sha256()
        entries = []
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                arcname = info.filename.replace("\\", "/")
                file_hash = hashlib.sha256(zf.read(info.filename)).hexdigest()
                entries.append((arcname, file_hash))
        for arcname, file_hash in sorted(entries):
            hasher.update(f"{arcname}:{file_hash}\n".encode("utf-8"))
        return hasher.hexdigest()
    except Exception:
        return None


def collect_files_to_backup(root_dir: str = ".") -> list[str]:
    """Dynamically collect all active coding sheets, key reports, and .agents configuration."""
    files = []

    # 1. All .xlsx files in 03_Coding_Sheets/ (excluding Excel lock files)
    coding_dir = os.path.join(root_dir, "03_Coding_Sheets")
    if os.path.isdir(coding_dir):
        for fname in sorted(os.listdir(coding_dir)):
            if fname.endswith(".xlsx") and not fname.startswith("~$"):
                files.append(os.path.join(coding_dir, fname))

    # 2. Key reports in 04_Reports/
    for report_name in ["CHANGELOG.md", "Match_Rate_Report.md", "final_screening_report.md"]:
        rpath = os.path.join(root_dir, "04_Reports", report_name)
        if os.path.isfile(rpath):
            files.append(rpath)

    # 3. All files in .agents/ (excluding __pycache__ and .pyc)
    agents_dir = os.path.join(root_dir, ".agents")
    if os.path.isdir(agents_dir):
        for dirpath, dirnames, filenames in os.walk(agents_dir):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for fname in sorted(filenames):
                if not fname.endswith(".pyc"):
                    files.append(os.path.join(dirpath, fname))

    return files


def backup_databases(root_dir: str = ".") -> str | None:
    """
    Backs up all active coding sheets in 03_Coding_Sheets/, key reports in 04_Reports/,
    and .agents/ into a timestamped zip archive in 99_Archives_and_Backups/02_Database_Milestones
    with SHA-256 content deduplication.
    """
    root_dir = os.path.abspath(root_dir)
    backup_dir = os.path.join(root_dir, "99_Archives_and_Backups", "02_Database_Milestones")
    os.makedirs(backup_dir, exist_ok=True)

    files_to_backup = collect_files_to_backup(root_dir)
    if not files_to_backup:
        print("[BACKUP_WARNING] No files found to back up.")
        return None

    current_digest = _compute_fileset_digest(files_to_backup, root_dir)

    # Check existing zip archives for identical content snapshot (SHA-256 deduplication)
    existing_zips = sorted(glob.glob(os.path.join(backup_dir, "db_milestone_*.zip")))
    for zpath in existing_zips:
        if _compute_zip_digest(zpath) == current_digest:
            rel_z = os.path.relpath(zpath, root_dir)
            print(f"[BACKUP_SKIPPED] Identical snapshot (SHA-256: {current_digest[:12]}) already exists at {rel_z}")
            return zpath

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(backup_dir, f"db_milestone_{timestamp}.zip")
    rel_zip = os.path.relpath(zip_filename, root_dir)

    print(f"Initiating automated backup to {rel_zip} ({len(files_to_backup)} files)...")

    try:
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for fpath in files_to_backup:
                if os.path.isfile(fpath):
                    arcname = os.path.relpath(fpath, root_dir).replace("\\", "/")
                    zipf.write(fpath, arcname=arcname)
        print(f"[BACKUP_SUCCESS] Milestone snapshot saved to {rel_zip} (SHA-256: {current_digest[:12]})")
        return zip_filename
    except Exception as e:
        print(f"[BACKUP_ERROR] Failed to create backup: {e}")
        return None


if __name__ == "__main__":
    backup_databases()
