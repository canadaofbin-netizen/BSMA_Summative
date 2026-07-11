import os
import shutil
import zipfile
from datetime import datetime

def backup_databases():
    """
    Backs up the core database files into a timestamped zip archive
    in the 99_Archives_and_Backups/02_Database_Milestones directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join("99_Archives_and_Backups", "02_Database_Milestones")
    os.makedirs(backup_dir, exist_ok=True)
    
    zip_filename = os.path.join(backup_dir, f"db_milestone_{timestamp}.zip")
    
    files_to_backup = [
        "coding sheet data extraction.xlsx",
        "batch_queue.csv",
        "error_log.md"
    ]
    
    print(f"Initiating automated backup to {zip_filename}...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_backup:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"  - Backed up: {file}")
                else:
                    print(f"  - Skipped (not found): {file}")
        print(f"[BACKUP_SUCCESS] Milestone snapshot saved to {zip_filename}")
    except Exception as e:
        print(f"[BACKUP_ERROR] Failed to create backup: {e}")

if __name__ == "__main__":
    backup_databases()
