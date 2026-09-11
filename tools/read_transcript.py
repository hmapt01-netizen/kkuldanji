import json

log_path = r'C:\Users\lim\.gemini\antigravity\brain\c0c1d8b2-7cab-4efd-8035-e3b03a510574\.system_generated\logs\transcript.jsonl'

entries = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        entries.append(json.loads(line))

print(f"Total entries: {len(entries)}")

# Search backwards for "수정" or image analysis
for i in range(len(entries)-1, -1, -1):
    e = entries[i]
    t = e.get('type')
    c = e.get('content', '')
    if t == 'USER_INPUT':
        print(f"\n--- Entry {i} (USER) ---")
        print(c)
    elif t == 'PLANNER_RESPONSE' and ('어색' in c or '수정' in c or '분석' in c or '골프공' in c):
        print(f"\n--- Entry {i} (ASSISTANT snippet) ---")
        lines = c.split('\n')
        for l in lines[:30]:
            print(l)
        if len(lines) > 30:
            print("...")
        if len(entries) - i > 25:
            break
