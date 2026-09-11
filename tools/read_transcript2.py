import json

log_path = r'C:\Users\lim\.gemini\antigravity\brain\c0c1d8b2-7cab-4efd-8035-e3b03a510574\.system_generated\logs\transcript.jsonl'

entries = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        entries.append(json.loads(line))

for i in range(len(entries)-1, max(0, len(entries)-100), -1):
    e = entries[i]
    t = e.get('type')
    c = e.get('content', '')
    if t == 'USER_INPUT' and any(k in c for k in ['수정', '분석', '어색', '보고해']):
        print(f"\n================ USER ENTRY {i} ================")
        print(c)
    elif t == 'PLANNER_RESPONSE' and any(k in c for k in ['잘못된 이미지', '수정 제안', '어색한']):
        print(f"\n================ ASSISTANT ENTRY {i} ================")
        print(c[:2000])
