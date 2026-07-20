import json

transcript_path = r"C:\Users\yunky\.gemini\antigravity\brain\d41acc3d-ee84-4769-ad17-aa513248f445\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("type") == "USER_INPUT":
                content = data.get("content", "")
                if "지우" in content or "다시" in content or "validation" in content.lower():
                    print(f"USER: {content.strip()}")
        except:
            pass
