import json

log_path = r'C:\Users\lim\.gemini\antigravity\brain\c0c1d8b2-7cab-4efd-8035-e3b03a510574\.system_generated\logs\transcript.jsonl'

entries = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        entries.append(json.loads(line))

for i in range(len(entries)-1, -1, -1):
    e = entries[i]
    t = e.get('type')
    c = e.get('content', '')
    if t == 'USER_INPUT':
        if any(k in c for k in ['의자', '꼬고', '분석', '어때', '맞는거야', '먼지만']):
            print(f"\n================ USER ENTRY {i} ================")
            print(c)
    elif t == 'PLANNER_RESPONSE' and any(k in c for k in ['수정했으면', '어색', '잘못된']):
        print(f"\n================ ASSISTANT ENTRY {i} ================")
        print(c[:2000])
