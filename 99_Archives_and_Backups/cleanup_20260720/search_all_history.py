import json
import glob

brain_dir = r"C:\Users\yunky\.gemini\antigravity\brain"
transcripts = glob.glob(f"{brain_dir}\\*\\.system_generated\\logs\\transcript.jsonl")

print(f"Searching {len(transcripts)} transcripts...")

for t_path in transcripts:
    with open(t_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "")
                    if "지우" in content or "다시" in content or "삭제" in content:
                        print(f"\nFound in {t_path.split(chr(92))[5]}:")
                        print(f"USER: {content.strip()}")
            except:
                pass
