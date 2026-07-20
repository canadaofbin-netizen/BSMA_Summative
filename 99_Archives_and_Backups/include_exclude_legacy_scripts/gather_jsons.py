import os
import glob
import shutil

brain_dir = r"C:\Users\yunky\.gemini\antigravity\brain"
target_dir = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 1. Gather from brain directories
pattern = os.path.join(brain_dir, "*", "scratch", "outputs", "BSMA*.json")
files = glob.glob(pattern)

# 2. Gather from antigravity scratch directory
antigravity_scratch = r"C:\Users\yunky\.gemini\antigravity\scratch\outputs"
pattern2 = os.path.join(antigravity_scratch, "BSMA*.json")
files.extend(glob.glob(pattern2))

count = 0
for f in files:
    filename = os.path.basename(f)
    dest_path = os.path.join(target_dir, filename)
    
    try:
        shutil.copy2(f, dest_path)
        count += 1
    except Exception as e:
        print(f"Failed to copy {f}: {e}")

print(f"Copied {count} JSON files from subagent directories to {target_dir}")
